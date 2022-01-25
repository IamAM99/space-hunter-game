import os
import random
import pygame
from collections import deque
from objects.enemy import Enemy
from objects.player import Player
from objects.projectile import Projectile


def get_init_variables():
    """Get the initial variables"""
    res = (900, 600)
    player_size = dict(w=56, h=57)

    variables = dict(
        res=res,  # game window size
        fps=60,  # game frame rate
        player_size=player_size,  # size of the player character
        player_loc=dict(
            x=(res[0] - player_size["w"]) // 2, y=res[1] + player_size["h"] + 5
        ),  # initial location of the player
        bg_vel=1,  # velocity of background movement
    )
    return variables


def get_images():
    bg_image = pygame.image.load(os.path.join("assets", "bg.png"))
    player_image = pygame.image.load(os.path.join("assets", "player.png"))
    enemy_image = pygame.image.load(os.path.join("assets", "enemy.png"))
    bullet_image = pygame.image.load(os.path.join("assets", "bullet.png"))
    return bg_image, player_image, enemy_image, bullet_image


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
    bullet_image,
    fps,
    resolution,
):
    bg_loc = 0
    player = Player(loc=player_loc, image=player_image)
    enemies = deque()
    loop_cnt = 0  # count while loop iterations
    bullets_left = []
    bullets_right = []

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # print(loop_cnt)
        # create a new enemy
        if loop_cnt == fps:  # try to add enemy every second
            if random.getrandbits(1):
                print("enemy created")
                enemies.append(
                    Enemy(
                        loc=dict(x=random.random() * (resolution[0] - 64), y=-38),
                        image=enemy_image,
                    )
                )
            loop_cnt = 0

        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            if bullet_r.loc["y"] > -bullet_r.size["h"]:
                bullet_r.loc["y"] -= bullet_r.vel
                bullet_l.loc["y"] -= bullet_l.vel
            else:
                bullets_right.pop(bullets_right.index(bullet_r))
                bullets_left.pop(bullets_left.index(bullet_l))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.loc["x"] -= player.vel
        if keys[pygame.K_RIGHT]:
            player.loc["x"] += player.vel

        if keys[pygame.K_UP]:
            player.loc["y"] -= player.vel
        if keys[pygame.K_DOWN]:
            player.loc["y"] += player.vel

        if keys[pygame.K_SPACE]:
            if loop_cnt % 10 < 2:
                bullets_right.append(
                    Projectile(
                        player=player,
                        side="right",
                        image=bullet_image,
                    )
                )
                bullets_left.append(
                    Projectile(
                        player=player,
                        side="left",
                        image=bullet_image,
                    )
                )

        player.loc["x"] = max(0, min(player.loc["x"], resolution[0] - player.size["w"]))
        player.loc["y"] = max(
            (resolution[1] - player.size["h"]) // 1.4,
            min(player.loc["y"], resolution[1] - player.size["h"]),
        )

        # draw
        bg_loc += bg_vel
        if bg_loc > resolution[1]:
            bg_loc = 0
        draw_window(bg_image, bg_loc, resolution)

        for enemy in list(enemies):
            if enemy.loc["y"] > resolution[1]:
                enemies.popleft()
                print("enemy out of screen")
            enemy.draw(win)
            enemy.move()

            if player.collided(enemy):
                print("collided")

        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            bullet_l.draw(win)
            bullet_r.draw(win)

        player.draw(win)

        pygame.display.update()

        loop_cnt += 1


if __name__ == "__main__":
    var = get_init_variables()
    clock = pygame.time.Clock()

    bg_image, player_image, enemy_image, bullet_image = get_images()

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
        bullet_image=bullet_image,
        fps=var["fps"],
        resolution=var["res"],
    )
    pygame.quit()
