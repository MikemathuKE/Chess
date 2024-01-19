from abc import ABC, abstractmethod
from utils.utils import *

class Character(ABC):

    @abstractmethod
    def __init__(self, _position: Position, _color: Color, _texture: str) -> None:
        self.direction_constraints = [
            Movement.FORWARD,
            Movement.BACKWARD,
            Movement.LEFT,
            Movement.RIGHT,
            Movement.FORWARD_LEFT,
            Movement.FORWARD_RIGHT,
            Movement.BACKWARD_LEFT,
            Movement.BACKWARD_RIGHT
        ]
        self.position = _position
        self.texture = _texture
        self.first_move = True
        self.color = _color
        self.max_steps = 7
        self.alive = True

    @abstractmethod
    def move(self, direction: str, steps: int) -> bool:
        pass

    def move_valid(self, direction: str, steps: int) -> bool:
        if steps < self.max_steps:
            if direction in self.direction_constraints:
                return True
        return False

    def kill(self) -> None:
        self.alive = False

    def revive(self, _position: Position) -> None:
        self.position = _position
        self.alive = True

    def is_alive(self) -> bool:
        return self.alive