from utils.utils import *
from characters.Character import *

class Knight(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.direction_constraints = [
            Movement.NNE,
            Movement.NNW,
            Movement.NEE,
            Movement.NWW,
            Movement.SWW,
            Movement.SEE,
            Movement.SSW,
            Movement.SSE
        ]
        self.max_steps = 1

    def move(self, direction: str, steps: int) -> bool:
        if self.move_valid():
            pass