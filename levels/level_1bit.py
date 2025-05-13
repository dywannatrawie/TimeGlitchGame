import pygame
import random
from settings import WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER_SPEED, ENEMY_SPEED

class Level1Bit:
    def __init__(self, manager):
        self.manager = manager
        self.player_score = 0
        self.enemy_score = 0
        self.enemy_split = False
        self.glitch_timer = 0
        self.enemy_split_2 = False

        self.player_paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_paddle = pygame.Rect(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

        self.ball_size = 15
        self.ball = pygame.Rect(WIDTH // 2 - self.ball_size // 2, HEIGHT // 2 - self.ball_size // 2, self.ball_size, self.ball_size)
        self.ball_speed_x = 4
        self.ball_speed_y = 4

        self.font = pygame.font.Font(None, 36)

    def split_enemy(self):
        x = self.enemy_paddle.x
        self.enemy_paddle_top = pygame.Rect(x, HEIGHT // 4 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_paddle_bottom = pygame.Rect(x, 3 * HEIGHT // 4 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_split = True

    def split_enemy_2(self):
        x = self.enemy_paddle.x
        self.enemy_paddle_top_left = pygame.Rect(x, HEIGHT // 6 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_paddle_top_right = pygame.Rect(x, HEIGHT // 3 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_paddle_bottom_left = pygame.Rect(x, 2 * HEIGHT // 3 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_paddle_bottom_right = pygame.Rect(x, 5 * HEIGHT // 6 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.enemy_split_2 = True


    def reset_positions(self, direction):
        self.ball.center = (WIDTH // 2, HEIGHT // 2)
        self.ball_speed_x = direction * abs(self.ball_speed_x)
        self.ball_speed_y = random.choice([-4, 4])
        self.player_paddle.centery = HEIGHT // 2
        self.glitch_timer = 10
        if not self.enemy_split:
            self.enemy_paddle.centery = HEIGHT // 2
        else:
            self.enemy_paddle_top.centery = HEIGHT // 4
            self.enemy_paddle_bottom.centery = 3 * HEIGHT // 4

    def update(self, keys, events):
        # Sterowanie gracza
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.player_paddle.top > 0:
            self.player_paddle.y -= PLAYER_SPEED
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.player_paddle.bottom < HEIGHT:
            self.player_paddle.y += PLAYER_SPEED

        # AI sterowanie
        if not self.enemy_split:
            if self.enemy_paddle.centery < self.ball.centery and self.enemy_paddle.bottom < HEIGHT:
                self.enemy_paddle.y += ENEMY_SPEED
            elif self.enemy_paddle.centery > self.ball.centery and self.enemy_paddle.top > 0:
                self.enemy_paddle.y -= ENEMY_SPEED
        elif not self.enemy_split_2:
            if self.ball.centery < HEIGHT // 2:
                if self.enemy_paddle_top.centery < self.ball.centery:
                    self.enemy_paddle_top.y += ENEMY_SPEED
                elif self.enemy_paddle_top.centery > self.ball.centery:
                    self.enemy_paddle_top.y -= ENEMY_SPEED
            else:
                if self.enemy_paddle_bottom.centery < self.ball.centery:
                    self.enemy_paddle_bottom.y += ENEMY_SPEED
                elif self.enemy_paddle_bottom.centery > self.ball.centery:
                    self.enemy_paddle_bottom.y -= ENEMY_SPEED

            # Ograniczenia
            if self.enemy_paddle_top.bottom > HEIGHT // 2:
                self.enemy_paddle_top.bottom = HEIGHT // 2
            if self.enemy_paddle_bottom.top < HEIGHT // 2:
                self.enemy_paddle_bottom.top = HEIGHT // 2
        else:
            # Ruch 4 paletek (2 górne, 2 dolne)
            paddles = [
                self.enemy_paddle_top_left, self.enemy_paddle_top_right,
                self.enemy_paddle_bottom_left, self.enemy_paddle_bottom_right
            ]
            for paddle in paddles:
                if paddle.centery < self.ball.centery:
                    paddle.y += ENEMY_SPEED
                elif paddle.centery > self.ball.centery:
                    paddle.y -= ENEMY_SPEED

            for paddle in paddles:
                paddle.top = max(paddle.top, 0)
                paddle.bottom = min(paddle.bottom, HEIGHT)

        # Ograniczenia gracza
        self.player_paddle.top = max(self.player_paddle.top, 0)
        self.player_paddle.bottom = min(self.player_paddle.bottom, HEIGHT)

        if not self.enemy_split:
            self.enemy_paddle.top = max(self.enemy_paddle.top, 0)
            self.enemy_paddle.bottom = min(self.enemy_paddle.bottom, HEIGHT)

        # Ruch piłki
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Odbicia od ścian
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed_y *= -1

        # Kolizje z paletkami
        if self.ball.colliderect(self.player_paddle):
            self.ball_speed_x = abs(self.ball_speed_x)

        if not self.enemy_split:
            if self.ball.colliderect(self.enemy_paddle):
                self.ball_speed_x = -abs(self.ball_speed_x)
        elif not self.enemy_split_2:
            if self.ball.colliderect(self.enemy_paddle_top) or self.ball.colliderect(self.enemy_paddle_bottom):
                self.ball_speed_x = -abs(self.ball_speed_x)
        else:
            for paddle in [self.enemy_paddle_top_left, self.enemy_paddle_top_right,
                           self.enemy_paddle_bottom_left, self.enemy_paddle_bottom_right]:
                if self.ball.colliderect(paddle):
                    self.ball_speed_x = -abs(self.ball_speed_x)
                    break

        # Punktacja
        if self.ball.left <= 0:
            self.enemy_score += 1
            self.glitch_timer = 10  # efekt glitcha
            self.reset_positions(direction=1)

        elif self.ball.right >= WIDTH:
            self.player_score += 1
            self.glitch_timer = 10  # efekt glitcha
            if self.player_score >= 3 and not self.enemy_split:
                self.split_enemy()
            elif self.player_score >= 7 and not self.enemy_split_2:
                self.split_enemy_2()
            self.reset_positions(direction=-1)


    def draw(self, screen):
        if self.glitch_timer > 0:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.glitch_timer -= 1
        else:
            screen.fill((0, 0, 0))

        # Gracz
        pygame.draw.rect(screen, (255, 255, 255), self.player_paddle)

        # Wróg
        if self.enemy_split_2:
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_top_left)
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_top_right)
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_bottom_left)
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_bottom_right)
        elif self.enemy_split:
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_top)
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle_bottom)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.enemy_paddle)

        # Piłka
        pygame.draw.rect(screen, (255, 255, 255), self.ball)

        # Wynik
        score_text = f"{self.player_score} : {self.enemy_score}"
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH // 2, 30))
        screen.blit(text_surf, text_rect)
