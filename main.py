import os
import math
import pygame

## Globals
RES = (500, 500)  # game window size
FPS = 60  # game frame rate
PLAYER_SIZE = dict(w=64, h=64)
PLAYER_LOC = dict(x=(RES[0] - PLAYER_SIZE["w"]) // 2, y=RES[1] + PLAYER_SIZE["h"] + 5)

pygame.init()


sign = lambda x: math.copysign(1, x)

player_image = pygame.image.load(os.path.join("assets", "player.png"))
bg_image = pygame.image.load(os.path.join("assets", "bg.png"))


clock = pygame.time.Clock()

win = pygame.display.set_mode(RES)
pygame.display.set_caption("AP Project")


class Player:
    def __init__(self, loc, size) -> None:
        self.loc = loc
        self.size = size
        self.vel = 24


def draw_window(bg_image, player_image, player: Player):
    win.blit(bg_image, (0, 0))
    win.blit(player_image, (player.loc["x"], player.loc["y"]))
    pygame.display.update()


player = Player(loc=PLAYER_LOC, size=PLAYER_SIZE)
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.loc["x"] -= player.vel
    if keys[pygame.K_RIGHT]:
        player.loc["x"] += player.vel

    if keys[pygame.K_UP]:
        player.loc["y"] -= player.vel
    if keys[pygame.K_DOWN]:
        player.loc["y"] += player.vel

    player.loc["x"] = max(0, min(player.loc["x"], RES[0] - player.size["w"]))
    player.loc["y"] = max(0, min(player.loc["y"], RES[1] - player.size["h"]))

    draw_window(bg_image, player_image, player)

pygame.quit()
