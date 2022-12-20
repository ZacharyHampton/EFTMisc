from offsets import Offsets
from game import game


class Lod:
    def __init__(self, lodPtr: int):
        super(Lod, self).__init__()

        self.lodPtr = lodPtr

    def ReadSkinnedMeshRendererFromSkin(self):
        className = game.memory.read_str(game.memory.read_ptr_chain(self.lodPtr, Offsets['UnityObject']['ObjectName']), 64)

        if className == "Skin":
            return game.memory.read_ptr_chain(self.lodPtr, [Offsets['AbstractSkin']['Renderer'], 0x10])
        elif className == "TorsoSkin":
            return game.memory.read_ptr_chain(self.lodPtr, [Offsets['EFTVisualTorsoSkin']['_skin'], Offsets['AbstractSkin']['Renderer'], 0x10])

        return 0
