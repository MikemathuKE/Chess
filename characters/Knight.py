from utils.utils import *
from characters.Character import *

class Knight(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.set_direction_constraints([
            Movement.NNE,
            Movement.NNW,
            Movement.NEE,
            Movement.NWW,
            Movement.SWW,
            Movement.SEE,
            Movement.SSW,
            Movement.SSE
        ])
        self.set_max_steps(1)