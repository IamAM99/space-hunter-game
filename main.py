import os
import pygame


def get_init_variables():
    """Get the initial variables"""
    res = (900, 600)
    player_size = dict(w=64, h=64)

    variables = dict(
        res=res,  # game window size
        fps=60,  # game frame rate
        player_size=player_size,  # size of the player character
        player_loc=dict(
            x=(res[0] - player_size["w"]) // 2, y=res[1] + player_size["h"] + 5
        ),  # initial location of the player
        bg_vel=2,  # velocity of background movement
    )
    return variables


def get_images():
    bg_image = pygame.image.load(os.path.join("assets", "bg.png"))
    player_image = pygame.image.load(os.path.join("assets", "player.png"))
    return bg_image, player_image


class Player:
    def __init__(self, loc, size, image) -> None:
        self.loc = loc
        self.size = size
        self.vel = 24
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.loc["x"], self.loc["y"]))


class Enemy(Player):
    def __init__(self, loc, size, image) -> None:
        super().__init__(loc, size, image)

    def move(self):
        pass


def draw_window(bg_image, loc, resolution):
    win.blit(bg_image, (0, loc))
    win.blit(bg_image, (0, loc - resolution[1]))


def main_loop(
    run: bool,
    win,
    clock,
    bg_image,
    bg_vel,
    player_loc,
    player_size,
    player_image,
    fps,
    resolution,
):
    player = Player(loc=player_loc, size=player_size, image=player_image)
    bg_loc = 0
    while run:
        clock.tick(fps)

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

        player.loc["x"] = max(0, min(player.loc["x"], resolution[0] - player.size["w"]))
        player.loc["y"] = max(0, min(player.loc["y"], resolution[1] - player.size["h"]))

        # draw
        bg_loc += bg_vel
        if bg_loc > resolution[1]:
            bg_loc = 0
        draw_window(bg_image, bg_loc, resolution)
        player.draw(win)
        pygame.display.update()


if __name__ == "__main__":
    var = get_init_variables()
    clock = pygame.time.Clock()

    bg_image, player_image = get_images()

    win = pygame.display.set_mode(var["res"])
    pygame.display.set_caption("Space")

    pygame.init()
    main_loop(
        run=True,
        win=win,
        clock=clock,
        bg_image=bg_image,
        bg_vel=var["bg_vel"],
        player_image=player_image,
        player_loc=var["player_loc"],
        player_size=var["player_size"],
        fps=var["fps"],
        resolution=var["res"],
    )
    pygame.quit()
