import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Efekty wizualne
        self.background_alpha = 0
        self.title_alpha = 0
        self.button_alpha = 0
        self.info_alpha = 0
        self.show_info = False
        
        # Czcionki
        self.title_font = pygame.font.SysFont('Arial', 72, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 42)
        self.info_font = pygame.font.SysFont('Arial', 24)
        
        # Przyciski
        self.play_button = pygame.Rect(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 + 50,
            200, 60
        )
        
        self.train_button = pygame.Rect(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 + 120,
            200, 60
        )
        
        self.info_button = pygame.Rect(
            SCREEN_WIDTH - 50,
            10,
            40, 40
        )

    def animate(self):
        # Animacja pojawiania się
        self.background_alpha = min(self.background_alpha + 3, 180)
        if self.background_alpha > 30:
            self.title_alpha = min(self.title_alpha + 5, 255)
        if self.title_alpha > 100:
            self.button_alpha = min(self.button_alpha + 7, 255)
            
        if self.show_info:
            self.info_alpha = min(self.info_alpha + 10, 200)
        else:
            self.info_alpha = max(self.info_alpha - 10, 0)

    def draw(self):
        # Tło
        self.screen.fill((0, 0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((25, 25, 35))
        overlay.set_alpha(255 - self.background_alpha)
        self.screen.blit(overlay, (0, 0))
        
        # Tytuł
        title = self.title_font.render("KOSTKA ŚMIERCI", True, (220, 30, 30))
        title.set_alpha(self.title_alpha)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70))
        self.screen.blit(title, title_rect)
        
        # Przycisk gry
        button_color = (60, 60, 90) if not self.play_button.collidepoint(pygame.mouse.get_pos()) else (90, 90, 130)
        pygame.draw.rect(self.screen, button_color, self.play_button, border_radius=10)
        
        button_text = self.button_font.render("GRAJ", True, (255, 255, 255))
        button_text.set_alpha(self.button_alpha)
        text_rect = button_text.get_rect(center=self.play_button.center)
        self.screen.blit(button_text, text_rect)
        
        # Przycisk treningu
        train_color = (60, 90, 60) if not self.train_button.collidepoint(pygame.mouse.get_pos()) else (90, 130, 90)
        pygame.draw.rect(self.screen, train_color, self.train_button, border_radius=10)
        
        train_text = self.button_font.render("TRENUJ", True, (255, 255, 255))
        train_text.set_alpha(self.button_alpha)
        train_rect = train_text.get_rect(center=self.train_button.center)
        self.screen.blit(train_text, train_rect)
        
        # Przycisk informacji
        pygame.draw.rect(self.screen, (40, 40, 60), self.info_button, border_radius=20)
        info_text = self.button_font.render("?", True, (255, 255, 255))
        info_rect = info_text.get_rect(center=self.info_button.center)
        self.screen.blit(info_text, info_rect)
        
        # Informacja o trybie treningu
        if self.info_alpha > 0:
            info_box = pygame.Surface((400, 200))
            info_box.fill((30, 30, 50))
            info_box.set_alpha(self.info_alpha)
            self.screen.blit(info_box, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100))
            
            lines = [
                "Tryb treningu:",
                "- AI uczy się przechodzić labirynt",
                "- Wykorzystuje moc obliczeniową CPU",
                "- Każdy agent żyje 5 sekund",
                "- Najlepsi są selekcjonowani",
                "- Nowe pokolenia uczą się na błędach"
            ]
            
            for i, line in enumerate(lines):
                text = self.info_font.render(line, True, (255, 255, 255))
                text.set_alpha(self.info_alpha)
                self.screen.blit(text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 - 80 + i * 30))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False, False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.button_alpha == 255:
                    if self.play_button.collidepoint(event.pos):
                        return True, False
                    elif self.train_button.collidepoint(event.pos):
                        return True, True
                    elif self.info_button.collidepoint(event.pos):
                        self.show_info = not self.show_info
                
                if event.type == pygame.MOUSEMOTION:
                    if self.train_button.collidepoint(event.pos):
                        self.show_info = True
                    elif not self.info_button.collidepoint(event.pos):
                        self.show_info = False
            
            self.animate()
            self.draw()
            self.clock.tick(60)