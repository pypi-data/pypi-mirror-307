# Inter-Process Communications (IPC)
![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/ipc)
[![Latest Version](https://img.shields.io/pypi/v/ipcpy.svg)](https://pypi.python.org/pypi/ipcpy/)
[![image](https://img.shields.io/pypi/pyversions/ipcpy.svg)](https://pypi.python.org/pypi/ipcpy)
[![image](https://img.shields.io/pypi/format/ipcpy.svg)](https://pypi.python.org/pypi/ipcpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ipcpy?color=aqua)


A simple library to allow processes to use UDP to communicate
with each other.

This is yet again another rehash of old work in a new way ... I keep
reinventing the wheel. :)

**in development**

## Example

``` python
import ipcpy as ipc
from collections import namedtuple

Msg = namedtuple("Msg","a b c")

d = {
    22: ("i", int),
    23: ("iii", Msg),
}

msglib = MsgLibrary(d)
run = True

def client():
    global run
    print("Client started")
    s = ipc.SocketUDP()
    s.open(TIMEOUT)

    for i in range(10):
        pkt = msglib.pack(MSG_ID_INT, [i])
        print(f"send: {pkt}")
        s.sendto(pkt, (HOST,PORT))
        time.sleep(0.25)
        # print('.')

    run = False

def server():
    global run
    print("Client started")
    s = ipc.SocketUDP()
    s.bind(HOST,PORT,TIMEOUT)

    while run:
        data, address = s.recvfrom(MSG_SIZE)
        if data is not None:
            id, info = ipc.get_msg(data)
            if id is not None:
                msg = msglib.unpack(id, info)
                print(f"recvfrom: {address} {info} {msg}")
            else:
                print(f"ERROR: {info}")

```

# MIT License

**Copyright (c) 2003 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
