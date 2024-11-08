#!/usr/bin/env python
# -*- coding:utf-8 -*-
__version__ = "1.5.4"


from . import connections, offline
Connect = connect = Connection =connections.Connection
offline = offline.Offline
__all__ = [
    "Connect",
    "Connection",
    "connect",
    "offline",
    "__version__",
]