# -*- coding: utf-8 -*-
import os
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION.txt'), 'rb') as f:
    __version__ = f.read().decode('ascii').strip()