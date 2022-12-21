from offsets import Offsets
import objects
from game import game
import struct


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

    def SetShader(self, shaderPtr: int):
        materialShaderInstanceId = game.memory.read_ptr_chain(self.materialPtr, [0x38, 0x0])

        if shaderPtr:
            shaderInstancePtr = game.memory.read_ptr(shaderPtr + 0x8)
            shaderInstanceId = struct.pack("L", shaderInstancePtr)

            game.memory.write_value(materialShaderInstanceId, shaderInstanceId)
        else:
            game.memory.write_value(materialShaderInstanceId, struct.pack("L", 0))

        self.UpdateToNewShaders()

    def UnshareMaterialData(self):
        materialSharedMaterialData = game.memory.read_ptr(self.materialPtr + 0xB8)
        game.memory.write_value(materialSharedMaterialData, struct.pack("Q", 0))

    def GetWritableSharedMaterialData(self, dirtyFlags: int):
        self.UnshareMaterialData()
        result = game.memory.read_ptr(self.materialPtr + 0xB8)
        if dirtyFlags & 1:
            #: v_MaterialPtr->m_PerMaterialTextureDirty = 1;
            game.memory.write_value(result + 0xB0, struct.pack("?", 1))
        if dirtyFlags & 2:
            #: v_MaterialPtr->m_PerMaterialCBDirty = 1;
            game.memory.write_value(result + 0xB1, struct.pack("?", 1))

        return result

    def UpdateToNewShaders(self):
        v_EmptySharedMaterialData = self.GetWritableSharedMaterialData(3)
        v_tagMap = game.memory.read_ptr(v_EmptySharedMaterialData + 0x128)
