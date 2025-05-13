import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.scene_manager import SceneManager
from settings import WIDTH, HEIGHT

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Time Glitch Game")
    clock = pygame.time.Clock()
    manager = SceneManager()
    current_scene_name = "hub"
    manager.load_scene(current_scene_name)

    def load_music(scene_name):
        music_path = f"assets/music/{scene_name}.mp3"
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    load_music(current_scene_name)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        previous_scene_name = current_scene_name
        manager.update(keys, events)
        current_scene_name = manager.current_scene_name

        if previous_scene_name != current_scene_name:
            load_music(current_scene_name)

        manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
