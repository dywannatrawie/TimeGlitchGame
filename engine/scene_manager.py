import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hub.hub_world import HubWorld
from levels.level_4bit import Level4Bit
from levels.level_1bit import Level1Bit
from levels.level_8bit import Level8Bit  
import subprocess

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.unlocked_scenes = {
            "hub": True,
            "1bit": True,
            "4bit": False,
            "8bit": False,  # ⬅️ Pacman, zablokowany na start
            "16bit": False
        }
        self.tetris_process = None
        self.in_tetris = False

    def load_scene(self, scene_name):
        self.current_scene_name = scene_name
        if scene_name == "hub":
            self.current_scene = HubWorld(self)
        elif scene_name == "1bit":
            self.current_scene = Level1Bit(self)
        elif scene_name == "4bit":
            self.current_scene = Level4Bit(self)
        elif scene_name == "8bit":  # ⬅️ Dodano Pacmana
            self.current_scene = Level8Bit(self)
        # przyszłościowo:
        # elif scene_name == "16bit":
        #     self.current_scene = Level16Bit(self)

    def update(self, keys, events):
        if self.in_tetris:
            if self.tetris_process and self.tetris_process.poll() is not None:
                self.in_tetris = False
            return
        self.current_scene.update(keys, events)

    def draw(self, screen):
        if not self.in_tetris:
            self.current_scene.draw(screen)

    def launch_tetris(self):
        if not self.in_tetris:
            self.tetris_process = subprocess.Popen(["python", "tetris.py"])
            self.in_tetris = True
