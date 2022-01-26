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
    bg_image = pygame.image.load(os.path.join("assets/img", "bg.png"))
    player_image = pygame.image.load(os.path.join("assets/img", "player.png"))
    enemy_image = pygame.image.load(os.path.join("assets/img", "enemy.png"))
    bullet_image = pygame.image.load(os.path.join("assets/img", "bullet.png"))
    return bg_image, player_image, enemy_image, bullet_image


def get_sounds() -> tuple:
    bullet_sound = pygame.mixer.Sound(os.path.join("assets/sound", "bullet.wav"))
    hit_sound = pygame.mixer.Sound(os.path.join("assets/sound", "hit.mp3"))
    music = pygame.mixer.music.load(os.path.join("assets/sound", "music.mp3"))
    return bullet_sound, hit_sound, music


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
    pygame.mixer.music.play(-1)
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
            if loop_cnt % 10 < 1:
                bullet_sound.play()
            if loop_cnt % 10 < 2:
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
                score -= 1
                print("enemy out of screen")
                continue
            enemy.draw(win)
            enemy.move()

            # player-enemy collision
            if player.collided(enemy):
                print("player collided")

        # projectiles
        for idx_b, bullet in enumerate(bullets):
            bullet.draw(win)

            # bullet-enemy collision
            for idx_e, enemy in enumerate(enemies):
                if bullet.collided(enemy):
                    score += 2
                    enemies.pop(idx_e)
                    bullets.pop(idx_b)

        # player
        player.draw(win)

        text = font.render("Score: " + str(score), 1, (220, 220, 220))
        win.blit(text, (9, 0))

        # update the display
        pygame.display.update()

        # update the loop counter
        loop_cnt += 1


if __name__ == "__main__":
    # initialize game
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # get config variables
    var = get_init_variables()

    # load assets
    bg_image, player_image, enemy_image, bullet_image = get_images()
    bullet_sound, hit_sound, music = get_sounds()

    # create game window
    win = pygame.display.set_mode(var["res"])
    pygame.display.set_caption("Space Hunter")

    # game main loop
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
