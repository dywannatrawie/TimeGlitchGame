import pygame

# Dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# 1bit level
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80

PLAYER_SPEED = 6
ENEMY_SPEED = 2 # oryginalne 5, może być 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGIC = (255, 0, 255)

# Font
pygame.font.init()
FONT = pygame.font.SysFont(None, 36)
