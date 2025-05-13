import pygame
from settings import WIDTH, HEIGHT, BLACK, WHITE, YELLOW, BLUE

TILE_SIZE = 20
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

class Level8Bit:
    def __init__(self, manager):
        self.manager = manager
        self.clock = pygame.time.Clock()
        self.player = pygame.Rect(40, 40, TILE_SIZE, TILE_SIZE)
        self.speed = 4
        self.dots = []
        self.walls = []
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.load_map()

    def load_map(self):
        # Prosty układ ścian i punktów
        for y in range(ROWS):
            for x in range(COLS):
                if x == 0 or y == 0 or x == COLS-1 or y == ROWS-1 or (x % 4 == 0 and y % 3 == 0):
                    self.walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    self.dots.append(pygame.Rect(x * TILE_SIZE + TILE_SIZE//4, y * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))

    def update(self, keys, events):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -self.speed
        if keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_UP]: dy = -self.speed
        if keys[pygame.K_DOWN]: dy = self.speed

        future = self.player.move(dx, dy)
        if not any(future.colliderect(wall) for wall in self.walls):
            self.player = future

        # Jedzenie punktów
        self.dots = [dot for dot in self.dots if not self.player.colliderect(dot)]
        self.score = 300 - len(self.dots)

        if not self.dots:
            print("PACMAN WIN!")
            self.manager.load_scene("hub")  # powrót do huba

    def draw(self, screen):
        screen.fill(BLACK)
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
        for dot in self.dots:
            pygame.draw.ellipse(screen, WHITE, dot)
        pygame.draw.circle(screen, YELLOW, self.player.center, TILE_SIZE // 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
