# coding: utf-8

import os
from burglar import Burglar

rootdir = os.path.abspath(os.path.dirname(__file__))
public = os.path.join(rootdir, 'public')

site = Burglar(public)
