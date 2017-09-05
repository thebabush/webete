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
from . import settings
from . import util

log = logging.getLogger()


def start_section(name):
    print('=' * settings.SECTION_WIDTH + ' {} '.format(name) + '=' * settings.SECTION_WIDTH)


def action_auto(target):
    start_section('robots.txt')
    r = requests.get(target + 'robots.txt')
    if r.status_code == 200:
        print(r.text)
    else:
        print(r.status_code)


def action_python(target, fpath):
    # Should we support these?
    # foo.cpython-35.opt-1.pyc
    # foo.cpython-35.opt-2.pyc
    # pypy?
    PYTHON_EXTS = ['pyc', 'pyd', 'pyo']
    PYTHON_VERSIONS = ['26', '27', '35', '36', '37']

    start_section('PYTHON')

    # Mangle file name
    fpath = util.strip_file_ext_from_list(fpath, ['py'] + PYTHON_EXTS)
    fdir, fname = os.path.split(fpath)

    guess_prefix = target + fdir + '/' if fdir else target 
    for guess in itertools.chain(
            ('{}.cpython-{}.{}'.format(fname, ver, ext) for ver, ext in itertools.product(PYTHON_VERSIONS, PYTHON_EXTS)),
            ('__pycache__/{}.cpython-{}.{}'.format(fname, ver, ext) for ver, ext in itertools.product(PYTHON_VERSIONS, PYTHON_EXTS))
        ):
        # Build complete target url
        guess_url = guess_prefix + guess

        # Check if it exists
        log.info('Trying "{}"...'.format(guess))
        r = requests.get(guess_url)
        if r.status_code == 200:
            print('FOUND: {} @ {}'.format(guess, guess_url))
            data = r.content
            break
    else:
        return None
    
    version, ts, magic, code, is_pypy, source_size = xdis.load.load_module_from_file_object(io.BytesIO(data))
    out_name = fpath + '.py'
    out_dir  = os.path.dirname(out_name)

    # Create output directory if not working on webroot
    if out_dir:
        os.makedirs(os.path.dirname(out_name), exist_ok=True)

    # Decompile and save the file
    with open(out_name, 'w') as f:
        uncompyle6.semantics.pysource.deparse_code(version, code, out=f)
        print('Decompiled to "{}"'.format(out_name))


def dispatch_action(args):
    if args.auto:
        action_auto(args.target)
    elif args.python:
        action_python(args.target, args.python)


def main():
    parser = argparse.ArgumentParser(description='WEBETE - WEB Extensive Testing Environment')

    parser.add_argument('target', help='Target URL (e.g.: http://127.0.0.1/)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-a', '--auto', action='store_true', help='Automatic simple recon')
    action_group.add_argument('-p', '--py', dest='python', help='Look for a specific pyc file')
    action_group.add_argument('--version', action='store_true', help='Print the version number')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.NOTSET)
    log.debug('Args: {}'.format(args))

    dispatch_action(args)

