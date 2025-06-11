import pygame
import random
from .settings import *
from .maze_presets import ALL_MAZES

class Map:
    def __init__(self, map_name="Początek"):
        self.tile_size = TILE_SIZE
        self.walls = []
        self.holes = []
        self.generate_map(map_name)

    def generate_map(self, map_name):
        if map_name in ALL_MAZES:
            self.maze_data = ALL_MAZES[map_name]
        else:
            # W razie błędu załaduj pierwszą mapę z listy
            default_map_key = list(ALL_MAZES.keys())[0]
            self.maze_data = ALL_MAZES[default_map_key]
      
        # Dodaj dziury (10% szans)
        for y in range(1, len(self.maze_data)-1):
            row = list(self.maze_data[y])
            for x in range(1, len(row)-1):
                if row[x] == '1' and random.random() < 0.1:
                    row[x] = '2'
            self.maze_data[y] = ''.join(row)
      
        self.convert_to_rects()

    def convert_to_rects(self):
        self.walls = []
        self.holes = []
        for y in range(len(self.maze_data)):
            for x in range(len(self.maze_data[0])):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size + UI_HEIGHT,
                    self.tile_size,
                    self.tile_size
                )
                if self.maze_data[y][x] == '1':
                    self.walls.append(rect)
                elif self.maze_data[y][x] == '2':
                    self.holes.append(rect)

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for hole in self.holes:
            pygame.draw.rect(screen, (70, 70, 90), hole)