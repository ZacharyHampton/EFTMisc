import threading
import time
import sys
import memprocfs
from memory import Memory


def main():
    vmm = memprocfs.Vmm(["-printf", "-v", "-device", "FPGA", "-memmap", "auto"])
    game = Memory(vmm)

    time.sleep(2.5)

    threading.Thread(target=game.playerLoop).start()

    while True:
        q = input("Press enter to quit.")
        if q == "":
            break

    sys.exit(0)


if __name__ == '__main__':
    main()

