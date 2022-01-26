import os
import random
import pygame
from collections import deque
from objects.enemy import Enemy
from objects.player import Player


def get_init_variables() -> dict:
    """Get the initial variables"""
    variables = dict(
        res=(900, 600),  # game window size
        fps=60,  # game frame rate
        bg_vel=1,  # velocity of background movement
    )
    return variables


def get_images() -> tuple:
    bg_image = pygame.image.load(os.path.join("assets", "bg.png"))
    player_image = pygame.image.load(os.path.join("assets", "player.png"))
    enemy_image = pygame.image.load(os.path.join("assets", "enemy.png"))
    bullet_image = pygame.image.load(os.path.join("assets", "bullet.png"))
    return bg_image, player_image, enemy_image, bullet_image


def draw_window(bg_image: pygame.Surface, loc: float, resolution: tuple) -> None:
    win.blit(bg_image, (0, loc))
    win.blit(bg_image, (0, loc - resolution[1]))


def main_loop(
    run: bool,
    win: pygame.Surface,
    clock: pygame.time.Clock,
    bg_image: pygame.Surface,
    bg_vel: float,
    player_image: pygame.Surface,
    enemy_image: pygame.Surface,
    bullet_image: pygame.Surface,
    fps: int,
    resolution: tuple,
) -> None:
    bg_loc = 0  # initial y location of the background image
    player = Player(resolution=resolution, image=player_image)
    enemies = deque()
    loop_cnt = 0  # count while loop iterations
    bullets_left = []
    bullets_right = []

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        # move bullets and remove outside bullets
        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            if bullet_r.loc["y"] > -bullet_r.size["h"]:
                bullet_r.move()
                bullet_l.move()
            else:
                bullets_right.pop(bullets_right.index(bullet_r))
                bullets_left.pop(bullets_left.index(bullet_l))

        # check key pushes
        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            if loop_cnt % 10 < 2:
                player.shoot(bullets_right, bullets_left, bullet_image)

        ## draw the images
        # background
        bg_loc += bg_vel
        if bg_loc > resolution[1]:
            bg_loc = 0
        draw_window(bg_image, bg_loc, resolution)

        # enemies
        for enemy in list(enemies):
            if enemy.loc["y"] > resolution[1]:
                enemies.popleft()
                print("enemy out of screen")
            enemy.draw(win)
            enemy.move()

            if player.collided(enemy):
                print("collided")

        # projectiles
        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            bullet_l.draw(win)
            bullet_r.draw(win)

        # player
        player.draw(win)

        # update the display
        pygame.display.update()

        # update the loop counter
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
        bg_vel=var["bg_vel"],
        bg_image=bg_image,
        player_image=player_image,
        enemy_image=enemy_image,
        bullet_image=bullet_image,
        fps=var["fps"],
        resolution=var["res"],
    )
    pygame.quit()
