# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT_DIR)
VENDOR = os.path.join(ROOT, 'vendor')

# Add the vendored libraries to `sys.path` so that we can import isort
sys.path.insert(0, VENDOR)
sys.path.insert(0, os.path.join(VENDOR, 'isort'))
sys.path.insert(0, os.path.join(VENDOR, 'natsort'))
sys.path.insert(0, os.path.join(VENDOR, 'pies'))

from isort.main import main  # isort:skip

# Remove the paths we just added to `sys.path` so that they don't
# interfere with other Sublime Text packages.
sys.path.pop(0)
sys.path.pop(0)
sys.path.pop(0)
sys.path.pop(0)

if __name__ == '__main__':
    main()
