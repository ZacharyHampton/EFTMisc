import threading

import memprocfs
import time
from offsets import Offsets
import struct
from objects.game_object_manager import GameObjectManager
from objects.base_object import BaseObject
import memory


class GameManager:

    def __init__(self):
        #: Static
        self.vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
        self.process = self.get_game_process()
        self.pid: int = self.process.pid
        self._unity_base: int = self.get_module_base("UnityPlayer.dll")
        self.memory = memory.Memory(self.process)

        #: May change
        self.gom = self.get_gom()
        print('Found object game manager.')

        self.lgw_ptr = self.get_lgw()
        self.in_raid = False

        threading.Thread(target=self.in_raid_thread).start()

        time.sleep(2.5)

    def in_raid_thread(self):
        while True:
            time.sleep(1)

            playerCount = self.get_player_count()
            if playerCount < 1 or playerCount > 1024:
                if self.in_raid:
                    print("Left raid.")
                    self.in_raid = False
                    self.gom = self.get_gom()
                    self.lgw_ptr = self.get_lgw()

                    continue
                else:
                    self.in_raid = False
            else:
                self.in_raid = True

    def get_game_process(self):
        while True:
            print('Waiting for game process...')

            try:
                process = self.vmm.process("EscapeFromTarkov.exe")
                print('Found game process!')
                return process
            except RuntimeError:
                time.sleep(1)
                continue

    def get_module_base(self, module_name: str):
        base = self.process.module(module_name).base
        print(f"Found {module_name}; Base: {hex(base)}")
        return base

    def get_gom(self):
        address = self.memory.read_ptr(self._unity_base + Offsets['ModuleBase']['GameObjectManager'])
        gom = GameObjectManager(self.memory.read_value(address, struct.calcsize(
            "LLLLLL" * 2)))  #: ptr read and type cast (6 uints (48 bits))
        return gom

    def GetObjectFromList(self, activeObjectsPtr: int, lastObjectPtr: int, objectName: str):
        activeObject = BaseObject(
            self.memory.read_value(activeObjectsPtr, struct.calcsize("LLL" * 2)))  #: 24 bits
        lastObject = BaseObject(self.memory.read_value(lastObjectPtr, struct.calcsize("LLL" * 2)))

        if activeObject.obj != 0x0:
            while activeObject.obj != 0x0:
                objectNamePtr = self.memory.read_ptr(activeObject.obj + Offsets['GameObject']['ObjectName'])
                objectNameStr = self.memory.read_str(objectNamePtr, 64)

                if objectName.lower() in objectNameStr.lower():
                    print(f"Found {objectNameStr}; Base: {hex(activeObject.obj + Offsets['GameObject']['ObjectName'])}")
                    return activeObject.obj

                if activeObject.obj == lastObject.obj:
                    break

                try:
                    activeObject = BaseObject(
                        self.memory.read_value(activeObject.nextObjectLink, struct.calcsize("LLL" * 2)))
                except struct.error:
                    print("Error reading game list object.")
                    return None

        print(f"Could not find {objectName}")

    def GetObjectByInstanceId(self, activeObjectsPtr: int, lastObjectPtr: int, instanceId: int):
        activeObject = BaseObject(
            self.memory.read_value(activeObjectsPtr, struct.calcsize("LLL" * 2)))  #: 24 bits
        lastObject = BaseObject(self.memory.read_value(lastObjectPtr, struct.calcsize("LLL" * 2)))

        if activeObject.obj != 0x0:
            while activeObject.obj != 0x0:
                objectPtr = self.memory.read_ptr_chain(activeObject.obj, [Offsets['GameObject']['EditorExtension'], Offsets['EditorExtension']['Object']])
                objectInstanceId = self.memory.read_int(objectPtr + Offsets['Object']['m_InstanceID'])

                if objectInstanceId == instanceId:
                    objectNamePtr = self.memory.read_ptr(activeObject.obj + Offsets['GameObject']['ObjectName'])
                    objectNameStr = self.memory.read_str(objectNamePtr, 64)

                    print(f"Found {objectNameStr}; Base: {hex(activeObject.obj + Offsets['GameObject']['ObjectName'])}")
                    return activeObject.obj

                if activeObject.obj == lastObject.obj:
                    break

                try:
                    activeObject = BaseObject(
                        self.memory.read_value(activeObject.nextObjectLink, struct.calcsize("LLL" * 2)))
                except struct.error:
                    print("Error reading game list object.")
                    return None

        print(f"Could not find {instanceId}")

    def GetObjectsFromList(self, activeObjectsPtr: int, lastObjectPtr: int):
        activeObject = BaseObject(
            self.memory.read_value(activeObjectsPtr, struct.calcsize("LLL" * 2)))  #: 24 bits
        lastObject = BaseObject(self.memory.read_value(lastObjectPtr, struct.calcsize("LLL" * 2)))
        objectNames = []

        if activeObject.obj != 0x0:
            while activeObject.obj != 0x0:
                objectNamePtr = self.memory.read_ptr(activeObject.obj + Offsets['GameObject']['ObjectName'])
                objectNameStr = self.memory.read_str(objectNamePtr, 64)

                objectNames.append(objectNameStr)

                if activeObject.obj == lastObject.obj:
                    break

                try:
                    activeObject = BaseObject(
                        self.memory.read_value(activeObject.nextObjectLink, struct.calcsize("LLL" * 2)))
                except struct.error:
                    print("Error reading game list object.")
                    return []

        return objectNames

    def get_lgw(self):
        """Get LocalGameWorld"""

        activeNodes = self.memory.read_ptr(self.gom.ActiveNodes)
        lastActiveNode = self.memory.read_ptr(self.gom.LastActiveNode)
        while True:
            gameWorld = self.GetObjectFromList(activeNodes, lastActiveNode, "GameWorld")
            if gameWorld is not None:
                break

            self.gom = self.get_gom()
            time.sleep(1)

        return self.memory.read_ptr_chain(gameWorld, Offsets['GameWorld']['To_LocalGameWorld'])

    def GetObjectComponent(self, objectPointer: int, componentName: str):
        componentList = self.memory.read_ptr(objectPointer + 0x30)
        for i in range(0, 100):
            field = self.memory.read_ptr_chain(componentList, [0x8 + (i * 0x10), 0x28])
            object_name_pointer = self.memory.read_ptr_chain(field, [0x0, 0x0, 0x48])
            object_name = self.memory.read_str(object_name_pointer, 64)

            if componentName.lower() in object_name.lower():
                return field

        return None

    def GetComponentsFromObject(self, objectPointer: int):
        componentList = self.memory.read_ptr(objectPointer + 0x30)
        components = []
        for i in range(0, 100):
            field = self.memory.read_ptr_chain(componentList, [0x8 + (i * 0x10), 0x28])
            object_name_pointer = self.memory.read_ptr_chain(field, [0x0, 0x0, 0x48])
            object_name = self.memory.read_str(object_name_pointer, 64)

            if object_name:
                components.append(object_name)

        return components

    def GetFPSCamera(self):
        while True:
            fpsCamera = self.GetObjectFromList(self.gom.MainCameraTaggedNodes, self.gom.LastMainCameraTaggedNode,
                                               "FPS Camera")
            if fpsCamera is not None:
                break

            self.gom = self.get_gom()
            time.sleep(1)

        return fpsCamera

    def get_sky_material(self):
        fpsCamera = self.GetFPSCamera()
        scattering = self.GetObjectComponent(fpsCamera, "TOD_Scattering")
        return self.memory.read_ptr(scattering + Offsets['TOD_Scattering']['ScatteringMaterial'])

    def get_player_count(self):
        registeredPlayers = self.memory.read_ptr(self.lgw_ptr + Offsets['LocalGameWorld']['RegisteredPlayers'])
        playerCount = self.memory.read_int(registeredPlayers + Offsets['UnityList']['Count'])

        return playerCount

    def get_players(self, get_local_player: bool = False):
        from objects.player import Player
        from objects.local_player import LocalPlayer

        registeredPlayers = self.memory.read_ptr(self.lgw_ptr + Offsets['LocalGameWorld']['RegisteredPlayers'])
        listBase = self.memory.read_ptr(registeredPlayers + Offsets['UnityList']['Base'])
        playerCount = self.memory.read_int(registeredPlayers + Offsets['UnityList']['Count'])

        if playerCount < 1 or playerCount > 1024:
            #: raid done
            return None

        players = []
        for i in range(playerCount):
            playerBase = self.memory.read_ptr(listBase + Offsets['UnityListBase']['Start'] + (i * 0x8))
            if playerBase == 0x0:
                continue

            player = Player(playerPtr=playerBase)
            if player.isLocalPlayer:
                player = LocalPlayer(playerPtr=playerBase)
                if get_local_player:
                    return player

            players.append(player)

        return players
