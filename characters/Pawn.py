from utils.utils import *
from characters.Character import *

class Pawn(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.direction_constraints = [
            Movement.FORWARD_LEFT,
            Movement.FORWARD_RIGHT,
            Movement.FORWARD,
        ]
        self.max_steps = 2

    def move(self, direction: str, steps: int) -> bool:
        if self.move_valid():
            pass