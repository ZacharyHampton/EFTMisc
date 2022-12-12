import memprocfs
import json
import os
from memory import Memory


def main():
    vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
    memory = Memory(vmm)

    print("abc")




if __name__ == '__main__':
    main()

