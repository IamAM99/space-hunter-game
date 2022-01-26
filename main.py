import os
import random
import pygame
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
    bullet_sound,
) -> None:
    font = pygame.font.SysFont("comicsans", 30, True)
    bg_loc = 0  # initial y location of the background image
    player = Player(resolution=resolution, image=player_image)
    loop_cnt = 0  # count while loop iterations
    enemies = []
    bullets = []
    score = 0

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
        for idx, bullet in enumerate(bullets):
            if bullet.loc["y"] > -bullet.size["h"]:
                bullet.move()
            else:
                bullets.pop(idx)

        # check key pushes
        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            if loop_cnt % 10 < 2:
                bullet_sound.play()
                player.shoot(bullets, bullet_image)

        ## draw the images
        # background
        bg_loc += bg_vel
        if bg_loc > resolution[1]:
            bg_loc = 0
        draw_window(bg_image, bg_loc, resolution)

        # enemies
        for enemy in list(enemies):
            if enemy.loc["y"] > resolution[1]:
                enemies.pop(0)
                print("enemy out of screen")
                continue
            enemy.draw(win)
            enemy.move()

            # player-enemy collision
            if player.collided(enemy):
                score += 1
                print("player collided")
        text = font.render("Score: " + str(score), 1, (8, 227, 14))
        win.blit(text, (10, 10))

        # projectiles
        for idx_b, bullet in enumerate(bullets):
            bullet.draw(win)

            # bullet-enemy collision
            for idx_e, enemy in enumerate(enemies):
                if bullet.collided(enemy):
                    enemies.pop(idx_e)
                    bullets.pop(idx_b)

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
    pygame.mixer.init()

    # music
    bullet_sound = pygame.mixer.Sound(os.path.join("assets", "bullet.mp3"))
    hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit.mp3"))
    music = pygame.mixer.music.load(os.path.join("assets", "music.mp3"))
    pygame.mixer.music.play(-1)

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
        bullet_sound=bullet_sound,
    )
    pygame.quit()
