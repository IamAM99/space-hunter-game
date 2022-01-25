import pygame
from objects import BaseObject


class Projectile(BaseObject):
    def __init__(self, player, side: str, image: pygame.Surface) -> None:
        loc = self._calculate_location(player, side)
        super().__init__(loc, image)
        self.vel = 15

    @staticmethod
    def _calculate_location(player, side: str) -> dict:
        if side == "right":
            x_multiplier = 3.2
        elif side == "left":
            x_multiplier = 0
        else:
            raise ValueError("Wrong 'side' parameter.")

        loc = dict(
            x=player.loc["x"] + x_multiplier * player.size["w"] // 4,
            y=player.loc["y"] + player.size["h"] // 3,
        )
        return loc

    def move(self) -> None:
        self.loc["y"] -= self.vel
