import pygame
from settings import *

class UI:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)

    def update_score(self, points):
        self.score += points

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, UI_HEIGHT))
        text = self.font.render(f"Punkty: {self.score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))