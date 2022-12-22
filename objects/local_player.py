import threading
import objects
from offsets import Offsets
import time
from game import game


class LocalPlayer(objects.player.Player):
    def __init__(self, playerPtr: int):
        super(LocalPlayer, self).__init__(playerPtr)
        self.featuresEnabled = False

    def no_recoil(self):
        while True:
            if not game.in_raid:
                time.sleep(1)
                continue

            shotEffector = game.memory.read_ptr_chain(self.pointer, [Offsets['Player']['ProceduralWeaponAnimation'], Offsets['ProceduralWeaponAnimation']['ShootingShotEffector']])
            intensity = game.memory.read_float(shotEffector + Offsets['ShotEffector']['Intensity'])

            if intensity != 0.0:
                game.memory.write_float(shotEffector + Offsets['ShotEffector']['Intensity'], 0.0)

            time.sleep(0.1)

    def no_sway(self):
        while True:
            if not game.in_raid:
                time.sleep(1)
                continue

            proceduralWeaponAnimation = game.memory.read_ptr(self.pointer + Offsets['Player']['ProceduralWeaponAnimation'])

            breathEffector = game.memory.read_ptr(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Breath'])
            if game.memory.read_bool(breathEffector + Offsets['BreathEffector']['isAiming']) is False:
                mask = game.memory.read_int(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Mask'])
                if mask != 0:
                    game.memory.write_int(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Mask'], 0)
            else:
                walkEffector = game.memory.read_ptr(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Walk'])
                motionEffector = game.memory.read_ptr(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Motion'])
                forceEffector = game.memory.read_ptr(proceduralWeaponAnimation + Offsets['ProceduralWeaponAnimation']['Force'])

                BreathIntensity = game.memory.read_float(breathEffector + Offsets['BreathEffector']['Intensity'])
                WalkIntensity = game.memory.read_float(walkEffector + Offsets['WalkEffector']['Intensity'])
                MotionIntensity = game.memory.read_float(motionEffector + Offsets['MotionEffector']['Intensity'])
                ForceIntensity = game.memory.read_float(forceEffector + Offsets['ForceEffector']['Intensity'])

                if any([True for i in [BreathIntensity, WalkIntensity, MotionIntensity, ForceIntensity] if i != 0.0]):
                    game.memory.write_float(breathEffector + Offsets['BreathEffector']['Intensity'], 0.0)
                    game.memory.write_float(walkEffector + Offsets['WalkEffector']['Intensity'], 0.0)
                    game.memory.write_float(motionEffector + Offsets['MotionEffector']['Intensity'], 0.0)
                    game.memory.write_float(forceEffector + Offsets['ForceEffector']['Intensity'], 0.0)

            time.sleep(1)

    def infinite_stamina(self):
        while True:
            if not game.in_raid:
                time.sleep(1)
                continue

            staminaData = game.memory.read_ptr_chain(self.pointer, [Offsets['Player']['Physical'], Offsets['Physical']['Stamina']])
            current = game.memory.read_float(staminaData + Offsets['PhysicalCurrent']['Current'])

            if current < 107.0 / 2:  #: todo: get max stamina
                game.memory.write_float(staminaData + Offsets['PhysicalCurrent']['Current'], 107.0)

            time.sleep(1)

    def enable_features(self):
        self.featuresEnabled = True

        threading.Thread(target=self.no_recoil).start()
        threading.Thread(target=self.no_sway).start()
        threading.Thread(target=self.infinite_stamina).start()
