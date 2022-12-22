import sys
from game import game
import time
import threading


def main_thread():
    foundLocalPlayer = False

    while True:
        players = game.get_players()
        if not players:
            print("Not in raid.")
            game.in_raid = False
            foundLocalPlayer = False
            time.sleep(5)
            continue

        if foundLocalPlayer is False:
            localPlayer = game.get_players(get_local_player=True)
            if localPlayer is None:
                print('Could not find localPlayer.')
                game.in_raid = False
                foundLocalPlayer = False

                time.sleep(5)
                continue

            print('Found localPlayer.')
            localPlayer.enable_features()
            foundLocalPlayer = True

        time.sleep(1)


def main():
    threading.Thread(target=main_thread).start()

    #: TODO: method for chams
    #: TODO: recreate Material::SetFloat function & set _ZTest to 8 every frame

    while True:
        q = input("Press enter to quit.")
        if q == "":
            break

    sys.exit(0)


if __name__ == '__main__':
    main()
