import pygame

# Ustawienia gry
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 40
UI_HEIGHT = 60
MOVE_COOLDOWN = 5 # Cooldown ruchu w klatkach
BG_COLOR = (40, 40, 40)
WALL_COLOR = (100, 100, 100)

# Kolory gracza i ceny
PLAYER_COLORS = {
    "Czerwony": (255, 0, 0),
    "Niebieski": (0, 120, 200),
    "Zielony": (0, 255, 0),
    "Żółty": (255, 255, 0),
    "Fioletowy": (128, 0, 128),
    "Różowy": (255, 105, 180),
}
SKIN_PRICES = {
    "Niebieski": 10,
    "Zielony": 15,
    "Żółty": 15,
    "Fioletowy": 25,
    "Różowy": 25,
}
DEFAULT_COLOR = "Czerwony"

# Konsola developerska
CONSOLE_BG_COLOR = (30, 30, 50)
CONSOLE_TEXT_COLOR = (200, 200, 200)
CONSOLE_HOTKEY = (pygame.K_j, pygame.KMOD_SHIFT)

# Monety
COIN_COLOR = (255, 215, 0)
COIN_SIZE = 15
COIN_DURATION = 600

# Ustawienia AI
AI_AGENT_COUNT = 50