#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import logging
import os
import sys
from datetime import datetime


__version__ = '1.0.0'

CMD_BLACKLIST='ls cd'.split()
DEFAULT_LOG_PATH = os.path.expanduser('~/.bev_log')

logging.basicConfig(level=logging.WARNING)


def log_handler(args):

    log_path = os.environ.get('BEV_LOG_PATH', DEFAULT_LOG_PATH)

    if not log_path:
        log_path = DEFAULT_LOG_PATH

    if not os.path.exists(os.path.dirname(log_path)):
        logging.warning("Bev: log path doesn't exist. {}".format(log_path))
        logging.warning("Bev: reverting to default log path. {}".format(DEFAULT_LOG_PATH))
        log_path = DEFAULT_LOG_PATH

    cmd = os.path.expanduser(os.path.expandvars(' '.join(args.cmd)))

    if cmd in CMD_BLACKLIST:
        return

    tags = get_tags()

    cwd = os.getcwd()

    last_change = '0'

    if os.path.exists(log_path):
        st = os.stat(log_path)
        last_change = str(st.st_mtime)

    now = str(datetime.now())
    with open(log_path, 'a') as fh:

        s = json.dumps({
            'version': __version__,
            'cwd': cwd,
            'cmd': cmd,
            'last_change': last_change,
            'now': now,
            'tags': tags,
        })
        fh.write(s + '\n')


def get_tags():
    tags = os.environ.get('BEV_TAGS', [])
    if tags:
        tags = tags.split(',')

    return tags


def tags_handler(args):

    tags = set(get_tags())
    tags.update(args.add)

    for t in args.remove:
        tags.remove(t)

    out = ','.join(tags)
    print(out, end='')


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

log_parser = subparsers.add_parser('log')
log_parser.add_argument('cmd', nargs='*')
log_parser.set_defaults(func=log_handler)

tags_parser = subparsers.add_parser('tags')
tags_parser.add_argument('--add', action='append')
tags_parser.add_argument('--remove', action='append')
tags_parser.set_defaults(func=tags_handler, add=[], remove=[])


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
