import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.scene_manager import SceneManager
from settings import WIDTH, HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro World: Ludzik vs Wąż")
    clock = pygame.time.Clock()
    manager = SceneManager()
    manager.load_scene("hub")

    running = True
    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.update(keys, events)
        manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
