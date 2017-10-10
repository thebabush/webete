#!/usr/bin/env python3

import argparse
import io
import itertools
import logging
import os

import requests
import xdis.load
import uncompyle6.semantics.pysource

from .__init__ import __version__
from . import printer
from . import settings
from . import util

log = logging.getLogger()
session = requests.Session()


def init_session():
    session.headers.update({
        'User-Agent': settings.HTTP_DEFAULT_USER_AGENT
    })


def action_auto(target):

    def get_file(filename):
        printer.print_header(filename)
        printer.print_request(target + filename, method='get')
        r = session.get(target + filename)
        printer.print_request_result(r.status_code, r.text if r.status_code == 200 else None, settings.PREVIEW_LINES)

    def probe_file(filename):
        printer.print_request(target + filename, method='head')
        r = session.head(target + filename)
        printer.print_request_result(r.status_code)

    # Step 0 - Print raw response headers
    printer.print_header('Response Headers')
    printer.print_request(target, method='get')
    r = session.get(target)
    print(r.status_code)
    if r.status_code == 200:
        for header in r.headers:
            print("{}: {}".format(header, r.headers[header]))

    # Step 1 - Webserver files
    # We GET potentially interesting files
    for _file in settings.AUTO_PROBE_FILES:
        get_file(_file)
    # We only HEAD potentially interesting folders (checking, e.g., for Apache directory listing)
    printer.print_header('Folder probing')
    for _file in settings.AUTO_PROBE_FOLDERS:
        probe_file(_file)

    # Step 2 - Path traversal
    printer.print_header('Path traversal')
    printer.print_request(target + settings.PASSWD_TRAVERSAL, method='get')
    r = session.get(target + settings.PASSWD_TRAVERSAL)
    printer.print_request_result(r.status_code, r.text if r.status_code == 200 else None)

    # Step 3 - Language probing
    printer.print_header('Language probing')
    # Python: try common file names, check also for potential .pyc
    printer.print_header('Python')
    for _file in settings.PYTHON_COMMON:
        probe_file(_file)
        probe_file(_file + 'c')
    # PHP: try PHP easter egg (for PHP < 5.5)
    printer.print_header('PHP < 5.5')
    probe_file(settings.PHP_EASTER_EGG)


def action_python(target, fpath):
    printer.print_header('PYTHON')

    # Mangle file name
    exts = settings.PYTHON_EXTS
    tags = settings.PYTHON_CACHE_TAGS
    fpath = util.strip_file_ext_from_list(fpath, ['py'] + exts)
    fdir, fname = os.path.split(fpath)

    guess_prefix = target + fdir + '/' if fdir else target
    guesses = itertools.chain(
        ('{}.{}'.format(fname, ext) for ext in exts),
        ('{}.{}.{}'.format(fname, tag, ext) for tag, ext in itertools.product(tags, exts)),
        ('__pycache__/{}.{}.{}'.format(fname, tag, ext) for tag, ext in itertools.product(tags, exts))
    )
    for guess in guesses:
        # Build complete target url
        guess_url = guess_prefix + guess

        # Check if it exists
        printer.print_request(guess_url)
        r = session.get(guess_url)
        printer.print_request_result(r.status_code)
        if r.status_code == 200:
            data = r.content
            break
    else:
        print('\nNot found\n')
        return None

    version, ts, magic, code, is_pypy, source_size = xdis.load.load_module_from_file_object(io.BytesIO(data))
    out_name = fpath + '.py'
    out_dir = os.path.dirname(out_name)

    # Create output directory if not working on webroot
    if out_dir:
        os.makedirs(os.path.dirname(out_name), exist_ok=True)

    # Decompile and save the file
    with open(out_name, 'w') as f:
        uncompyle6.semantics.pysource.deparse_code(version, code, out=f)
        print('\nDecompiled to "{}"\n'.format(out_name))


def dispatch_action(args):
    if args.auto:
        action_auto(args.target)
    elif args.python:
        action_python(args.target, args.python)


def main():
    parser = argparse.ArgumentParser(description='WEBETE - WEB Extensive Testing Environment')

    parser.add_argument('target', help='Target URL (e.g.: http://127.0.0.1/)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', help='Print the version number', version='%(prog)s {version}'.format(version=__version__))
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-a', '--auto', action='store_true', help='Automatic simple recon')
    action_group.add_argument('-p', '--python', dest='python', metavar='FILE', help='Look for a specific pyc file under __pycache__ subdir')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.NOTSET)

    log.debug('Args: {}'.format(args))

    init_session()
    dispatch_action(args)
