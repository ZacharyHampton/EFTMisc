Offsets = {
    'ModuleBase': {
        'GameObjectManager': 0x017FFD28,
        'PersistentManager': 0x0184BD18,
    },

    'UnityString': {
        'Length': 0x10,
        'Value': 0x14,
    },
    'UnityList': {
        'Base': 0x10,
        'Count': 0x18,
    },
    'UnityListBase': {
        'Size': 0x18,
        'Start': 0x20,  #: start of list + (i * 0x8)
    },
    'UnityDictionary': {
        'Elements': 0x18,  #: array(<KeyValuePair>)
        'Count': 0x40,
    },
    'KeyValuePair': {
        'Key': 0x8,
        'Value': 0x10,
    },
    'UnityObject': {
      'ObjectName': [0x0, 0x0, 0x48]
    },
    'GameObject': {
        'EditorExtension': 0x0,
        'ObjectClass': 0x30,
        'ObjectName': 0x60,
    },
    'EditorExtension': {
        'Object': 0x0,
    },
    'Object': {
        'm_InstanceID': 0x8,
    },
    'GameWorld': {
        'To_LocalGameWorld': [0x30, 0x18, 0x28],
    },
    'LocalGameWorld': {
        'RegisteredPlayers': 0xA0,
        'Grenades': 0x128,
        'ExfilController': 0x18
    },
    'Player': {
        'To_TransformInternal': [0xA8, 0x28, 0x28, 0x10, 0x20 + (0 * 0x8), 0x10],  #: 0xA8, 0x28, 0x28, Offsets.UnityList.Base, Offsets.UnityListBase.Start + (0 * 0x8), 0x10
        'MovementContext': 0x40,
        'Corpse': 0x338,
        'Profile': 0x520,
        'HealthController': 0x558,
        'InventoryController': 0x568,
        'IsLocalPlayer': 0x837,
        'ProceduralWeaponAnimation': 0x1A0,
        'Physical': 0x530,  #: GClass05ED
        'Body': 0xA8,
        'Bones': 0x580,
    },
    'Transform': {
        'LocalRotation': 0x48,
        'LocalPosition': 0x58,
    },
    'PlayerBody': {
        'BodySkins': 0x38,
        'SlotViews': 0x50,
        'Bones': 0x20
    },
    'PlayerBones': {
        'Neck': 0x38,  #: Transform
        'R_Neck': 0x1B8,
    },
    'BifacialTransform': {
        '_accumulatedPosition': 0xAC,
        '_accumulatedRotation': 0xB8,
    },
    'Vector3': {
        'X': 0x0,
        'Y': 0x4,
        'Z': 0x8,
    },
    'Profile': {
        'Id': 0x10,
        'AccountId': 0x18,
        'PlayerInfo': 0x28,  #: GClass1148
        'Stats': 0xF0,
    },
    'ProceduralWeaponAnimation': {
        'ShootingShotEffector': 0x48,
        'Breath': 0x28,
        'Walk': 0x30,
        'Motion': 0x38,
        'Force': 0x40,
        'Mask': 0x118
    },
    'ShotEffector': {
        'Intensity': 0x70,
    },
    'BreathEffector': {
        'Intensity': 0xA4,
        'isAiming': 0xA0
    },
    'WalkEffector': {
        'Intensity': 0x70
    },
    'MotionEffector': {
        'Intensity': 0xD0
    },
    'ForceEffector': {
        'Intensity': 0x28
    },
    'PlayerInfo': {
        'Nickname': 0x18,
        'MainProfileNickname': 0x26,
        'PlayerSide': 0x76,
    },
    'Physical': {
        'Stamina': 0x38
    },
    'PhysicalCurrent': {
        'Current': 0x48
    },
    'TOD_Scattering': {
        'TOD_Sky': 0x18,
        'ScatteringShader': 0x30,
        'ScatteringMaterial': 0x40
    },
    'TOD_Sky': {
        'Cycle': 0x18,
        'Components': 0x80
    },
    'TOD_Components': {
      'Time': 0x140,
    },
    'TOD_Time': {
        'GameDateTime': 0x18
    },
    'TOD_CycleParameters': {
        'Hour': 0x10,
    },
    'LoddedSkin': {
        '_lods': 0x18,
    },
    'AbstractSkin': {
        'Renderer': 0x20
    },
    'EFTVisualTorsoSkin': {
        '_skin': 0x20
    },
    'PlayerSlot': {  #: GClass148F
        'Dresses': 0x40
    },
    'Dress': {
        'Renderers': 0x28
    },
    'Material': {
        'SharedMaterialData': 0xB8,
    },
    'SharedMaterialData': {
        'Properties': 0x18,
    },
    'ShaderPropertySheet': {
        'm_Names': 0x30, #: dynamic_array<ShaderLab::FastPropertyName,0>
        'm_Descs': 0x50,  #: dynamic_array<unsigned int,0>
    },
    'SpriteShapeRenderer': {
        'm_Color': 0x1E0
    },
    'ColorRGBAf': {
        'R': 0x0,
        'G': 0x4,
        'B': 0x8,
        'A': 0xC,
    },
    'ThermalVision': {
        'Shader': 0x90,
        'On': 0xE0,
        'isNoisy': 0xE1,
        'isFpsStuck': 0xE2,
        'isMotionBlurred': 0xE3,
        'isGlitch': 0xE4,
        'isPixelated': 0xE5,
    },
    'VisorEffect': {
        'Intensity': 0xB8,
    },
    'NightVision': {
        'On': 0xE4,
        'Intensity': 0xC0,
        'NoiseIntensity': 0xC8,
    }
}
