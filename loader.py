import pygame
import os
from settings import WIDTH, HEIGHT

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

def load_background(scene="hub"):
    try:
        if scene == "hub":
            path = os.path.join("assets", "graphic", "hubbackground.png")
        else:
            path = os.path.join("assets", scene, "background.png")
        bg = pygame.image.load(path)
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"Nie udało się załadować tła dla '{scene}': {e}")
        return pygame.Surface((WIDTH, HEIGHT))  # domyślne czarne tło

def load_portal_image():
    try:
        img = pygame.image.load(os.path.join("assets", "hub", "portal.png")).convert_alpha()
        return pygame.transform.scale(img, (40, 80))
    except:
        return None

def load_font(scene="hub"):
    try:
        if scene == "8bit":
            return pygame.font.Font(os.path.join("assets", "8bit", "8bit_font.ttf"), 28)
        elif scene == "16bit":
            return pygame.font.Font(os.path.join("assets", "16bit", "16bit_font.ttf"), 32)
        else:
            return pygame.font.SysFont(None, 36)
    except Exception as e:
        print(f"Błąd ładowania fontu dla '{scene}': {e}")
        return pygame.font.SysFont(None, 36)
