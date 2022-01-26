import os
import pygame


def get_init_variables() -> dict:
    """Get the initial variables"""
    variables = dict(
        res=(900, 600),  # game window size
        fps=60,  # game frame rate
        bg_vel=1,  # velocity of background movement
    )
    return variables


def get_game_init_vars():
    bg_loc = 0  # initial y location of the background image
    loop_cnt = 0  # count while loop iterations
    enemies = []
    bullets = []
    score = 0
    out = (bg_loc, loop_cnt, enemies, bullets, score)
    return out


def get_images() -> tuple:
    bg_image = pygame.image.load(os.path.join("assets", "img", "bg.png"))
    player_image = pygame.image.load(os.path.join("assets", "img", "player.png"))
    enemy_image = pygame.image.load(os.path.join("assets", "img", "enemy.png"))
    bullet_image = pygame.image.load(os.path.join("assets", "img", "bullet.png"))
    return bg_image, player_image, enemy_image, bullet_image


def get_sounds() -> tuple:
    bullet_sound = pygame.mixer.Sound(os.path.join("assets", "sound", "bullet.wav"))
    music = pygame.mixer.music.load(os.path.join("assets", "sound", "music.mp3"))
    return bullet_sound, music
