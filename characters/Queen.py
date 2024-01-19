from utils.utils import *
from Character import *

class Queen(Character):

    def __init__(self, _position: Position) -> None:
        super().__init__(_position)
        self.movt_constraints = [Movement.VERTICAL, Movement.HORIZONTAL, Movement.DIAGONAL]
        self.step_constraints = Movement.MULTIPLE

    def move(self, direction: str, steps: int) -> bool:
        if Movement.is_valid(self.movt_constraints, direction):
            pass
        else:
            return False