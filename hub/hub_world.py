import pygame
from settings import WIDTH, HEIGHT, YELLOW, WHITE, CYAN, BLACK
from loader import load_background, load_font

class HubWorld:
    def __init__(self, manager):
        self.background = load_background()
        self.font = load_font()
        self.manager = manager
        self.ludzik = pygame.Rect(100, 300, 20, 20)
        self.portal = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 40, 30, 80)
        self.portal2 = pygame.Rect(300, 200, 50, 80)
        self.portal2_color = (255, 100, 0)

    def update(self, keys, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        ludzik_speed = 5
        for dx, dy, key in [(-ludzik_speed, 0, keys[pygame.K_LEFT]), (ludzik_speed, 0, keys[pygame.K_RIGHT]),
                            (0, -ludzik_speed, keys[pygame.K_UP]), (0, ludzik_speed, keys[pygame.K_DOWN])]:
            if key:
                next_pos = self.ludzik.move(dx, dy)
                self.ludzik = next_pos

        if self.ludzik.colliderect(self.portal):
            self.manager.load_scene("4bit")

        if self.manager.unlocked_scenes["8bit"] and self.ludzik.colliderect(self.portal2):
            # np. launch external Tetris or transition
            self.manager.launch_tetris()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        pygame.draw.rect(screen, YELLOW, self.ludzik)
        pygame.draw.rect(screen, WHITE, self.portal)

        if self.manager.unlocked_scenes["8bit"]:
            pygame.draw.rect(screen, self.portal2_color, self.portal2)
            screen.blit(self.font.render("Mini-gra odblokowana!", True, BLACK), (WIDTH // 2 - 120, HEIGHT // 2))
        else:
            screen.blit(self.font.render("Wejście do Areny", True, BLACK), (self.portal.x - 30, self.portal.y - 30))
