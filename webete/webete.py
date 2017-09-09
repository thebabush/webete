#!/usr/bin/env python3

import argparse
import io
import itertools
import logging
import os

import requests
import xdis.load
import uncompyle6.semantics.pysource
import urllib.parse

from .__init__ import __version__
from . import settings
from . import util

log = logging.getLogger()


class Requester:
    '''
    Magic proxy class for requests. Each instance is bound to a single session.
    Every call is proxied to a requests.Session()
    '''
    session = None

    def __init__(self):
        self._session = requests.Session()
        # Here you'd put your auth stuff etc.
        pass

    def __getattr__(self, name):
        return getattr(self._session, name)


# An instance of Requester provided for each function that does not need a clean session
# Maybe we'd like to build it in __main__ as to support auth between different objects
requester = Requester()


class PrettyPrinter:
    '''
    Class to pretty-print stuff. Provides a header method to print headers between different probing modes
    and other helper functions
    '''
    @staticmethod
    def header(text):
        print('=' * settings.SECTION_WIDTH + ' {} '.format(text) + '=' * settings.SECTION_WIDTH)

    @staticmethod
    def file_probing(name):
        print('*' * settings.LIST_INDENT + ' Trying {}...'.format(name), end=' ')

    @staticmethod
    def file_probed(status, content=None):
        print(status)
        if content:
            print(content)


printer = PrettyPrinter()


def probe_file(target, name, get_content=True):
    '''
    :param target: base URL and folder of website to probe
    :param name: name of file to be probed
    :param get_content: whether to GET and return the file content, if the file is found
    :return: status_code of the request. If status_code is 200 and parameter get_content is True, returns also content
    '''
    # url = urllib.parse.urljoin(target, name)
    # urllib has some "problems", i.e., it fixes relative paths and removes any ../
    # Since this is not desirable, I'm leaving this commented for the moment and do some horrible string concat
    url = target + name if target[-1] == "/" else target + "/" + name
    response = requester.head(url)
    content = requester.get(url).text if get_content and response.status_code == 200 else None
    return response.status_code, content


def action_auto(target, custom_targets=()):
    printer.header("AUTO SCAN")

    # Step 1 - typical config files
    for f_name in settings.AUTO_PROBE + list(custom_targets):
        printer.file_probing(f_name)
        status_code, content = probe_file(target, f_name)
        printer.file_probed(status_code, content)

    # Step 2 - dir traversal vulnerability
    printer.file_probing("Directory traversal to /etc/passwd")
    status_code, content = probe_file(target, settings.PASSWD_TRAVERSAL)
    printer.file_probed(status_code, content)


def action_python(target, fpath):
    # Should we support these?
    # foo.cpython-35.opt-1.pyc
    # foo.cpython-35.opt-2.pyc
    # pypy?

    printer.header('PYTHON')

    # TODO blocks to develop next:
    # WSGI config
    # Probe common files (app.py, main.py, etc)
    # Probe backup files for given names and common files

    # TODO this could be done in probing common files (see above), besides giving explicit targets?
    # Mangle file name
    fpath = util.strip_file_ext_from_list(fpath, ['py'] + settings.PYTHON_EXTS)
    fdir, fname = os.path.split(fpath)

    guess_prefix = target + fdir + '/' if fdir else target
    guesses = itertools.chain(
        ('{}.cpython-{}.{}'.format(fname, ver, ext) for ver, ext in itertools.product(settings.PYTHON_VERSIONS,
                                                                                      settings.PYTHON_EXTS)),
        # TODO BTW sometimes cached files for ABC.py are given as ABC.pyc (no cpython or version #)
        ('__pycache__/{}.cpython-{}.{}'.format(fname, ver, ext) for ver, ext in
         itertools.product(settings.PYTHON_VERSIONS, settings.PYTHON_EXTS))
    )
    for guess in guesses:
        printer.file_probing(guess)
        status_code, content = probe_file(guess_prefix, guess)
        printer.file_probed(status_code)
        if status_code == 200:
            break
    else:
        return None

    version, ts, magic, code, is_pypy, source_size = xdis.load.load_module_from_file_object(io.BytesIO(content))
    out_name = fpath + '.py'
    out_dir = os.path.dirname(out_name)

    # Create output directory if not working on webroot
    if out_dir:
        os.makedirs(os.path.dirname(out_name), exist_ok=True)

    # Decompile and save the file
    with open(out_name, 'w') as f:
        uncompyle6.semantics.pysource.deparse_code(version, code, out=f)
        print('Decompiled to "{}"'.format(out_name))


def dispatch_action(args):
    # TODO I think we can concatenate probings to auto_probing to try & guess language used in smart ways
    if args.auto:
        action_auto(args.target, args.additional_targets)
    elif args.python:
        action_python(args.target, args.python)


def main():
    parser = argparse.ArgumentParser(description='WEBETE - WEB Extensive Testing Environment')

    parser.add_argument('target', help='Target URL (e.g.: http://127.0.0.1/)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', help='Print the version number',
                        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-T', '--additional_targets', nargs='+', type=str, help='List of additional targets to probe',
                        default=[])
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-a', '--auto', action='store_true', help='Automatic simple recon')
    action_group.add_argument('-p', '--python', dest='python', metavar='FILE',
                              help='Look for a specific pyc file under __pycache__ subdir')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.NOTSET)

    log.debug('Args: {}'.format(args))

    dispatch_action(args)
