import pygame
from objects import BaseObject
from .projectile import Projectile


class Player(BaseObject):
    def __init__(self, resolution: tuple, image: pygame.Surface) -> None:
        loc = dict(
            x=(resolution[0] - image.get_width()) // 2,
            y=resolution[1] + image.get_height() + 5,
        )
        super().__init__(loc, image)
        self.vel = 8
        self.res = resolution

    def move(self, keys):
        # x axis movement
        if keys[pygame.K_LEFT]:
            self.loc["x"] -= self.vel
        if keys[pygame.K_RIGHT]:
            self.loc["x"] += self.vel

        # y axis movement
        if keys[pygame.K_UP]:
            self.loc["y"] -= self.vel
        if keys[pygame.K_DOWN]:
            self.loc["y"] += self.vel

        # prevent from moving outside
        self.loc["x"] = max(0, min(self.loc["x"], self.res[0] - self.size["w"]))
        self.loc["y"] = max(
            (self.res[1] - self.size["h"]) // 1.4,
            min(self.loc["y"], self.res[1] - self.size["h"]),
        )

    def shoot(self, bullets_right, bullets_left, bullet_image):
        bullets_right.append(
            Projectile(
                player=self,
                side="right",
                image=bullet_image,
            )
        )
        bullets_left.append(
            Projectile(
                player=self,
                side="left",
                image=bullet_image,
            )
        )
