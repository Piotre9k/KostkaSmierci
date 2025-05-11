import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background_alpha = 0
        self.title_alpha = 0
        self.button_alpha = 0
        
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 36)
        
        self.play_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT // 2 + 50, 
            200, 50
        )

    def animate(self):
        self.background_alpha = min(self.background_alpha + 3, 180)
        if self.background_alpha > 30:
            self.title_alpha = min(self.title_alpha + 5, 255)
        if self.title_alpha > 100:
            self.button_alpha = min(self.button_alpha + 7, 255)

    def draw(self):
        self.screen.fill((0, 0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((20, 20, 30))
        overlay.set_alpha(255 - self.background_alpha)
        self.screen.blit(overlay, (0, 0))
        
        title = self.title_font.render("KOSTKA ŚMIERCI", True, (220, 30, 30))
        title.set_alpha(self.title_alpha)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70))
        self.screen.blit(title, title_rect)
        
        button_color = (50, 50, 80) if not self.play_button.collidepoint(pygame.mouse.get_pos()) else (80, 80, 120)
        pygame.draw.rect(self.screen, button_color, self.play_button, border_radius=8)
        
        button_text = self.button_font.render("GRAJ", True, (240, 240, 240))
        button_text.set_alpha(self.button_alpha)
        text_rect = button_text.get_rect(center=self.play_button.center)
        self.screen.blit(button_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.button_alpha == 255:
                    if self.play_button.collidepoint(event.pos):
                        return True
            
            self.animate()
            self.draw()
            self.clock.tick(60)