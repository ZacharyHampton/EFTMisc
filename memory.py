import threading

import memprocfs
import time
from structs import GameObjectManager, BaseObject
from offsets import Offsets
import struct


class Memory:
    def __init__(self, vmm: memprocfs.Vmm):
        self.vmm: memprocfs.Vmm = vmm
        self.process = self.get_game_process()
        self.pid: int = self.process.pid
        self._unity_base: int = self.get_module_base("UnityPlayer.dll")
        self.gom = self.get_gom()
        self.lgw_ptr = self.get_lgw()

        self.localPlayer: int = 0

        self.runningFeatureThreads = False

        self.player_count = 0

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

    def reset_process(self):
        self.process = self.get_game_process()
        self.pid: int = self.process.pid
        self._unity_base: int = self.get_module_base("UnityPlayer.dll")
        self.gom = self.get_gom()
        self.lgw_ptr = self.get_lgw()

    def _read_ptr(self, address: int):
        return int.from_bytes(self._read_value(address, struct.calcsize("LL")), 'little')

    def _read_ptr_chain(self, pointer: int, offsets: list[int]):
        address: int = self._read_ptr(pointer + offsets[0])
        for offset in offsets[1:]:
            address = self._read_ptr(address + offset)

        return address

    def _read_value(self, address: int, size: int):
        return self.process.memory.read(address, size, memprocfs.FLAG_NOCACHE)

    def _read_str(self, address: int, size: int):
        return self._read_value(address, size).decode('utf-8', errors='ignore').split('\0')[0]

    def _read_unity_string(self, address: int, size: int):
        return self._read_value(address, size * 2).decode('utf-8', errors='ignore').replace('\x00', '')

    def _read_bool(self, address: int):
        return bool(self._read_value(address, 1)[0])

    def _write_value(self, address: int, value: bytes):
        self.process.memory.write(address, value)

    def _write_float(self, address: int, value: float):
        self._write_value(address, struct.pack("f", value))

    def _write_bool(self, address: int, value: bool):
        self._write_value(address, struct.pack("?", value))

    def get_gom(self):
        address = self._read_ptr(self._unity_base + Offsets['ModuleBase']['GameObjectManager'])
        gom = GameObjectManager(
            self._read_value(address, struct.calcsize("LLLLLL" * 2)))  #: ptr read and type cast (6 uints (48 bits))
        print(f"Found GOM; Base: {hex(address)}")
        return gom

    def _GetObjectFromList(self, activeObjectsPtr: int, lastObjectPtr: int, objectName: str):
        activeObject = BaseObject(self._read_value(activeObjectsPtr, struct.calcsize("LLL" * 2)))  #: 24 bits
        lastObject = BaseObject(self._read_value(lastObjectPtr, struct.calcsize("LLL" * 2)))

        if activeObject.obj != 0x0:
            while activeObject.obj != 0x0 and activeObject.obj != lastObject.obj:
                objectNamePtr = self._read_ptr(activeObject.obj + Offsets['GameObject']['ObjectName'])
                objectNameStr = self._read_str(objectNamePtr, 64)
                if objectName.lower() in objectNameStr.lower():
                    print(f"Found {objectNameStr}; Base: {hex(activeObject.obj + Offsets['GameObject']['ObjectName'])}")
                    return activeObject.obj

                try:
                    activeObject = BaseObject(self._read_value(activeObject.nextObjectLink, struct.calcsize("LLL" * 2)))
                except struct.error:
                    print("Error reading game list object.")
                    return None

        print(f"Could not find {objectName}")

    def get_lgw(self):
        """Get LocalGameWorld"""

        activeNodes = self._read_ptr(self.gom.ActiveNodes)
        lastActiveNode = self._read_ptr(self.gom.LastActiveNode)
        while True:
            gameWorld = self._GetObjectFromList(activeNodes, lastActiveNode, "GameWorld")
            if gameWorld is not None:
                break

            self.gom = self.get_gom()
            time.sleep(1)

        return self._read_ptr_chain(gameWorld, Offsets['GameWorld']['To_LocalGameWorld'])

    def get_players(self):
        registeredPlayers = self._read_ptr(self.lgw_ptr + Offsets['LocalGameWorld']['RegisteredPlayers'])
        listBase = self._read_ptr(registeredPlayers + Offsets['UnityList']['Base'])
        self.player_count = int.from_bytes(self._read_value(registeredPlayers + Offsets['UnityList']['Count'], 4),
                                           'little')

        if self.player_count < 1 or self.player_count > 1024:
            #: raid done
            return None

        for i in range(self.player_count):
            playerBase = self._read_ptr(listBase + Offsets['UnityListBase']['Start'] + (i * 0x8))
            playerProfile = self._read_ptr(playerBase + Offsets['Player']['Profile'])

            playerId = self._read_ptr(playerProfile + Offsets['Profile']['Id'])
            playerIdLength = int.from_bytes(self._read_value(playerId + Offsets['UnityString']['Length'], 4), 'little')
            playerIdStr = self._read_unity_string(playerId + Offsets['UnityString']['Value'], playerIdLength)

            isLocalPlayer = self._read_bool(playerBase + Offsets['Player']['IsLocalPlayer'])
            if isLocalPlayer:
                self.localPlayer = playerBase

            if isLocalPlayer and not self.runningFeatureThreads:
                threading.Thread(target=self.no_recoil).start()
                threading.Thread(target=self.no_sway).start()
                threading.Thread(target=self.infinite_stamina).start()

                self.runningFeatureThreads = True

            print(hex(playerId), playerIdStr, isLocalPlayer)

    def no_recoil(self):
        while True:
            shotEffector = self._read_ptr_chain(self.localPlayer, [Offsets['Player']['ProceduralWeaponAnimation'], Offsets['ProceduralWeaponAnimation']['ShootingShotEffector']])
            intensity = self._read_value(shotEffector + Offsets['ShotEffector']['Intensity'], 4)
            intensity = struct.unpack('f', intensity)[0]

            if intensity != 0.0:
                self._write_float(shotEffector + Offsets['ShotEffector']['Intensity'], 0.0)

            time.sleep(0.1)

    def no_sway(self):
        while True:
            breathEffector = self._read_ptr_chain(self.localPlayer, [Offsets['Player']['ProceduralWeaponAnimation'], Offsets['ProceduralWeaponAnimation']['Breath']])
            intensity = self._read_value(breathEffector + Offsets['BreathEffector']['Intensity'], 4)
            intensity = struct.unpack('f', intensity)[0]

            if intensity != 0.0:
                self._write_float(breathEffector + Offsets['BreathEffector']['Intensity'], 0.0)

            time.sleep(0.1)

    def infinite_stamina(self):
        while True:
            staminaData = self._read_ptr_chain(self.localPlayer, [Offsets['Player']['Physical'], Offsets['Physical']['Stamina']])
            current = self._read_value(staminaData + Offsets['PhysicalCurrent']['Current'], 4)
            current = struct.unpack('f', current)[0]

            if current < 107.0 / 2:
                self._write_float(staminaData + Offsets['PhysicalCurrent']['Current'], 107.0)

            time.sleep(1)
