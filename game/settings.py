import pygame  # Dodaj tę linię na początku pliku

# Ustawienia gry
SCREEN_WIDTH = 1000  # Zwiększona szerokość dla statystyk AI
SCREEN_HEIGHT = 700  # Zwiększona wysokość
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

# Ustawienia AI
AI_AGENT_COUNT = 20  # Domyślna liczba agentów
AI_TRAINING_MODES = {
    "Podstawowy": 10,
    "Średni": 30,
    "Zaawansowany": 50
}

# Dodaj nowe ustawienia labiryntów
MAZE_TYPES = {
    "BASIC": "Podstawowy",
    "CROSS": "Krzyż",
    "ROOMS": "Pokoje", 
    "SPIRAL": "Spirala",
    "RANDOM": "Losowy",
    "TRAIN_1": "Treningowy 1",
    "TRAIN_2": "Treningowy 2"
}

# Rozmiary labiryntów
MAZE_SIZES = {
    "SMALL": (16, 11),  # Standardowy rozmiar
    "MEDIUM": (23, 23), # Dla przyszłego edytora
    "LARGE": (32, 32)   # Dla zaawansowanych
}

# Wybór domyślnego
DEFAULT_MAZE_TYPE = "BASIC"
DEFAULT_MAZE_SIZE = "SMALL"