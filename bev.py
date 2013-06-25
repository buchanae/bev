#!/usr/bin/env python

import json
import os
import sys
from datetime import datetime


__version__ = '0.2'

DEFAULT_LOG_PATH = os.path.expanduser('~/.bev_log')

log_path = os.environ.get('BEV_LOG_PATH', DEFAULT_LOG_PATH)

cmd = os.path.expanduser(os.path.expandvars(' '.join(sys.argv[1:])))

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
    })
    fh.write(s + '\n')
