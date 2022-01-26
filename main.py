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
    music = pygame.mixer.music.load(os.path.join("assets/sound", "music.mp3"))
    return bullet_sound, music


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
    font,
) -> None:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    bullet_sound.set_volume(0.7)
    bg_loc = 0  # initial y location of the background image
    player = Player(resolution=resolution, image=player_image)
    loop_cnt = 0  # count while loop iterations
    enemies = []
    bullets = []
    score = 0
    game = True
    end_text_str = "Press space to try again!"
    end_text = font.render(end_text_str, 1, (220, 220, 220))

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
                loop_cnt = 0  # count while loop iterations
                enemies = []
                bullets = []
                score = 0

            draw_window(bg_image, bg_loc, var["res"])
            pygame.draw.rect(
                win,
                (0, 0, 0),
                (
                    (var["res"][0] - rect_size[0]) // 2,
                    (var["res"][1] - rect_size[1] + 50) // 2,
                    *rect_size,
                ),
                border_radius=5,
            )
            win.blit(
                score_text,
                (
                    (var["res"][0] - font.size(score_text_str)[0]) // 2,
                    (var["res"][1] - font.size(score_text_str)[1]) // 2,
                ),
            )
            win.blit(
                end_text,
                (
                    (var["res"][0] - font.size(end_text_str)[0]) // 2,
                    (
                        var["res"][1]
                        - font.size(end_text_str)[1]
                        + font.size(score_text_str)[1] * 2
                    )
                    // 2,
                ),
            )

        # update the display
        pygame.display.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
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
    score, bg_loc = main_loop(**loop_kwargs)

    pygame.quit()
