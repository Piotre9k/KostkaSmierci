import pygame
import random
from settings import *

class Target:
    def __init__(self, walls):
        self.size = TILE_SIZE
        self.color = TARGET_COLOR
        self.rect = self.get_valid_position(walls)

    def get_valid_position(self, walls):
        free_cells = []
        
        # Sprawdź wszystkie możliwe pozycje (z pominięciem paska UI)
        for y in range(UI_HEIGHT, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                cell = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                if not any(cell.colliderect(wall) for wall in walls):
                    free_cells.append(cell)
        
        return random.choice(free_cells) if free_cells else pygame.Rect(0, UI_HEIGHT, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)