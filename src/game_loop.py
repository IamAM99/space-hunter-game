import random
import pygame
from objects.enemy import Enemy
from objects.player import Player
from .config import get_init_variables, get_game_init_vars, get_images, get_sounds


def draw_window(
    win: pygame.Surface, bg_image: pygame.Surface, loc: float, resolution: tuple
) -> None:
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
    bullet_sound: pygame.mixer.Sound,
    font: pygame.font.SysFont,
) -> None:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    bullet_sound.set_volume(0.7)
    end_text_str = "Press space to try again!"
    end_text = font.render(end_text_str, 1, (220, 220, 220))
    player = Player(resolution=resolution, image=player_image)
    bg_loc, loop_cnt, enemies, bullets, score = get_game_init_vars()
    game = True

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if game:
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
            draw_window(win, bg_image, bg_loc, resolution)

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
                    score_text = font.render(score_text_str, 1, (220, 220, 220))
                    rect_size = (
                        font.size(end_text_str)[0] + 50,
                        font.size(score_text_str)[1] + font.size(end_text_str)[1] + 50,
                    )
                    game = False

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

            # score
            score_text_str = "Score: " + str(score)
            score_text = font.render(score_text_str, 1, (220, 220, 220))
            win.blit(score_text, (9, 0))

            # update the loop counter
            loop_cnt += 1
        else:
            # check key press
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game = True
                bg_loc, loop_cnt, enemies, bullets, score = get_game_init_vars()

            # draw game over
            draw_window(win, bg_image, bg_loc, resolution)
            pygame.draw.rect(
                win,
                (0, 0, 0),
                (
                    (resolution[0] - rect_size[0]) // 2,
                    (resolution[1] - rect_size[1] + 50) // 2,
                    *rect_size,
                ),
                border_radius=5,
            )
            win.blit(
                score_text,
                (
                    (resolution[0] - font.size(score_text_str)[0]) // 2,
                    (resolution[1] - font.size(score_text_str)[1]) // 2,
                ),
            )
            win.blit(
                end_text,
                (
                    (resolution[0] - font.size(end_text_str)[0]) // 2,
                    (
                        resolution[1]
                        - font.size(end_text_str)[1]
                        + font.size(score_text_str)[1] * 2
                    )
                    // 2,
                ),
            )

        # update the display
        pygame.display.update()


def run_game() -> None:
    # initialize game
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # get config variables
    var = get_init_variables()

    # load assets
    bg_image, player_image, enemy_image, bullet_image = get_images()
    bullet_sound, music = get_sounds()
    font = pygame.font.SysFont("comicsans", 30, True)

    # create game window
    win = pygame.display.set_mode(var["res"])
    pygame.display.set_caption("Space Hunter")

    # game main loop
    loop_kwargs = dict(
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
        font=font,
    )
    main_loop(**loop_kwargs)

    pygame.quit()


if __name__ == "__main__":
    run_game()
