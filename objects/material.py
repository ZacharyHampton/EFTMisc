from offsets import Offsets
import objects
from game import game


class Material:
    def __init__(self, materialPtr: int):
        self.materialPtr = materialPtr

    def GetColors(self):
        sharedMaterialDataPtr = game.memory.read_ptr(self.materialPtr + Offsets['Material']['SharedMaterialData'])
        materialPropertiesPtr = game.memory.read_ptr(sharedMaterialDataPtr + Offsets['SharedMaterialData']['Properties'])
        descriptions = game.memory.read_ptr_chain(materialPropertiesPtr, [0x0, Offsets['ShaderPropertySheet']['m_Descs']])

        if descriptions == 0x0:
            return None

        for spritePtr in game.memory.ReadArray(descriptions):
            m_Color = game.memory.read_ptr(spritePtr + Offsets['SpriteShapeRenderer']['m_Color'])

            if m_Color == 0x0:
                continue

            r = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['R'])
            g = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['G'])
            b = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['B'])
            a = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['A'])

            print(objects.color_rgba_f.ColorRGBAf(r, g, b, a))
