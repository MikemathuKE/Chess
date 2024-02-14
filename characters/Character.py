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
    
    def get_id(self) -> int:
        return self.id
    
    def is_first_move(self) -> bool:
        return self.first_move
    
    def first_move_made(self) -> None:
        self.first_move = False
    
    def get_grid_position(self) -> tuple:
        return Position.interpret_position(self.position[0], self.position[1])
    
    def set_grid_position(self, _position: Position) -> None:
        self.grid_position = _position
        self.set_pixel_position()

    def get_direction_constraints(self) -> list:
        return self.direction_constraints
    
    def set_direction_constraints(self, _direction_constraints: list) -> None:
        self.direction_constraints = _direction_constraints

    def get_max_steps(self) -> int:
        return self.max_steps
    
    def set_max_steps(self, _max_steps: int) -> None:
        self.max_steps = _max_steps

    @abstractmethod
    def move(self, direction: str, steps: int) -> bool:
        pass

    def move_valid(self, direction: str, steps: int) -> bool:
        # print(self.max_steps, self.direction_constraints)
        if steps <= self.max_steps:
            if direction in self.direction_constraints:
                return True
        return False
    
    def get_piece_color(self) -> Color:
        return self.color_piece
    
    def is_inversed(self) -> bool:
        return self.color_piece == Color.BLACK

    def kill(self) -> None:
        self.alive = False

    def get_name(self) -> str:
        return self.name

    def revive(self, _position: Position) -> None:
        self.position = _position
        self.alive = True

    def get_direction_constraints(self) -> list:
        return self.direction_constraints

    def is_alive(self) -> bool:
        return self.alive
    
    def move(self, _position: tuple) -> bool:
        self.set_grid_position(Position(_position[0], _position[1]))
        if self.first_move:
            self.first_move_made()
    
    def __str__(self) -> str:
        return self.name
    
    def matches(self, other) -> bool:
        return self.name == other.get_name() and self.get_grid_position() == other.get_grid_position()