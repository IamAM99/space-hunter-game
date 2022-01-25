import pygame
from objects import BaseObject


class Player(BaseObject):
    def __init__(self, resolution: tuple, image: pygame.Surface) -> None:
        loc = dict(
            x=(resolution[0] - image.get_width()) // 2,
            y=resolution[1] + image.get_height() + 5,
        )
        super().__init__(loc, image)
        self.vel = 8
