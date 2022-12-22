import struct
from offsets import Offsets
import objects
from objects.vector2 import Vector2
from objects.vector3 import Vector3
from objects.lod import Lod
from objects.renderer import Renderer
from game import game


class Player:
    def __init__(self, playerPtr: int):
        self.pointer = playerPtr
        self.playerProfile = self.get_player_profile()

        self.uuid: str = self.get_player_id()
        self.name: str = ""
        self.health: int = 0
        self.isAlive: bool = False
        self.isLocalPlayer: bool = self.is_local_player()
        self.position: Vector3 = Vector3(0, 0, 0)
        self.rotation: Vector2 = Vector2(0, 0)

    def get_player_profile(self):
        return game.memory.read_ptr(self.pointer + Offsets['Player']['Profile'])

    def get_player_id(self):
        playerId = game.memory.read_ptr(self.playerProfile + Offsets['Profile']['Id'])
        playerIdLength = game.memory.read_int(playerId + Offsets['UnityString']['Length'])
        return game.memory.read_unity_string(playerId + Offsets['UnityString']['Value'], playerIdLength)

    def is_local_player(self):
        return game.memory.read_bool(self.pointer + Offsets['Player']['IsLocalPlayer'])

    def set_chams(self):
        self.set_skin_chams()

    def get_body(self):
        return game.memory.read_ptr(self.pointer + Offsets['Player']['Body'])

    def set_gear_chams(self):
        playerBody = self.get_body()
        if playerBody == 0x0:
            return

        slotViewsPtr = game.memory.read_ptr(playerBody + Offsets['PlayerBody']['SlotViews'])
        if slotViewsPtr == 0x0:
            return

        slots = game.memory.ReadList(slotViewsPtr)

        for slot in slots:
            dressesArray = game.memory.read_ptr(slot + Offsets['PlayerSlot']['Dresses'])
            if dressesArray == 0x0:
                continue

            dresses = game.memory.ReadArray(dressesArray)
            for dress in dresses:
                renderersArray = game.memory.read_ptr(dress + Offsets['Dress']['Renderers'])
                if renderersArray == 0x0:
                    continue

                renderers = game.memory.ReadArray(renderersArray)

                for renderer in renderers:
                    renderer = objects.renderer.Renderer(game.memory.read_ptr(renderer + 0x10))
                    renderer.write_null_renderer()

    def set_skin_chams(self):
        playerBody = self.get_body()
        playerSkinsDict = game.memory.read_ptr(playerBody + Offsets['PlayerBody']['BodySkins'])

        playerSkinsValues = game.memory.read_ptr(playerSkinsDict + Offsets['UnityDictionary']['Elements'])
        playerSkinsValuesCount = game.memory.read_int(playerSkinsDict + Offsets['UnityDictionary']['Count'])

        for i in range(playerSkinsValuesCount):
            skin = game.memory.read_ptr(
                playerSkinsValues + 0x30 + (i * 0x18))  #: Offsets['UnityListBase']['Start'] or 0x30?

            if skin == 0:
                continue

            abstractSkinList = game.memory.read_ptr(skin + Offsets['LoddedSkin']['_lods'])
            if abstractSkinList == 0:
                continue

            abstractSkinCount = game.memory.read_int(abstractSkinList + Offsets['UnityListBase']['Size'])

            for j in range(abstractSkinCount):
                abstractSkin = game.memory.read_ptr(abstractSkinList + Offsets['UnityListBase']['Start'] + (j * 0x8))

                if j == 1:
                    abstractSkin = game.memory.read_ptr(abstractSkinList + Offsets['UnityListBase']['Start'])

                lod = Lod(lodPtr=abstractSkin)

                skinnedMeshRenderer = lod.ReadSkinnedMeshRendererFromSkin()
                if skinnedMeshRenderer == 0x0:
                    continue

                renderer = Renderer(skinnedMeshRenderer)
                renderer.write_null_renderer()

    def get_position(self):
        bodyTransform = game.memory.read_ptr_chain(self.pointer, [0x580, 0x110])
        transform = game.memory.read_value(bodyTransform + 0x10, struct.calcsize('fff'))

        print(struct.unpack('fff', transform))

        return Vector3(0.0, 0.0, 0.0)
