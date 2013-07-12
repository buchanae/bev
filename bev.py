#!/usr/bin/env python

import json
import logging
import os
import sys
from datetime import datetime


__version__ = '0.3.0'

CMD_BLACKLIST='ls cd'.split()

cmd = os.path.expanduser(os.path.expandvars(' '.join(sys.argv[1:])))

if cmd in CMD_BLACKLIST:
    sys.exit()


logging.basicConfig(level=logging.WARNING)

DEFAULT_LOG_PATH = os.path.expanduser('~/.bev_log')

log_path = os.environ.get('BEV_LOG_PATH', DEFAULT_LOG_PATH)

if not log_path:
    log_path = DEFAULT_LOG_PATH

if not os.path.exists(os.path.dirname(log_path)):
    logging.warning("Bev: log path doesn't exist. {}".format(log_path))
    logging.warning("Bev: reverting to default log path. {}".format(DEFAULT_LOG_PATH))
    log_path = DEFAULT_LOG_PATH


tags = os.environ.get('BEV_TAGS', '')

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
