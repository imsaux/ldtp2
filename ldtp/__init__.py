'''
LDTP v2 client init file

@author: Eitan Isaacson <eitan@ascender.com>
@copyright: Copyright (c) 2009 Eitan Isaacson
@license: LGPL

http://ldtp.freedesktop.org

This file may be distributed and/or modified under the terms of the GNU General
Public License version 2 as published by the Free Software Foundation. This file
is distributed without any warranty; without even the implied warranty of 
merchantability or fitness for a particular purpose.

See "COPYING" in the source distribution for more information.

Headers in this file shall remain intact.
'''

import os
import state
import client
import atexit
import tempfile
from base64 import b64decode
from client_exception import LdtpExecutionError

def setHost(host):
    client._client.setHost(host)

def whoismyhost():
    return client._client._ServerProxy__host

def log(self, *args):
    # Do nothing. For backward compatability
    pass

def _populateNamespace(d):
    for method in client._client.system.listMethods():
        if method.startswith('system.'):
            continue
        if d.has_key(method):
            local_name = '_remote_' + method
        else:
            local_name = method
        d[local_name] = getattr(client._client, method)
        d[local_name].__doc__ = client._client.system.methodHelp(method)

def imagecapture(window_name = None, out_file = None, x = 0, y = 0,
                 width = None, height = None):
    if not out_file:
        out_file = tempfile.mktemp('.png', 'ldtp_')
    else:
        out_file = os.path.expanduser(out_file)
        
    data = _remote_imagecapture(window_name, x, y, width, height)
    f = open(out_file, 'w')
    f.write(b64decode(data))
    f.close()

    return out_file

_populateNamespace(globals())

atexit.register(client._client.kill_daemon)
