import pygame
from objects import BaseObject


class Player(BaseObject):
    def __init__(self, loc: dict, image: pygame.Surface) -> None:
        super().__init__(loc, image)
        self.vel = 8
