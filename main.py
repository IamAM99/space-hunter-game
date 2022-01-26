import os
import random
import pygame
from collections import deque


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
    return bg_image, player_image, enemy_image


class Player:
    def __init__(self, loc, size, image) -> None:
        self.loc = loc
        self.size = size
        self.vel = 8
        self.image = image
        self.hitbox = self._get_hitbox()  # (x, y, width, height)

    def _get_hitbox(self):
        return (self.loc["x"], self.loc["y"], self.size["w"], self.size["h"])

    def collided(self, other) -> bool:
        x1, y1, w1, h1 = self.hitbox
        x2, y2, w2, h2 = other.hitbox
        if (x1 < x2 + w2) and (x1 + w1 > x2) and (y1 < y2 + h2) and (y1 + h1 > y2):
            return True
        else:
            return False

    def draw(self, win):
        self.hitbox = self._get_hitbox()  # update hitbox

        # draw the character
        win.blit(self.image, (self.loc["x"], self.loc["y"]))
        # pygame.draw.rect(win, (255, 255, 255), self.hitbox, 2)  # draw the hitbox


class Enemy(Player):
    def __init__(self, loc, size, image) -> None:
        super().__init__(loc, size, image)
        self.vel = 4

    def move(self):
        self.loc["y"] += self.vel


class Projectile:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 15

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
    bg_vel,
    player_loc,
    player_size,
    player_image,
    fps,
    resolution,
    bullet_sound,
):
    bg_loc = 0
    font = pygame.font.SysFont("comicsans", 30, True)
    player = Player(loc=player_loc, size=player_size, image=player_image)
    enemies = deque()
    loop_cnt = 0  # count while loop iterations
    loc = 0
    score = 0
    bullets_left = []
    bullets_right = []
    num_of_bullets = resolution[1]

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
                        size=dict(w=64, h=38),
                        image=enemy_image,
                    )
                )
            loop_cnt = 0

        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            if bullet_r.y < num_of_bullets and bullet_r.y > 0:
                bullet_r.y -= bullet_r.vel
                bullet_l.y -= bullet_l.vel
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
                bullet_sound.play()
                bullets_right.append(
                    Projectile(
                        round(player.loc["x"] + 3.5 * player.size["w"] // 4),
                        round(player.loc["y"] + player.size["h"] // 3),
                        6,
                        (200, 0, 0),
                    )
                )
                bullets_left.append(
                    Projectile(
                        round(player.loc["x"] + 0.5 * player.size["w"] // 4),
                        round(player.loc["y"] + player.size["h"] // 3),
                        6,
                        (200, 0, 0),
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
        player.draw(win)
        for enemy in list(enemies):
            if enemy.loc["y"] > resolution[1]:
                enemies.popleft()
                print("enemy out of screen")
            enemy.draw(win)
            enemy.move()

            if player.collided(enemy):
                score += 1
                print("collided")
        text = font.render("Score: " + str(score), 1, (8, 227, 14))
        win.blit(text, (10, 10))
        for bullet_r, bullet_l in zip(bullets_right, bullets_left):
            bullet_l.draw(win)
            bullet_r.draw(win)
        pygame.display.update()

        loop_cnt += 1


if __name__ == "__main__":
    var = get_init_variables()
    clock = pygame.time.Clock()

    bg_image, player_image, enemy_image = get_images()

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
        bg_image=bg_image,
        bg_vel=var["bg_vel"],
        player_image=player_image,
        player_loc=var["player_loc"],
        player_size=var["player_size"],
        fps=var["fps"],
        resolution=var["res"],
        bullet_sound=bullet_sound,
    )
    pygame.quit()
