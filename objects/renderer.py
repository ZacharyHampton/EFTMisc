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
            materialPtr = materialDictBase + (p * 0x50)

            if game.memory.read_int(materialPtr) != 0x0:
                game.memory.write_value(materialPtr, struct.pack("L", nullValue))
                return game.memory.read_int(materialPtr) == 0
