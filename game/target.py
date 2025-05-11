import pygame
import random
from settings import *

class Target:
    def __init__(self, walls, holes=None):
        self.size = TILE_SIZE
        self.color = TARGET_COLOR
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)