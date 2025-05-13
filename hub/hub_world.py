import pygame
import math
import os
from settings import WIDTH, HEIGHT, YELLOW, WHITE, CYAN, BLACK, GREEN, RED
from loader import load_background, load_font, load_portal_image
import pygame.mixer

class HubWorld:
    def __init__(self, manager):
        self.background = load_background()
        self.font = load_font()
        self.manager = manager

        self.ludzik = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.portal_glow = 0
        self.glow_up = True

        # Wczytanie grafiki portalu
        self.portal_img = load_portal_image()


        # Dźwięk portalu
        try:
            self.portal_sound = pygame.mixer.Sound("assets/sound/portal.wav")
        except:
            self.portal_sound = None

        spacing = 100
        top_y = HEIGHT // 2 - 150
        left_x = WIDTH // 4 - 20
        right_x = WIDTH * 3 // 4 - 20

        self.portals = {
            "1bit": pygame.Rect(left_x, top_y + spacing * 0, 40, 80),
            "8bit": pygame.Rect(left_x, top_y + spacing * 1, 40, 80),
            "8bit_2": pygame.Rect(right_x, top_y + spacing * 0, 40, 80),
            "8bit_3": pygame.Rect(right_x, top_y + spacing * 1, 40, 80),
            "64bit": pygame.Rect(WIDTH // 2 - 20, top_y + spacing * 2, 40, 80),
            "tetris": pygame.Rect(WIDTH // 2 - 20, HEIGHT - 120, 40, 80)
        }

        self.portal_colors = {
            "1bit": CYAN,
            "8bit": GREEN,
            "8bit_2": GREEN,
            "8bit_3": GREEN,
            "64bit": RED,
            "tetris": WHITE
        }

    def update(self, keys, events):
        speed = 5
        if keys[pygame.K_LEFT]:
            self.ludzik.x -= speed
        if keys[pygame.K_RIGHT]:
            self.ludzik.x += speed
        if keys[pygame.K_UP]:
            self.ludzik.y -= speed
        if keys[pygame.K_DOWN]:
            self.ludzik.y += speed

        for name, rect in self.portals.items():
            if self.ludzik.colliderect(rect):
                if self.portal_sound:
                    self.portal_sound.play()
                scene = name if not name.startswith("8bit_") else "8bit"
                self.manager.load_scene(scene)

        # Animacja świecenia portali
        if self.glow_up:
            self.portal_glow += 2
            if self.portal_glow >= 60:
                self.glow_up = False
        else:
            self.portal_glow -= 2
            if self.portal_glow <= 0:
                self.glow_up = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for name, rect in self.portals.items():
            color = self.portal_colors[name]
            animated_color = (
                min(color[0] + self.portal_glow, 255),
                min(color[1] + self.portal_glow, 255),
                min(color[2] + self.portal_glow, 255)
            )

            pygame.draw.rect(screen, animated_color, rect.inflate(10, 10), 3)
            if self.portal_img:
                screen.blit(self.portal_img, rect.topleft)
            else:
                pygame.draw.rect(screen, animated_color, rect)

            screen.blit(self.font.render(name.upper(), True, BLACK), (rect.x, rect.y - 30))

        pygame.draw.rect(screen, WHITE, self.ludzik)
