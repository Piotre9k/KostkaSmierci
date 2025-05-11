import pygame
from settings import *

class Player:
    def __init__(self):
        self.reset_position()
        self.move_cooldown = 0

    def reset_position(self):
        self.rect = pygame.Rect(
            2 * TILE_SIZE,
            6 * TILE_SIZE + UI_HEIGHT,
            TILE_SIZE,
            TILE_SIZE
        )
        self.color = PLAYER_COLOR
        self.move_request = None

    def move(self, keys, walls):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        # Zapamiętanie żądania ruchu
        if keys[pygame.K_LEFT]: self.move_request = (-TILE_SIZE, 0)
        elif keys[pygame.K_RIGHT]: self.move_request = (TILE_SIZE, 0)
        elif keys[pygame.K_UP]: self.move_request = (0, -TILE_SIZE)
        elif keys[pygame.K_DOWN]: self.move_request = (0, TILE_SIZE)
        else: return

        new_x = self.rect.x + self.move_request[0]
        new_y = self.rect.y + self.move_request[1]

        # Ograniczenia ekranu
        new_x = max(0, min(new_x, SCREEN_WIDTH - TILE_SIZE))
        new_y = max(UI_HEIGHT, min(new_y, SCREEN_HEIGHT - TILE_SIZE))

        # Sprawdzenie kolizji
        temp_rect = pygame.Rect(new_x, new_y, TILE_SIZE, TILE_SIZE)
        if not any(temp_rect.colliderect(wall) for wall in walls):
            self.rect = temp_rect
            self.move_cooldown = 10  # Opóźnienie między ruchami

        self.move_request = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)