from utils.utils import *
from characters.Character import *

class King(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.set_max_steps(1)

    def move(self, direction: str, steps: int) -> bool:
        if self.move_valid():
            pass