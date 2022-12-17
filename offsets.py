Offsets = {
    'ModuleBase': {
        'GameObjectManager': 0x017FFD28,
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
        'Start': 0x20,  #: start of list + (i * 0x8)
    },

    'GameObject': {
        'ObjectClass': 0x30,
        'ObjectName': 0x60,
    },
    'GameWorld': {
        'To_LocalGameWorld': [0x30, 0x18, 0x28],
    },
    'LocalGameWorld': {
        'RegisteredPlayers': 0x90,
        'Grenades': 0x108,
        'ExfilController': 0x18
    },
    'Player': {
        'To_TransformInternal': [0xA8, 0x28, 0x28, 0x10, 0x20 + (0 * 0x8), 0x10],  #: 0xA8, 0x28, 0x28, Offsets.UnityList.Base, Offsets.UnityListBase.Start + (0 * 0x8), 0x10
        'MovementContext': 0x40,
        'Corpse': 0x338,
        'Profile': 0x4E8,
        'HealthController': 0x520,
        'InventoryController': 0x530,
        'IsLocalPlayer': 0x7FF,
        'ProceduralWeaponAnimation': 0x198,
    },
    'Profile': {
        'Id': 0x10,
        'AccountId': 0x18,
        'PlayerInfo': 0x28,  #: GClass1148
        'Stats': 0xE8,
    },
    'ProceduralWeaponAnimation': {
        'ShootingShotEffector': 0x48
    },
    'ShotEffector': {
        'Intensity': 0x70
    },
    'PlayerInfo': {
        'Nickname': 0x10,
        'MainProfileNickname': 0x18,
        'PlayerSide': 0x68,
    }
}
