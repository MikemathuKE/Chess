from utils.utils import *
from characters.Character import *

class Queen(Character):

    def __init__(self, position: Position, color: Color, texture: str) -> None:
        super().__init__(position, color, texture)
        self.id = int(Pieces.QUEEN) & int(color)