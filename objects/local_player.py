import threading
import objects
from offsets import Offsets
import time
from game import game
import struct


class LocalPlayer(objects.player.Player):
    def __init__(self, playerPtr: int):
        super(LocalPlayer, self).__init__(playerPtr)
        self.featuresEnabled = False

    def no_recoil(self):
        while True:
            if not game.in_raid:
                self.featuresEnabled = False
                return

            shotEffector = game.memory.read_ptr_chain(self.pointer, [Offsets['Player']['ProceduralWeaponAnimation'], Offsets['ProceduralWeaponAnimation']['ShootingShotEffector']])
            intensity = game.memory.read_float(shotEffector + Offsets['ShotEffector']['Intensity'])

            if intensity != 0.0:
                game.memory.write_float(shotEffector + Offsets['ShotEffector']['Intensity'], 0.0)

            time.sleep(0.1)

    def no_sway(self):
        while True:
            if not game.in_raid:
                self.featuresEnabled = False
                return

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
                self.featuresEnabled = False
                return

            staminaData = game.memory.read_ptr_chain(self.pointer, [Offsets['Player']['Physical'], Offsets['Physical']['Stamina']])
            current = game.memory.read_float(staminaData + Offsets['PhysicalCurrent']['Current'])

            if current < 80:  #: todo: get max stamina
                game.memory.write_float(staminaData + Offsets['PhysicalCurrent']['Current'], 200.0)

            time.sleep(1)

    def extra_vision(self, nightVision=True, thermalVision=True):
        if not nightVision and not thermalVision:
            return

        fpsCamera = game.GetFPSCamera()
        thermalVisionPtr = game.GetObjectComponent(fpsCamera, 'ThermalVision')
        nightVisionPtr = game.GetObjectComponent(fpsCamera, 'NightVision')

        while True:
            if not game.in_raid:
                self.featuresEnabled = False
                return

            breathEffector = game.memory.read_ptr_chain(self.pointer, [Offsets['Player']['ProceduralWeaponAnimation'], Offsets['ProceduralWeaponAnimation']['Breath']])

            isAiming = game.memory.read_bool(breathEffector + Offsets['BreathEffector']['isAiming'])
            isOn = game.memory.read_bool(thermalVisionPtr + Offsets['ThermalVision']['On'])
            if isAiming:
                if isOn:
                    if thermalVision:
                        self.toggle_thermal_vision(thermalVisionPtr, False)

                    if nightVision:
                        self.toggle_night_vision(nightVisionPtr, True)

            else:
                if not isOn:
                    if thermalVision:
                        self.toggle_thermal_vision(thermalVisionPtr, True)

                    if nightVision:
                        self.toggle_night_vision(nightVisionPtr, False)

            time.sleep(0.2)

    @staticmethod
    def toggle_night_vision(component: int, turnOn: bool):
        if turnOn:
            game.memory.write_bool(component + Offsets['NightVision']['On'], True)
            game.memory.write_float(component + Offsets['NightVision']['Intensity'], 0.0)
            game.memory.write_float(component + Offsets['NightVision']['NoiseIntensity'], 0.0)
        else:
            game.memory.write_bool(component + Offsets['NightVision']['On'], False)\


    @staticmethod
    def toggle_thermal_vision(component: int, turnOn: bool):
        if turnOn:
            game.memory.write_bool(component + Offsets['ThermalVision']['On'], True)

            #: shader = game.memory.read_ptr_chain(component, [Offsets['ThermalVision']['Shader'], 0x10])
            #: print(game.memory.read_int(shader + 0x38))

            game.memory.write_bool(component + Offsets['ThermalVision']['isNoisy'], False)
            game.memory.write_bool(component + Offsets['ThermalVision']['isFpsStuck'], False)
            game.memory.write_bool(component + Offsets['ThermalVision']['isMotionBlurred'], False)
            game.memory.write_bool(component + Offsets['ThermalVision']['isGlitch'], False)
            game.memory.write_bool(component + Offsets['ThermalVision']['isPixelated'], False)
        else:
            game.memory.write_bool(component + Offsets['ThermalVision']['On'], False)

    def no_visor(self):
        visor = game.GetObjectComponent(game.GetFPSCamera(), 'VisorEffect')

        while True:
            if not game.in_raid:
                self.featuresEnabled = False
                return

            if game.memory.read_float(visor + Offsets['VisorEffect']['Intensity']) != 0.0:
                game.memory.write_float(visor + Offsets['VisorEffect']['Intensity'], 0.0)

            time.sleep(1)

    def always_day(self):
        fpsCamera = game.GetFPSCamera()
        scattering = game.GetObjectComponent(fpsCamera, "TOD_Scattering")
        sky = game.memory.read_ptr(scattering + Offsets['TOD_Scattering']['TOD_Sky'])

        while True:
            if not game.in_raid:
                self.featuresEnabled = False
                return

            gameDateTime = game.memory.read_ptr_chain(sky, [Offsets['TOD_Sky']['Components'], Offsets['TOD_Components']['Time']])
            if gameDateTime != 0x0:
                nullBytes = struct.pack('Q', 0)
                game.memory.write_value(gameDateTime + Offsets['TOD_Time']['GameDateTime'], nullBytes)

            cycle = game.memory.read_ptr(sky + Offsets['TOD_Sky']['Cycle'])
            hour = game.memory.read_float(cycle + Offsets['TOD_CycleParameters']['Hour'])
            if 6 <= hour <= 18:
                game.memory.write_float(cycle + Offsets['TOD_CycleParameters']['Hour'], 10.0)

            time.sleep(5)

            if 10 <= game.memory.read_float(cycle + Offsets['TOD_CycleParameters']['Hour']) <= 11:
                time.sleep(180)
            else:
                print('Failed to set time.')

    def enable_features(self):
        if self.featuresEnabled:
            return

        self.featuresEnabled = True

        threading.Thread(target=self.no_recoil).start()
        threading.Thread(target=self.no_sway).start()
        threading.Thread(target=self.infinite_stamina).start()
        threading.Thread(target=self.no_visor).start()
        threading.Thread(target=self.extra_vision, kwargs={'nightVision': False, 'thermalVision': True}).start()
        threading.Thread(target=self.always_day).start()
