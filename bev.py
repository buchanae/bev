#!/usr/bin/env python

import os
import sys
from datetime import datetime


DEFAULT_LOG_PATH = os.path.expanduser('~/.bev_log')

log_path = os.environ.get('BEV_LOG_PATH', DEFAULT_LOG_PATH)

cmd = os.path.expanduser(os.path.expandvars(' '.join(sys.argv[1:])))

cwd = os.getcwd()

last_change = '0'

project = os.environ.get('BEV_PROJECT')
if not project:
    project = 'none'

if os.path.exists(log_path):
    st = os.stat(log_path)
    last_change = str(st.st_mtime)

now = str(datetime.now())
with open(log_path, 'a') as fh:

    cols = [cwd, cmd, last_change, project, now]
    record = '\t'.join(cols) 
    fh.write(record + '\n')
