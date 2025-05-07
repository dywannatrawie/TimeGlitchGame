import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
import random
from settings import WIDTH, HEIGHT, YELLOW, GREEN, WHITE, CYAN, MAGIC
from loader import load_fruit_images, load_mouse_images, load_obstacle_image, load_font
from engine.utils import clamp_rect, distance, safe_div


class Level4Bit:
    def __init__(self, manager):
        self.fruit_imgs = load_fruit_images()
        self.mouse_imgs = load_mouse_images()
        self.obstacle_img = load_obstacle_image()
        self.font = load_font()
        self.manager = manager
        self.reset_level()

    def reset_level(self):
        self.ludzik = pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20)
        self.last_direction = [0, 0]
        self.bullet_ready = 0
        self.score = 0
        self.snake_lives = 10
        self.snake_length = 50
        self.snake = []
        self.obstacles = []
        self.veggies = []
        self.veggie_types = []
        self.bullets = []
        self.food_items = []
        self.food_velocities = []
        self.mouse_directions = []
        self.mouse_anim_timer = 0
        self.glitch_timer = 0
        self.magic_item = None
        self.exit_door = None
        self.has_magic_item = False
        self.spawn_snake()
        self.spawn_arena()

    def spawn_snake(self):
        self.snake.clear()
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        for i in range(self.snake_length):
            self.snake.append(pygame.Rect(x - i * 20, y, 20, 20))

    def spawn_arena(self):
        self.obstacles = [pygame.Rect(random.randint(100, WIDTH - 140),
                                      random.randint(100, HEIGHT - 140), 40, 40) for _ in range(6)]
        self.veggies.clear()
        self.veggie_types.clear()
        for _ in range(5):
            rect = pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 15, 15)
            self.veggies.append(rect)
            self.veggie_types.append(random.randint(0, len(self.fruit_imgs) - 1))

        self.food_items = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20)
                           for _ in range(4)]
        self.food_velocities.clear()
        self.mouse_directions.clear()
        for _ in self.food_items:
            vx = random.choice([-1, 1]) * random.randint(1, 2)
            vy = random.choice([-1, 1]) * random.randint(1, 2)
            self.food_velocities.append([vx, vy])
            if abs(vx) > abs(vy):
                self.mouse_directions.append("right" if vx > 0 else "left")
            else:
                self.mouse_directions.append("down" if vy > 0 else "up")

    def update(self, keys, events):
        self.glitch_timer += 1
        self.mouse_anim_timer += 1

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and self.bullet_ready > 0:
                    bullet = pygame.Rect(self.ludzik.centerx, self.ludzik.centery, 8, 8)
                    self.bullets.append((bullet, self.last_direction[:]))
                    self.bullet_ready -= 1

        ludzik_speed = 5
        for dx, dy, key in [(-ludzik_speed, 0, keys[pygame.K_LEFT]), (ludzik_speed, 0, keys[pygame.K_RIGHT]),
                            (0, -ludzik_speed, keys[pygame.K_UP]), (0, ludzik_speed, keys[pygame.K_DOWN])]:
            if key:
                self.last_direction = [dx // ludzik_speed, dy // ludzik_speed]
                next_pos = self.ludzik.move(dx, dy)
                if not any(next_pos.colliderect(o) for o in self.obstacles):
                    self.ludzik = clamp_rect(next_pos, WIDTH, HEIGHT)

        # Interakcje z warzywami
        for i, veggie in enumerate(self.veggies):
            if self.ludzik.colliderect(veggie):
                self.veggies.remove(veggie)
                self.bullet_ready += 1
                self.score += 1
                new_rect = pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 15, 15)
                self.veggies.append(new_rect)
                self.veggie_types.append(random.randint(0, len(fruit_imgs)-1))

        # Kolizja z wężem
        if self.snake and any(part.colliderect(self.ludzik) for part in self.snake):
            self.manager.load_scene("hub")
            return

        # Wąż śledzi gracza i jedzenie
        if self.snake:
            targets = [self.ludzik] + self.food_items
            closest = min(targets, key=lambda t: distance(self.snake[0], t))
            dx = closest.x - self.snake[0].x
            dy = closest.y - self.snake[0].y
            dist = distance(self.snake[0], closest)
            dir_x = safe_div(dx, dist)
            dir_y = safe_div(dy, dist)
            new_head = self.snake[0].move(int(2 * dir_x), int(2 * dir_y))
            if not any(new_head.colliderect(o) for o in self.obstacles):
                self.snake.insert(0, clamp_rect(new_head, WIDTH, HEIGHT))
            if len(self.snake) > self.snake_length:
                self.snake.pop()

        # Pociski
        for i in range(len(self.bullets)):
            bullet, direction = self.bullets[i]
            bullet.x += direction[0] * 6
            bullet.y += direction[1] * 6

        for bullet, _ in self.bullets[:]:
            if not self.snake:
                continue
            if any(bullet.colliderect(part) for part in self.snake):
                self.bullets.remove((bullet, _))
                self.snake_lives -= 1
                if self.snake_lives <= 0:
                    self.magic_item = pygame.Rect(self.snake[0].x, self.snake[0].y, 15, 15)
                    self.exit_door = pygame.Rect(WIDTH // 2 - 15, 50, 30, 60)
                    self.snake.clear()
                else:
                    self.snake_length = max(1, self.snake_length - 2)

        # Myszki z jedzeniem
        for i in range(len(self.food_items)):
            self.food_items[i] = self.food_items[i].move(*self.food_velocities[i])
            rect = self.food_items[i]
            if rect.right >= WIDTH or rect.left <= 0:
                self.food_velocities[i][0] *= -1
            if rect.bottom >= HEIGHT or rect.top <= 0:
                self.food_velocities[i][1] *= -1
            if self.snake and self.snake[0].colliderect(rect):
                rect.x, rect.y = random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20)
                self.snake_length += 3
                self.snake_lives = min(self.snake_lives + 1, 10)
                tail = self.snake[-1].copy()
                for _ in range(3):
                    self.snake.append(tail.copy())

        if self.magic_item and self.ludzik.colliderect(self.magic_item):
            self.has_magic_item = True
            self.magic_item = None

        if self.has_magic_item and self.exit_door and self.ludzik.colliderect(self.exit_door):
            self.manager.unlocked_scenes["8bit"] = True
            self.manager.load_scene("hub")

    def draw(self, screen):
        offset_x, offset_y = (0, 0)
        if self.glitch_timer % 10 < 3:
            offset_x, offset_y = random.randint(-5, 5), random.randint(-5, 5)
            screen.fill((random.randint(0,30), random.randint(0,30), random.randint(0,30)))
        else:
            screen.fill((0, 0, 0))

        screen.blit(self.font.render(f"Punkty: {self.score}", True, WHITE), (10, 10))
        screen.blit(self.font.render(f"Amunicja: {self.bullet_ready}", True, WHITE), (10, 40))
        screen.blit(self.font.render(f"Życia węża: {self.snake_lives}", True, WHITE), (10, 70))

        for o in self.obstacles:
            screen.blit(self.obstacle_img, o)

        pygame.draw.rect(screen, YELLOW, self.ludzik.move(offset_x, offset_y))

        for s in self.snake:
            pygame.draw.rect(screen, GREEN, s.move(offset_x, offset_y))

        for i, veggie in enumerate(self.veggies):
            screen.blit(self.fruit_imgs[self.veggie_types[i]], veggie.move(offset_x, offset_y))

        for bullet, _ in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet.move(offset_x, offset_y))

        for idx, food in enumerate(self.food_items):
            direction = self.mouse_directions[idx]
            frame = (self.mouse_anim_timer // 10) % 2
            mouse_img = self.mouse_imgs[direction][frame]
            screen.blit(mouse_img, food.move(offset_x, offset_y))

        if self.magic_item:
            pygame.draw.rect(screen, MAGIC, self.magic_item.move(offset_x, offset_y))
        if self.exit_door:
            pygame.draw.rect(screen, CYAN, self.exit_door)
