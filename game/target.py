import pygame
import random
from .settings import *

class Target:
    def __init__(self, walls, holes=None):
        self.size = TILE_SIZE
        self.colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]  # Zielony, Niebieski, Czerwony
        self.current_color_index = random.randint(0, len(self.colors)-1)
        self.color = self.colors[self.current_color_index]
        self.rect = self.get_valid_position(walls, holes if holes else [])

    def get_valid_position(self, walls, holes):
        safe_zone = pygame.Rect(
            2*TILE_SIZE, 
            UI_HEIGHT + 2*TILE_SIZE,
            SCREEN_WIDTH - 4*TILE_SIZE,
            SCREEN_HEIGHT - UI_HEIGHT - 4*TILE_SIZE
        )
        
        free_cells = []
        for y in range(safe_zone.y, safe_zone.y + safe_zone.height, TILE_SIZE):
            for x in range(safe_zone.x, safe_zone.x + safe_zone.width, TILE_SIZE):
                cell = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                wall_collision = any(cell.colliderect(wall) for wall in walls)
                hole_collision = any(cell.colliderect(hole) for hole in holes)
                if not wall_collision and not hole_collision:
                    free_cells.append(cell)
        
        return random.choice(free_cells) if free_cells else pygame.Rect(
            SCREEN_WIDTH//2, SCREEN_HEIGHT//2, TILE_SIZE, TILE_SIZE)

    def change_color(self):
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.color = self.colors[self.current_color_index]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
        self.lifetime = COIN_DURATION
        self.collected = False

    def update(self):
        if not self.collected:
            self.lifetime -= 1
            return self.lifetime > 0
        return False

    def draw(self, screen):
        if not self.collected and self.lifetime > 0:
            pygame.draw.circle(screen, COIN_COLOR, (self.x + COIN_SIZE//2, self.y + COIN_SIZE//2), COIN_SIZE//2)