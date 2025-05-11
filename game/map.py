import os
import pygame
from settings import *

class Map:
    def __init__(self):
        self.tile_size = TILE_SIZE
        self.walls = []
        self.load_map()

    def get_map_path(self):
        """Zwraca ścieżkę do mapy w wersji developerskiej i skompilowanej"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "assets", "map.txt")

    def load_map(self):
        try:
            map_path = self.get_map_path()
            if os.path.exists(map_path):
                with open(map_path, "r") as f:
                    self.map_data = [line.strip() for line in f if line.strip()]
            else:
                raise FileNotFoundError
        except:
            self.map_data = [
                "1111111111111111",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1111111111111111"
            ]

        self.generate_walls()

    def generate_walls(self):
        self.walls = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == "1":
                    wall = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size + UI_HEIGHT,
                        self.tile_size,
                        self.tile_size
                    )
                    self.walls.append(wall)

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)