from utils.utils import *
from characters.Character import *

class Rook(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.set_direction_constraints([
            Movement.FORWARD,
            Movement.BACKWARD,
            Movement.LEFT,
            Movement.RIGHT
        ])

    def move(self, direction: str, steps: int) -> bool:
        if self.move_valid():
            pass