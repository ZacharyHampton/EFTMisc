import memprocfs
from offsets import Offsets
import struct
import memprocfs.vmmpyc


class Memory:
    def __init__(self, process: memprocfs.vmmpyc.VmmProcess):
        self.process = process

    def read_ptr(self, address: int):
        return int.from_bytes(self.read_value(address, struct.calcsize("LL")), 'little')

    def read_ptr_chain(self, pointer: int, offsets: list[int]):
        address: int = self.read_ptr(pointer + offsets[0])
        for offset in offsets[1:]:
            address = self.read_ptr(address + offset)

        return address

    def read_value(self, address: int, size: int):
        return self.process.memory.read(address, size, memprocfs.FLAG_NOCACHE)

    def read_str(self, address: int, size: int):
        return self.read_value(address, size).decode('utf-8', errors='ignore').split('\0')[0]

    def read_unity_string(self, address: int, size: int):
        return self.read_value(address, size * 2).decode('utf-8', errors='ignore').replace('\x00', '')

    def read_bool(self, address: int):
        try:
            return bool(self.read_value(address, 1)[0])
        except IndexError:
            return False

    def read_int(self, address: int):
        return int.from_bytes(self.read_value(address, struct.calcsize("L")), 'little')

    def read_float(self, address: int):
        return struct.unpack("f", self.read_value(address, struct.calcsize("f")))[0]

    def write_value(self, address: int, value: bytes):
        self.process.memory.write(address, value)

    def write_float(self, address: int, value: float):
        self.write_value(address, struct.pack("f", value))

    def _write_bool(self, address: int, value: bool):
        self.write_value(address, struct.pack("?", value))

    def ReadList(self, pointer: int) -> list:
        listInfo = self.read_ptr(pointer + Offsets['UnityDictionary']['Elements'])

        array = self.read_ptr(listInfo + Offsets['UnityList']['Base'])
        listCount = self.read_int(listInfo + Offsets['UnityList']['Count'])

        returnList = []

        for i in range(listCount):
            _ptr = self.read_ptr(array + Offsets['UnityListBase']['Start'] + (i * 0x8))
            if _ptr == 0x0:
                continue

            returnList.append(_ptr)

        return returnList

    def ReadArray(self, pointer: int):
        listCount = self.read_int(pointer + Offsets['UnityList']['Count'])

        returnList = []

        maxInt = 10

        for i in range(0, maxInt):
            _ptr = self.read_ptr(pointer + Offsets['UnityListBase']['Start'] + (i * 0x8))
            if _ptr == 0x0:
                continue

            returnList.append(_ptr)

        return returnList
