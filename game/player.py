import pygame
from settings import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, 50, TILE_SIZE, TILE_SIZE)
        self.speed = TILE_SIZE
        self.move_cooldown = 0

    def handle_event(self, event):
        if self.move_cooldown <= 0:
            if event.key == pygame.K_w:
                self.rect.y -= self.speed
                self.move_cooldown = 10
            elif event.key == pygame.K_s:
                self.rect.y += self.speed
                self.move_cooldown = 10
            elif event.key == pygame.K_a:
                self.rect.x -= self.speed
                self.move_cooldown = 10
            elif event.key == pygame.K_d:
                self.rect.x += self.speed
                self.move_cooldown = 10

    def update_position(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 120, 200), self.rect)