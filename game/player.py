import pygame
from .settings import *

class Player:
    def __init__(self, walls, holes=None):
        self.speed = TILE_SIZE
        self.move_cooldown = 0
        self.walls = walls
        self.holes = holes if holes else []
        self.color = PLAYER_COLORS[DEFAULT_COLOR]
        self.rect = pygame.Rect(50, UI_HEIGHT + 50, TILE_SIZE, TILE_SIZE)
        self.teleport_cooldown = 0
        self.moving = {'up': False, 'down': False, 'left': False, 'right': False}

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moving['up'] = True
            elif event.key == pygame.K_s:
                self.moving['down'] = True
            elif event.key == pygame.K_a:
                self.moving['left'] = True
            elif event.key == pygame.K_d:
                self.moving['right'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moving['up'] = False
            elif event.key == pygame.K_s:
                self.moving['down'] = False
            elif event.key == pygame.K_a:
                self.moving['left'] = False
            elif event.key == pygame.K_d:
                self.moving['right'] = False

    def update_position(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        moved = False
        old_pos = self.rect.x, self.rect.y

        if self.moving['up']:
            self.rect.y -= self.speed
            moved = True
        elif self.moving['down']:
            self.rect.y += self.speed
            moved = True
        if self.moving['left']:
            self.rect.x -= self.speed
            moved = True
        elif self.moving['right']:
            self.rect.x += self.speed
            moved = True

        if moved:
            if any(self.rect.colliderect(wall) for wall in self.walls):
                self.rect.x, self.rect.y = old_pos
            else:
                self.move_cooldown = MOVE_COOLDOWN

        if self.teleport_cooldown <= 0 and self.holes:
            for hole in self.holes:
                if self.rect.colliderect(hole):
                    new_x = SCREEN_WIDTH - self.rect.x - TILE_SIZE
                    new_y = SCREEN_HEIGHT - self.rect.y - TILE_SIZE
                    self.rect.x = max(0, min(new_x, SCREEN_WIDTH - TILE_SIZE))
                    self.rect.y = max(UI_HEIGHT, min(new_y, SCREEN_HEIGHT - TILE_SIZE))
                    self.teleport_cooldown = 10
                    break
        else:
            self.teleport_cooldown -= 1

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(UI_HEIGHT, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def set_color(self, color):
        self.color = color