import pygame
import random
from settings import *

class Map:
    def __init__(self, map_type=None):
        self.tile_size = TILE_SIZE
        self.walls = []
        self.holes = []
        self.transition_alpha = 255
        self.is_transitioning = False
        self.map_type = map_type if map_type else random.choice(MAP_TYPES)
        self.generate_map()

    def generate_map(self):
        base_map = [
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

        if self.map_type == "SPECJALNA":
            base_map = [
                "1111111111111111",
                "1000000000000001",
                "1020000000000201",
                "1002000000020001",
                "1000000000000001",
                "1000000000000001",
                "1000000000000001",
                "1002000000020001",
                "1020000000000201",
                "1000000000000001",
                "1111111111111111"
            ]

        self.map_data = base_map
        self.generate_walls_and_holes()

    def generate_walls_and_holes(self):
        self.walls = []
        self.holes = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size + UI_HEIGHT,
                    self.tile_size,
                    self.tile_size
                )
                if tile == "1":
                    self.walls.append(rect)
                elif tile == "2":
                    self.holes.append(rect)

    def start_transition(self):
        self.is_transitioning = True
        self.transition_alpha = 0

    def update_transition(self):
        if self.is_transitioning:
            self.transition_alpha += 255 // TRANSITION_DURATION
            if self.transition_alpha >= 255:
                self.is_transitioning = False

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for hole in self.holes:
            pygame.draw.rect(screen, (70, 70, 90), hole)
        
        if self.is_transitioning:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - self.transition_alpha)
            screen.blit(overlay, (0, 0))