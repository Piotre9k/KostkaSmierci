# Ustawienia gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 50
BG_COLOR = (40, 40, 40)
WALL_COLOR = (100, 100, 100)
UI_HEIGHT = 50
TARGET_COLOR = (0, 255, 0)
MOVE_COOLDOWN = 10
TRANSITION_DURATION = 30

# Kolory gracza
PLAYER_COLORS = {
    "Czerwony": (255, 0, 0),
    "Niebieski": (0, 120, 200),
    "Zielony": (0, 255, 0),
    "Żółty": (255, 255, 0),
    "Fioletowy": (128, 0, 128),
    "Różowy": (255, 105, 180),
    "Tęcza": "rainbow"
}
DEFAULT_COLOR = "Czerwony"

# Typy map
MAP_TYPES = ["LABIRYNT", "KRZYŻ", "POKOJ", "TUNEL", "SPECJALNA"]

# Monety
COIN_COLOR = (255, 215, 0)
COIN_SIZE = 15
COIN_DURATION = 600  # czas w klatkach (5 sekund przy 60 FPS)

# Konsola developerska
CONSOLE_BG_COLOR = (30, 30, 50)
CONSOLE_TEXT_COLOR = (200, 200, 200)
CONSOLE_HOTKEY = (pygame.K_j, pygame.KMOD_SHIFT)  # SHIFT + J