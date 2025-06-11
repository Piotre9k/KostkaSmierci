import pygame
import json
from .settings import *

class UI:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.skin_font = pygame.font.SysFont("Arial", 18)
        self.shop_font = pygame.font.SysFont("Arial", 16)
        
        self.show_shop = False
        self.shop_button = pygame.Rect(SCREEN_WIDTH - 120, 10, 100, 40)
        self.current_color_name = DEFAULT_COLOR
        
        # Dane gry
        self.coins = 0
        self.owned_skins = []
        self.load_game_data()

    def load_game_data(self):
        try:
            with open('save.json', 'r') as f:
                data = json.load(f)
                self.coins = data.get('coins', 0)
                self.owned_skins = data.get('owned_skins', [DEFAULT_COLOR])
                self.current_color_name = self.owned_skins[0]
        except (FileNotFoundError, json.JSONDecodeError):
            self.coins = 0
            self.owned_skins = [DEFAULT_COLOR]
            self.save_game_data()

    def save_game_data(self):
        data = {
            'coins': self.coins,
            'owned_skins': self.owned_skins
        }
        with open('save.json', 'w') as f:
            json.dump(data, f, indent=2)

    def update_score(self, points):
        self.score += points

    def add_coins(self, amount):
        self.coins += amount
        self.save_game_data()

    def get_current_color(self):
        return PLAYER_COLORS.get(self.current_color_name, PLAYER_COLORS[DEFAULT_COLOR])

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 70), (0, 0, SCREEN_WIDTH, UI_HEIGHT))
        
        score_text = self.font.render(f"Punkty: {self.score:03d}", True, (255, 255, 255))
        coins_text = self.font.render(f"Monety: {self.coins:03d}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(coins_text, (200, 20))
        
        # Przycisk sklepu
        pygame.draw.rect(screen, (80, 80, 100), self.shop_button, border_radius=5)
        shop_text = self.skin_font.render("Sklep", True, (255, 255, 255))
        screen.blit(shop_text, (self.shop_button.x + 25, self.shop_button.y + 10))
        
        if self.show_shop:
            self.draw_shop(screen)

    def draw_shop(self, screen):
        shop_rect = pygame.Rect(self.shop_button.left - 150, self.shop_button.bottom + 5, 250, 300)
        pygame.draw.rect(screen, (60, 60, 80), shop_rect, border_radius=5)
        
        y_offset = shop_rect.y + 10
        for name, color in PLAYER_COLORS.items():
            item_rect = pygame.Rect(shop_rect.x + 10, y_offset, shop_rect.width - 20, 35)
            
            # Kolor
            pygame.draw.rect(screen, color, (item_rect.x + 5, item_rect.y + 7, 20, 20))
            name_text = self.shop_font.render(name, True, (255, 255, 255))
            screen.blit(name_text, (item_rect.x + 35, item_rect.y + 10))

            # Przycisk
            button_rect = pygame.Rect(item_rect.right - 80, item_rect.y + 5, 75, 25)
            
            if name in self.owned_skins:
                is_selected = (name == self.current_color_name)
                btn_color = (60, 120, 60) if is_selected else (80, 80, 100)
                btn_text = "Wybrany" if is_selected else "Wybierz"
                pygame.draw.rect(screen, btn_color, button_rect, border_radius=3)
            else:
                price = SKIN_PRICES.get(name, 999)
                btn_text = f"Kup ({price})"
                can_afford = self.coins >= price
                btn_color = (60, 90, 60) if can_afford else (120, 60, 60)
                pygame.draw.rect(screen, btn_color, button_rect, border_radius=3)
            
            text_render = self.shop_font.render(btn_text, True, (255, 255, 255))
            screen.blit(text_render, (button_rect.x + 5, button_rect.y + 5))
            
            y_offset += 40

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shop_button.collidepoint(event.pos):
                self.show_shop = not self.show_shop
                return None

            if self.show_shop:
                shop_rect = pygame.Rect(self.shop_button.left - 150, self.shop_button.bottom + 5, 250, 300)
                if not shop_rect.collidepoint(event.pos):
                    self.show_shop = False
                    return None

                y_offset = shop_rect.y + 10
                for name, _ in PLAYER_COLORS.items():
                    button_rect = pygame.Rect(shop_rect.right - 90, y_offset + 5, 75, 25)
                    if button_rect.collidepoint(event.pos):
                        if name in self.owned_skins:
                            self.current_color_name = name
                        else:
                            price = SKIN_PRICES.get(name, 999)
                            if self.coins >= price:
                                self.coins -= price
                                self.owned_skins.append(name)
                                self.current_color_name = name
                                self.save_game_data()
                        return self.get_current_color()
                    y_offset += 40
        return None