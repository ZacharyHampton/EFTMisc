import struct


class BaseObject:
    def __init__(self, base_object: bytes):
        self.previousObjectLink, self.nextObjectLink, self.obj = struct.unpack("QQQ", base_object)

