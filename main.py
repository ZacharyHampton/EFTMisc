import time

import memprocfs
import json
import os
from memory import Memory


def main():
    vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
    game = Memory(vmm)

    time.sleep(2.5)

    game.get_players()

    input("Press enter to quit.")


if __name__ == '__main__':
    main()

