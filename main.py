import time
import sys
import memprocfs
from memory import Memory


def main():
    vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
    game = Memory(vmm)

    time.sleep(2.5)

    game.get_players()

    input("Press enter to quit.")
    sys.exit(0)


if __name__ == '__main__':
    main()

