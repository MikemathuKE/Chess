from utils.utils import *
from characters.Character import *

class Queen(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)

    def move(self, _position: tuple, direction: str, steps: int) -> bool:
        self.set_grid_position(Position(_position[0], _position[1]))
        return True