# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2003 Kevin Walchko
# see LICENSE for full details
##############################################

from importlib.metadata import version # type: ignore
from .udpsocket import SocketUDP
from .message import *
from .ip import *

__author__ = "Kevin Walchko"
__license__ = "MIT"
__version__ = version("ipcpy")
