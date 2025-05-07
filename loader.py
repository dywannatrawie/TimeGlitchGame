# loader.py

import pygame
import os

def load_fruit_images():
    fruit_paths = ["apple.png", "banana.png", "pear.png"]
    return [pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "graphic", name)), (15, 15)) for name in fruit_paths]

def load_mouse_images():
    imgs = {}
    for direction in ["up", "down"]:
        imgs[direction] = [
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphic", f"mysz_1_{direction}.png")), (15, 20)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphic", f"mysz_2_{direction}.png")), (15, 20))
        ]
    for direction in ["left", "right"]:
        imgs[direction] = [
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphic", f"mysz_1_{direction}.png")), (20, 16)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphic", f"mysz_2_{direction}.png")), (20, 16))
        ]
    return imgs

def load_obstacle_image():
    return pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphic", "block.png")), (40, 40))

def load_background():
    bg = pygame.image.load(os.path.join("assets", "graphic", "background.png"))
    return pygame.transform.scale(bg, (800, 600))

def load_font():
    return pygame.font.SysFont(None, 36)
