import pygame
from settings import *

class UI:
    def __init__(self):
        self.score = 0
        self.coins = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.skin_font = pygame.font.SysFont("Arial", 20)
        self.show_skins = False
        self.show_shop = False
        self.current_color = DEFAULT_COLOR
        self.rainbow_counter = 0
        self.skin_button = pygame.Rect(SCREEN_WIDTH - 100, 10, 80, 30)
        self.shop_button = pygame.Rect(SCREEN_WIDTH - 200, 10, 80, 30)

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
        
        pygame.draw.rect(screen, (80, 80, 100), self.shop_button, border_radius=5)
        shop_text = self.skin_font.render("Sklep ▼" if self.show_shop else "Sklep ▲", True, (255, 255, 255))
        screen.blit(shop_text, (self.shop_button.x + 10, self.shop_button.y + 5))
        
        if self.show_skins:
            self.draw_skin_menu(screen)
        
        if self.show_shop:
            self.draw_shop_menu(screen)

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

    def draw_shop_menu(self, screen):
        shop_menu = pygame.Rect(SCREEN_WIDTH - 250, 45, 240, len(PLAYER_COLORS) * 30 + 10)
        pygame.draw.rect(screen, (60, 60, 80), shop_menu, border_radius=5)
        
        for i, (name, color) in enumerate(PLAYER_COLORS.items()):
            option_rect = pygame.Rect(shop_menu.x + 10, shop_menu.y + 10 + i*30, 220, 25)
            
            if name == self.current_color:
                pygame.draw.rect(screen, (90, 90, 110), option_rect, border_radius=3)
            
            cube_rect = pygame.Rect(option_rect.x + 5, option_rect.y + 5, 15, 15)
            if color == "rainbow":
                self.draw_rainbow_effect(screen, cube_rect)
            else:
                pygame.draw.rect(screen, color, cube_rect)
            
            price = COLOR_PRICES[name]
            can_afford = self.coins >= price
            color_text = (0, 255, 0) if can_afford else (255, 0, 0)
            
            name_text = self.skin_font.render(f"{name} - {price}", True, color_text)
            screen.blit(name_text, (option_rect.x + 25, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skin_button.collidepoint(event.pos):
                self.show_skins = not self.show_skins
                self.show_shop = False
                return None
            elif self.shop_button.collidepoint(event.pos):
                self.show_shop = not self.show_shop
                self.show_skins = False
                return None
            elif self.show_skins:
                mouse_pos = pygame.mouse.get_pos()
                for i, (name, color) in enumerate(PLAYER_COLORS.items()):
                    option_rect = pygame.Rect(SCREEN_WIDTH - 140, 55 + i*30, 120, 25)
                    if option_rect.collidepoint(mouse_pos):
                        self.current_color = name
                        self.show_skins = False
                        return name
            elif self.show_shop:
                mouse_pos = pygame.mouse.get_pos()
                for i, (name, color) in enumerate(PLAYER_COLORS.items()):
                    option_rect = pygame.Rect(SCREEN_WIDTH - 240, 55 + i*30, 220, 25)
                    if option_rect.collidepoint(mouse_pos) and self.coins >= COLOR_PRICES[name]:
                        self.coins -= COLOR_PRICES[name]
                        self.current_color = name
                        self.show_shop = False
                        return name
        return None

    def get_current_color(self):
        if self.current_color == "Tęcza":
            colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), 
                     (0,0,255), (75,0,130), (148,0,211)]
            return colors[self.rainbow_counter // 5 % len(colors)]
        return PLAYER_COLORS[self.current_color]