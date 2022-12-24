import sys
from game import game
import time
import threading


def main_thread():
    foundLocalPlayer = False
    playersDict = {
        #: uuid: player
    }

    while True:
        players = game.get_players()
        if not players:
            print("Not in raid.")
            game.in_raid = False
            foundLocalPlayer = False
            playersDict = {}

            time.sleep(5)
            continue

        for player in players:
            if player.uuid == '':
                continue

            if not player.isLocalPlayer:
                if player.uuid not in playersDict:
                    playersDict[player.uuid] = player
                    print("Found player: " + player.uuid)

                    threading.Thread(target=player.set_chams).start()
                    #: player.set_chams()
                else:
                    if player.pointer != playersDict[player.uuid].pointer:
                        playersDict[player.uuid].pointer = player.pointer
                        print("Player pointer changed: " + player.uuid)
            else:
                if foundLocalPlayer is False:
                    print('Found localPlayer.')
                    player.enable_features()
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
