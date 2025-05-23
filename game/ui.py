import pygame
from .settings import *

class UI:
    def __init__(self):
        self.score = 0
        self.coins = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.skin_font = pygame.font.SysFont("Arial", 20)
        self.show_skins = False
        self.current_color = DEFAULT_COLOR
        self.rainbow_counter = 0
        self.skin_button = pygame.Rect(SCREEN_WIDTH - 100, 10, 80, 30)
        
        self.ai_toggle = False
        self.ai_button = pygame.Rect(SCREEN_WIDTH - 220, 10, 110, 30)
        self.ai_start_button = pygame.Rect(SCREEN_WIDTH - 350, 10, 60, 30)
        self.ai_stop_button = pygame.Rect(SCREEN_WIDTH - 280, 10, 60, 30)
        self.ai_settings_button = pygame.Rect(SCREEN_WIDTH - 430, 10, 70, 30)
        self.show_ai_settings = False
        self.ai_agent_count = AI_AGENT_COUNT

    def update_score(self, points):
        self.score += points

    def add_coins(self, amount):
        self.coins += amount

    def draw_rainbow_effect(self, screen, rect):
        colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
        ]
        color = colors[self.rainbow_counter // 5 % len(colors)]
        pygame.draw.rect(screen, color, rect)
        self.rainbow_counter += 1

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 70), (0, 0, SCREEN_WIDTH, UI_HEIGHT))
        
        score_text = self.font.render(f"Punkty: {self.score:03d}", True, (255, 255, 255))
        coins_text = self.font.render(f"Monety: {self.coins:03d}", True, (255, 255, 255))
        pygame.draw.line(screen, (100, 100, 100), (120, 10), (120, UI_HEIGHT - 10), 2)
        pygame.draw.line(screen, (100, 100, 100), (250, 10), (250, UI_HEIGHT - 10), 2)
        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (130, 10))
        
        pygame.draw.rect(screen, (80, 80, 100), self.skin_button, border_radius=5)
        skin_text = self.skin_font.render("Skin ▼" if self.show_skins else "Skin ▲", True, (255, 255, 255))
        screen.blit(skin_text, (self.skin_button.x + 10, self.skin_button.y + 5))
        
        pygame.draw.rect(screen, (90, 60, 60) if self.ai_toggle else (60, 60, 90), self.ai_button, border_radius=5)
        ai_text = self.skin_font.render("AI: ON" if self.ai_toggle else "AI: OFF", True, (255, 255, 255))
        screen.blit(ai_text, (self.ai_button.x + 10, self.ai_button.y + 5))
        
        if self.ai_toggle:
            pygame.draw.rect(screen, (60, 90, 60), self.ai_start_button, border_radius=5)
            start_text = self.skin_font.render("Start", True, (255, 255, 255))
            screen.blit(start_text, (self.ai_start_button.x + 10, self.ai_start_button.y + 5))
            
            pygame.draw.rect(screen, (90, 60, 60), self.ai_stop_button, border_radius=5)
            stop_text = self.skin_font.render("Stop", True, (255, 255, 255))
            screen.blit(stop_text, (self.ai_stop_button.x + 10, self.ai_stop_button.y + 5))
            
            pygame.draw.rect(screen, (80, 80, 100), self.ai_settings_button, border_radius=5)
            settings_text = self.skin_font.render("Ustaw", True, (255, 255, 255))
            screen.blit(settings_text, (self.ai_settings_button.x + 10, self.ai_settings_button.y + 5))
        
        if self.show_skins:
            self.draw_skin_menu(screen)
            
        if self.show_ai_settings:
            self.draw_ai_settings(screen)

    def draw_skin_menu(self, screen):
        skin_menu = pygame.Rect(SCREEN_WIDTH - 150, 45, 140, len(PLAYER_COLORS) * 30 + 10)
        pygame.draw.rect(screen, (60, 60, 80), skin_menu, border_radius=5)
        
        for i, (name, color) in enumerate(PLAYER_COLORS.items()):
            option_rect = pygame.Rect(skin_menu.x + 10, skin_menu.y + 10 + i*30, 120, 25)
            
            if name == self.current_color:
                pygame.draw.rect(screen, (90, 90, 110), option_rect, border_radius=3)
            
            cube_rect = pygame.Rect(option_rect.x + 5, option_rect.y + 5, 15, 15)
            if color == "rainbow":
                self.draw_rainbow_effect(screen, cube_rect)
            else:
                pygame.draw.rect(screen, color, cube_rect)
            
            name_text = self.skin_font.render(name, True, (255, 255, 255))
            screen.blit(name_text, (option_rect.x + 25, option_rect.y + 5))

    def draw_ai_settings(self, screen):
        settings_menu = pygame.Rect(SCREEN_WIDTH - 450, 45, 430, 150)
        pygame.draw.rect(screen, (60, 60, 80), settings_menu, border_radius=5)
        
        title = self.skin_font.render("Ustawienia AI:", True, (255, 255, 255))
        screen.blit(title, (settings_menu.x + 10, settings_menu.y + 10))
        
        agents_text = self.skin_font.render(f"Liczba agentów: {self.ai_agent_count}", True, (255, 255, 255))
        screen.blit(agents_text, (settings_menu.x + 10, settings_menu.y + 40))
        
        plus_button = pygame.Rect(settings_menu.x + 200, settings_menu.y + 40, 30, 25)
        minus_button = pygame.Rect(settings_menu.x + 150, settings_menu.y + 40, 30, 25)
        
        pygame.draw.rect(screen, (60, 90, 60), plus_button, border_radius=3)
        pygame.draw.rect(screen, (90, 60, 60), minus_button, border_radius=3)
        
        plus_text = self.skin_font.render("+", True, (255, 255, 255))
        minus_text = self.skin_font.render("-", True, (255, 255, 255))
        
        screen.blit(plus_text, (plus_button.x + 10, plus_button.y + 5))
        screen.blit(minus_text, (minus_button.x + 10, minus_button.y + 5))
        
        for i, (name, count) in enumerate(AI_TRAINING_MODES.items()):
            profile_button = pygame.Rect(settings_menu.x + 10 + i*140, settings_menu.y + 80, 130, 30)
            pygame.draw.rect(screen, (70, 70, 100), profile_button, border_radius=5)
            profile_text = self.skin_font.render(f"{name}: {count}", True, (255, 255, 255))
            screen.blit(profile_text, (profile_button.x + 10, profile_button.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skin_button.collidepoint(event.pos):
                self.show_skins = not self.show_skins
                self.show_ai_settings = False
                return None
            elif self.ai_button.collidepoint(event.pos):
                self.ai_toggle = not self.ai_toggle
                self.show_skins = False
            elif self.ai_toggle and self.ai_settings_button.collidepoint(event.pos):
                self.show_ai_settings = not self.show_ai_settings
                self.show_skins = False
            elif self.show_skins:
                mouse_pos = pygame.mouse.get_pos()
                for i, (name, color) in enumerate(PLAYER_COLORS.items()):
                    option_rect = pygame.Rect(SCREEN_WIDTH - 140, 55 + i*30, 120, 25)
                    if option_rect.collidepoint(mouse_pos):
                        self.current_color = name
                        self.show_skins = False
                        return name
            elif self.show_ai_settings:
                mouse_pos = pygame.mouse.get_pos()
                
                plus_button = pygame.Rect(SCREEN_WIDTH - 450 + 200, 45 + 40, 30, 25)
                minus_button = pygame.Rect(SCREEN_WIDTH - 450 + 150, 45 + 40, 30, 25)
                
                if plus_button.collidepoint(mouse_pos):
                    self.ai_agent_count = min(100, self.ai_agent_count + 5)
                elif minus_button.collidepoint(mouse_pos):
                    self.ai_agent_count = max(5, self.ai_agent_count - 5)
                
                for i, (name, count) in enumerate(AI_TRAINING_MODES.items()):
                    profile_button = pygame.Rect(SCREEN_WIDTH - 450 + 10 + i*140, 45 + 80, 130, 30)
                    if profile_button.collidepoint(mouse_pos):
                        self.ai_agent_count = count
                        
        return None

    def get_current_color(self):
        if self.current_color == "Tęcza":
            colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), 
                     (0,0,255), (75,0,130), (148,0,211)]
            return colors[self.rainbow_counter // 5 % len(colors)]
        return PLAYER_COLORS[self.current_color]