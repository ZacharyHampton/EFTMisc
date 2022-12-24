from game import game
import struct


class Renderer:
    def __init__(self, rendererPtr: int):
        self.rendererPtr = rendererPtr

    def write_null_renderer(self):
        maxMaterialCount = 2

        materialCount = game.memory.read_int(self.rendererPtr + 0x158)
        if materialCount <= 0 or materialCount > maxMaterialCount:
            return None

        materialDictBase = game.memory.read_ptr(self.rendererPtr + 0x148)
        nullValue = 0
        for p in range(materialCount):
            materialInstancePtr = materialDictBase + (p * 0x50)  #: offset doesn't matter

            #: materialInstanceId = game.memory.read_int(materialInstancePtr)

            if game.memory.read_int(materialInstancePtr) != 0x0:
                game.memory.write_value(materialInstancePtr, struct.pack("L", nullValue))
                return game.memory.read_int(materialInstancePtr) == 0
