import os
import pygame


def get_init_variables():
    """Get the initial variables"""
    res = (900, 600)
    player_size = dict(w=64, h=64)

    variables = dict(
        res=res,  # game window size
        fps=80,  # game frame rate
        player_size=player_size,  # size of the player character
        player_loc=dict(
            x=(res[0] - player_size["w"]) // 2, y=res[1] + player_size["h"] + 5
        ),  # initial location of the player
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
        self.left = False
        self.right = False

    def draw(self, win):
        win.blit(self.image, (self.loc["x"], self.loc["y"]))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def draw_window(bg_image, loc, resolution):
    win.blit(bg_image, (0, loc))
    win.blit(bg_image, (0, loc - resolution[1]))


def main_loop(
    run: bool,
    win,
    clock,
    bg_image,
    player_loc,
    player_size,
    player_image,
    fps,
    resolution,
):
    player = Player(loc=player_loc, size=player_size, image=player_image)
    loc = 0
    bullets_left = []
    bullets_right = []
    num_of_bullets = 900
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            if bullet_r.y < num_of_bullets and bullet_r.y > 0:
                bullet_r.y += bullet_r.vel
                bullet_l.y += bullet_l.vel
            else:
                bullets_right.pop(bullets_right.index(bullet_r))
                bullets_left.pop(bullets_left.index(bullet_l))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.loc["x"] -= player.vel
            player.left = True
            player.right = False
        if keys[pygame.K_RIGHT]:
            player.loc["x"] += player.vel
            player.right = True
            player.left = False

        if keys[pygame.K_UP]:
            player.loc["y"] -= player.vel
            player.right = False
            player.left = False
        if keys[pygame.K_DOWN]:
            player.loc["y"] += player.vel
            player.right = False
            player.left = False

        if keys[pygame.K_SPACE]:
            if len(bullets_right) < 5:
                bullets_right.append(projectile(
                    round(player.loc["x"] + 3.4*player.size["w"]//4),
                    round(player.loc["y"] + player.size["h"]//3), 6, (200, 0, 0), -1))
                bullets_left.append(projectile(
                    round(player.loc["x"] + 0.6*player.size["w"]//4),
                    round(player.loc["y"] + player.size["h"]//3), 6, (200, 0, 0), -1))

        player.loc["x"] = max(
            0, min(player.loc["x"], resolution[0] - player.size["w"]))
        player.loc["y"] = max(
            0, min(player.loc["y"], resolution[1] - player.size["h"]))

        # draw
        loc += 2
        if loc > resolution[1]:
            loc = 0
        draw_window(bg_image, loc, resolution)
        player.draw(win)
        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            bullet_l.draw(win)
            bullet_r.draw(win)
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
        player_image=player_image,
        player_loc=var["player_loc"],
        player_size=var["player_size"],
        fps=var["fps"],
        resolution=var["res"],
    )
    pygame.quit()
