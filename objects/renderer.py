import objects
from game import game
from objects.material import Material


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

            """if self._read_int(address) != 0x0:
                self._write_value(address, struct.pack("L", nullValue))
                return self._read_int(address) == 0"""

            material = Material(materialPtr=materialPtr)
            name = material.GetColors()
            return True
