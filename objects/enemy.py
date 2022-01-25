import pygame
from objects import BaseObject


class Enemy(BaseObject):
    def __init__(self, loc: dict, image: pygame.Surface) -> None:
        super().__init__(loc, image)
        self.vel = 4

    def move(self):
        self.loc["y"] += self.vel
