from abc import ABC, abstractmethod
from utils.utils import *
import arcade

class Character(arcade.Sprite, ABC):

    def __init__(self, _position: Position, _color: Color, _texture: str) -> None:
        texture = "./assets/" + _texture
        super().__init__(texture)
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
        self.name = _texture.split(".")[0]
        self.grid_position = _position
        self.set_pixel_position()

    def set_pixel_position(self) -> None:
        center_x, center_y = self.grid_position.get_center_pixel()
        return super().set_position(center_x, center_y)
    
    def get_grid_position(self) -> Position:
        return Position.interpret_position(self.position[0], self.position[1])
    
    def set_grid_position(self, _position: Position) -> None:
        self.grid_position = _position
        self.set_pixel_position()

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
    
    def __str__(self) -> str:
        return self.name