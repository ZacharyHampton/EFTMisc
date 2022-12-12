import struct


class GameObjectManager:
    def __init__(self, gom: bytes):
        self.LastTaggedNode, self.TaggedNodes, self.LastMainCameraTaggedNode, self.MainCameraTaggedNodes, self.LastActiveNode, self.ActiveNodes = struct.unpack("QQQQQQ", gom)


class BaseObject:
    def __init__(self, base_object: bytes):
        self.previousObjectLink, self.nextObjectLink, self.obj = struct.unpack("QQQ", base_object)
