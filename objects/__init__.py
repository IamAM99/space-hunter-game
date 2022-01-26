from typing_extensions import Self
import pygame


class BaseObject:
    def __init__(self, loc: dict, image: pygame.Surface) -> None:
        self.loc = loc
        self.size = dict(w=image.get_width(), h=image.get_height())
        self.image = image
        self.hitbox = self._get_hitbox()  # (x, y, width, height)

    def _get_hitbox(self) -> tuple:
        return (self.loc["x"], self.loc["y"], self.size["w"], self.size["h"])

    def collided(self, other: Self) -> bool:
        x1, y1, w1, h1 = self.hitbox
        x2, y2, w2, h2 = other.hitbox
        if (x1 < x2 + w2) and (x1 + w1 > x2) and (y1 < y2 + h2) and (y1 + h1 > y2):
            return True
        else:
            return False

    def draw(self, win: pygame.Surface) -> None:
        self.hitbox = self._get_hitbox()  # update hitbox
        win.blit(self.image, (self.loc["x"], self.loc["y"]))  # draw the object
        # pygame.draw.rect(win, (255, 255, 255), self.hitbox, 2)  # draw the hitbox
