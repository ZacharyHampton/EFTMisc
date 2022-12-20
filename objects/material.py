from offsets import Offsets
import objects
from game import game


class Material:
    def __init__(self, materialPtr: int):
        self.materialPtr = materialPtr

    def GetColor(self, propertyName: str):
        sharedMaterialDataPtr = game.memory.read_ptr(self.materialPtr + Offsets['Material']['SharedMaterialData'])
        materialPropertiesPtr = game.memory.read_ptr(
            sharedMaterialDataPtr + Offsets['SharedMaterialData']['Properties'])
        descriptions = game.memory.read_ptr(materialPropertiesPtr + Offsets['ShaderPropertySheet']['m_Descs'])

        for spritePtr in game.memory.ReadArray(descriptions):
            m_Color = game.memory.read_ptr(spritePtr + Offsets['SpriteShapeRenderer']['m_Color'])

            r = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['R'])
            g = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['G'])
            b = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['B'])
            a = game.memory.read_float(m_Color + Offsets['ColorRGBAf']['A'])

            print(objects.color_rgba_f.ColorRGBAf(r, g, b, a))
