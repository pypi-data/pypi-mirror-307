# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2003 Kevin Walchko
# see LICENSE for full details
##############################################
from enum import IntEnum
import struct

IPC_HEADER_SIZE = 7

class IpcState(IntEnum):
  IPC_MAGIC1 = 1
  IPC_MAGIC2 = 2
  IPC_ID1 = 3
  IPC_ID2 = 4
  IPC_SIZE1 = 5
  IPC_SIZE2 = 6
  IPC_CRC = 7
  IPC_PAYLOAD = 8

def calc_crc(buffer):
    cs = 0
    for b in buffer:
        cs ^= b
    return cs & 0x000000FF

# def get_id(buffer):
#     # get the message id
#     return (buffer[3] << 8) | buffer[2]

def get_msg(buffer):
    # search a buffer and return the message payload and
    # message ID
    state = IpcState.IPC_MAGIC1
    size = 0
    crc = 0
    cnt = 0
    id = 0

    for b in buffer:
        if state == IpcState.IPC_MAGIC1:
            if b == 0xff: state = IpcState.IPC_MAGIC2
        elif state == IpcState.IPC_MAGIC2:
            if b == 0xff: state = IpcState.IPC_ID1
            else: state = IpcState.IPC_MAGIC1
        elif state == IpcState.IPC_ID1:
            id = b
            state = IpcState.IPC_ID2
        elif state == IpcState.IPC_ID2:
            id += (b << 8)
            state = IpcState.IPC_SIZE1
        elif state == IpcState.IPC_SIZE1:
            size = b
            state = IpcState.IPC_SIZE2
        elif state == IpcState.IPC_SIZE2:
            size += (b << 8)
            state = IpcState.IPC_CRC
        elif state == IpcState.IPC_CRC:
            crc = b
            state = IpcState.IPC_PAYLOAD
        elif state == IpcState.IPC_PAYLOAD:
            msg = buffer[cnt:cnt+size-IPC_HEADER_SIZE]
            # crc2 = calc_crc(msg, size-IPC_HEADER_SIZE)
            crc2 = calc_crc(msg)
            if (crc == crc2):
                return (id, msg)
            state = IpcState.IPC_MAGIC1; # crap, start over
        cnt += 1

    return None, None



class MsgLibrary:
    HEADER_FMT = "<BBHH"
    hdr = struct.Struct("<BBHH")
    msgs = {}
    def __init__(self, msg_map):
        """
        msg_map is a dict(msg_id, (msg_format_string, msg_class))
        """
        for key, (val, mtype) in msg_map.items():
            self.msgs[key] = {"struct": struct.Struct(val), "mtype": mtype}

    def unpack(self, msg_id, bytes):
        struct = self.msgs[msg_id]["struct"]
        mtype = self.msgs[msg_id]["mtype"]
        ret = struct.unpack(bytes)
        try: # should handle classes w/individual args
            ret = mtype(*ret)
        except TypeError: # should handle list/tuple w/array arg
            ret = mtype(ret)
        return ret

    def pack(self, msg_id, data):
        struct = self.msgs[msg_id]["struct"]
        size = struct.size
        # print(f"size: {size}")
        hdr = [0xff,0xff,msg_id,IPC_HEADER_SIZE + size]
        hdr = self.hdr.pack(*hdr)
        # print(f"hdr: {hdr}")
        payload = struct.pack(*data)
        crc = calc_crc(payload)
        pkt = hdr + crc.to_bytes(1) + payload
        # print(f"pkt: {pkt}")
        return pkt

    def get_size(self, msg_id):
        return self.msgs[msg_id]["struct"].size + IPC_HEADER_SIZE