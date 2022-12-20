import struct


class GameObjectManager:
    def __init__(self, gom: bytes):
        self.LastTaggedNode, self.TaggedNodes, self.LastMainCameraTaggedNode, self.MainCameraTaggedNodes, self.LastActiveNode, self.ActiveNodes = struct.unpack("QQQQQQ", gom)