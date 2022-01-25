import os
import math
import pygame

pygame.init()


sign = lambda x: math.copysign(1, x)

player = pygame.image.load(os.path.join("assets", "player.png"))
bg = pygame.image.load(os.path.join("assets", "bg.png"))


win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("AP Project")

x, y = 250 - 32, 500 - 64
height, width = 64, 64
vel = 24
fps = 60

is_jump = False
jump_count = 10
walk_count = 0


def draw_window():
    global walk_count

    win.blit(bg, (0, 0))
    win.blit(player, (x, y))
    # pygame.draw.rect(win, (255, 20, 20), (x, y, width, height))
    pygame.display.update()


run = True
while run:
    pygame.time.delay((10 ** 3) // fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if not is_jump:
        if keys[pygame.K_UP]:
            y -= vel
        if keys[pygame.K_DOWN]:
            y += vel
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            y -= sign(jump_count) * (jump_count ** 2) * 0.4
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

    x = max(0, min(x, 500 - width))
    y = max(0, min(y, 500 - height))

    draw_window()

pygame.quit()
