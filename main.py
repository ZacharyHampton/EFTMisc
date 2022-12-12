import memprocfs
import json
import os
from memory import Memory


def main():
    vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
    game = Memory(vmm)
    game.get_players()

    print("abc")




if __name__ == '__main__':
    main()

