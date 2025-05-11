import pygame
from settings import *

class Player:
    def __init__(self, walls):
        self.speed = TILE_SIZE
        self.move_cooldown = 0
        self.walls = walls  # Zapamiętujemy ściany
        self.rect = pygame.Rect(0, UI_HEIGHT, TILE_SIZE, TILE_SIZE)
        
        # Szukanie wolnego miejsca na start
        self.find_valid_position()

    def find_valid_position(self):
        """Znajduje wolne miejsce dla gracza"""
        for y in range(UI_HEIGHT, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                self.rect.x = x
                self.rect.y = y
                if not self.check_collision():
                    return
        # Jeśli nie znajdzie, ustaw w domyślnym miejscu
        self.rect.x = TILE_SIZE
        self.rect.y = UI_HEIGHT + TILE_SIZE

    def check_collision(self):
        """Sprawdza kolizję ze ścianami"""
        return any(self.rect.colliderect(wall) for wall in self.walls)

    def handle_event(self, event):
        if self.move_cooldown > 0:
            return

        # Zapamiętaj starą pozycję
        old_x, old_y = self.rect.x, self.rect.y

        if event.key == pygame.K_w:
            self.rect.y -= self.speed
        elif event.key == pygame.K_s:
            self.rect.y += self.speed
        elif event.key == pygame.K_a:
            self.rect.x -= self.speed
        elif event.key == pygame.K_d:
            self.rect.x += self.speed
        else:
            return  # Nieznany klawisz

        # Sprawdź kolizję
        if self.check_collision():
            # Cofnij ruch jeśli kolizja
            self.rect.x, self.rect.y = old_x, old_y
        else:
            self.move_cooldown = MOVE_COOLDOWN

    def update_position(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        # Ograniczenia ekranu
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(UI_HEIGHT, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)