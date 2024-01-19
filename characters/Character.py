from abc import ABC, abstractmethod
from utils.utils import Position

class Character(ABC):

    @abstractmethod
    def __init__(self, _position: Position) -> None:
        self.position = _position
        self.alive = True

    @abstractmethod
    def move(self, direction: str, steps: int) -> bool:
        pass

    def position(self) -> Position:
        return self.position

    def kill(self) -> None:
        self.alive = False

    def revive(self, _position: Position) -> None:
        self.position = _position
        self.alive = True

    def is_alive(self) -> bool:
        return self.alive