import pygame
from settings import *

class Player:
    def __init__(self, walls, holes=None):
        self.speed = TILE_SIZE
        self.move_cooldown = 0
        self.walls = walls
        self.holes = holes if holes else []
        self.color = PLAYER_COLORS[DEFAULT_COLOR]
        self.rect = pygame.Rect(50, UI_HEIGHT + 50, TILE_SIZE, TILE_SIZE)
        self.teleport_cooldown = 0

    def handle_event(self, event):
        if self.move_cooldown > 0:
            return

        old_pos = self.rect.x, self.rect.y

        if event.key == pygame.K_w:
            self.rect.y -= self.speed
        elif event.key == pygame.K_s:
            self.rect.y += self.speed
        elif event.key == pygame.K_a:
            self.rect.x -= self.speed
        elif event.key == pygame.K_d:
            self.rect.x += self.speed

        if any(self.rect.colliderect(wall) for wall in self.walls):
            self.rect.x, self.rect.y = old_pos
        else:
            self.move_cooldown = MOVE_COOLDOWN

    def update_position(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

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
        if color in PLAYER_COLORS.values():
            self.color = color
        elif color == "rainbow":
            colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
            self.color = colors[pygame.time.get_ticks() // 200 % len(colors)]