from abc import ABC, abstractmethod
from utils.utils import *
import arcade

class Character(arcade.Sprite, ABC):

    def __init__(self, _position: Position, _color: Color, _texture: str) -> None:
        texture = "./assets/" + _texture
        super().__init__(texture)
        self.set_position(_position)
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
        self.first_move = True  
        self.max_steps = 7
        self.alive = True
        self.color_piece = _color

    def set_position(self, _position: Position) -> None:
        center_x, center_y = _position.get_center_pixel()
        return super().set_position(center_x, center_y)

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