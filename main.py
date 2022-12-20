import sys
from game import game
import time


def main():
    while not (players := game.get_players()):
        print("Not in raid...")
        time.sleep(1)

    localPlayer = players[0]
    localPlayer.enable_features()

    while True:
        q = input("Press enter to quit.")
        if q == "":
            break

    sys.exit(0)


if __name__ == '__main__':
    main()

