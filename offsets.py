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
}
