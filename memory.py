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
        self.lgw = self.get_lgw()

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

    def _read_ptr(self, address: int):
        return int.from_bytes(self._read_value(address, struct.calcsize("LL")), 'little')

    def _read_value(self, address: int, size: int):
        return self.process.memory.read(address, size, memprocfs.FLAG_NOCACHE)

    def _read_str(self, address: int, size: int):
        return self._read_value(address, size).decode('utf-8', errors='ignore').split('\0')[0]

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
                    print(f"Found {objectName}; Base: {hex(activeObject.obj + Offsets['GameObject']['ObjectName'])}")
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
        while gameWorld := self._GetObjectFromList(activeNodes, lastActiveNode, "GameWorld") is None:
            self.gom = self.get_gom()
            time.sleep(1)

        print(gameWorld)
