import sys
from game import game
import time


def main():
    while not (players := game.get_players()):
        print("Not in raid...")
        game.in_raid = False

        time.sleep(5)

    localPlayer = players.pop(0)
    localPlayer.enable_features()

    """for player in players:
        print(player.get_position())"""

    #: TODO: method for chams
    #: TODO: recreate Material::SetFloat function & set _ZTest to 8 every frame

    while True:
        q = input("Press enter to quit.")
        if q == "":
            break

    sys.exit(0)


if __name__ == '__main__':
    main()
