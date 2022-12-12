from dataclasses import dataclass
from objects.vector3 import Vector3
from objects.vector2 import Vector2


@dataclass
class Player:
    pointer: int
    uuid: str
    name: str
    health: int
    isAlive: bool
    position: Vector3
    rotation: Vector2
