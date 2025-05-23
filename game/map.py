import pygame
import random
from .settings import *
from .maze_presets import TRAINING_MAZES

class Map:
    def __init__(self, map_type=None, maze_size="SMALL"):
        self.tile_size = TILE_SIZE
        self.walls = []
        self.holes = []
        self.transition_alpha = 255
        self.is_transitioning = False
        self.map_type = map_type if map_type else DEFAULT_MAZE_TYPE
        self.maze_width, self.maze_height = MAZE_SIZES[maze_size]
        self.generate_map()

    def generate_map(self):
        if self.map_type in TRAINING_MAZES:
            self.load_preset_maze()
        else:
            if self.map_type == "BASIC":
                self.generate_basic_maze()
            elif self.map_type == "CROSS":
                self.generate_cross_maze()
            elif self.map_type == "ROOMS":
                self.generate_room_maze()
            elif self.map_type == "SPIRAL":
                self.generate_spiral_maze()
            elif self.map_type == "RANDOM":
                self.generate_random_maze()

        self.adjust_tile_size()
        self.convert_to_rects()

    def load_preset_maze(self):
        self.maze_data = TRAINING_MAZES[self.map_type]
        self.maze_height = len(self.maze_data)
        self.maze_width = len(self.maze_data[0]) if self.maze_height > 0 else 0

    def generate_basic_maze(self):
        self.maze_data = [[1 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        
        self.maze_data[1][1] = 0
        self.maze_data[-2][-2] = 0
        
        stack = [(1, 1)]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            cx, cy = stack[-1]
            random.shuffle(directions)
            
            moved = False
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 < nx < self.maze_width-1 and 0 < ny < self.maze_height-1 and self.maze_data[ny][nx] == 1:
                    walls_count = 0
                    for dx2, dy2 in [(0,1), (1,0), (0,-1), (-1,0)]:
                        if self.maze_data[ny+dy2][nx+dx2] == 1:
                            walls_count += 1
                    if walls_count >= 3:
                        continue
                    
                    self.maze_data[ny][nx] = 0
                    self.maze_data[cy + dy//2][cx + dx//2] = 0
                    stack.append((nx, ny))
                    moved = True
                    break
            
            if not moved:
                stack.pop()

        for y in range(1, self.maze_height-1):
            for x in range(1, self.maze_width-1):
                if self.maze_data[y][x] == 1 and random.random() < 0.1:
                    self.maze_data[y][x] = 2

    def generate_cross_maze(self):
        self.maze_data = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        
        center_x, center_y = self.maze_width // 2, self.maze_height // 2
        for x in range(self.maze_width):
            self.maze_data[center_y][x] = 1
        for y in range(self.maze_height):
            self.maze_data[y][center_x] = 1
        
        openings = [
            (center_x, center_y),
            (center_x + 1, center_y),
            (center_x - 1, center_y),
            (center_x, center_y + 1),
            (center_x, center_y - 1)
        ]
        
        for x, y in openings:
            if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
                self.maze_data[y][x] = 0

    def generate_room_maze(self):
        self.maze_data = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        
        for x in range(self.maze_width):
            self.maze_data[0][x] = 1
            self.maze_data[-1][x] = 1
        for y in range(self.maze_height):
            self.maze_data[y][0] = 1
            self.maze_data[y][-1] = 1
        
        rooms = []
        for _ in range(random.randint(2, 4)):
            w = random.randint(3, min(6, self.maze_width-4))
            h = random.randint(2, min(4, self.maze_height-4))
            x = random.randint(1, self.maze_width - w - 1)
            y = random.randint(1, self.maze_height - h - 1)
            
            collision = False
            for (rx, ry, rw, rh) in rooms:
                if not (x + w < rx or x > rx + rw or y + h < ry or y > ry + rh):
                    collision = True
                    break
            
            if not collision:
                for ry in range(y, y+h):
                    for rx in range(x, x+w):
                        self.maze_data[ry][rx] = 1
                rooms.append((x, y, w, h))
                
                door_side = random.choice(['top', 'bottom', 'left', 'right'])
                if door_side == 'top' and y > 1:
                    door_x = x + random.randint(1, w-1)
                    self.maze_data[y-1][door_x] = 0
                elif door_side == 'bottom' and y + h < self.maze_height-1:
                    door_x = x + random.randint(1, w-1)
                    self.maze_data[y+h][door_x] = 0
                elif door_side == 'left' and x > 1:
                    door_y = y + random.randint(1, h-1)
                    self.maze_data[door_y][x-1] = 0
                elif door_side == 'right' and x + w < self.maze_width-1:
                    door_y = y + random.randint(1, h-1)
                    self.maze_data[door_y][x+w] = 0

    def generate_spiral_maze(self):
        self.maze_data = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x, y = self.maze_width // 2, self.maze_height // 2
        step = 1
        direction = 0
        path = []
        
        while 0 <= x < self.maze_width and 0 <= y < self.maze_height:
            for _ in range(2):
                for _ in range(step):
                    if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
                        self.maze_data[y][x] = 1
                        path.append((x, y))
                    x += directions[direction][0]
                    y += directions[direction][1]
                direction = (direction + 1) % 4
            step += 1
        
        center_x, center_y = self.maze_width // 2, self.maze_height // 2
        for i in range(min(center_x, center_y)):
            x, y = center_x + i, center_y + i
            if x < self.maze_width and y < self.maze_height:
                self.maze_data[y][x] = 0
            x, y = center_x - i, center_y - i
            if x >= 0 and y >= 0:
                self.maze_data[y][x] = 0

    def generate_random_maze(self):
        self.maze_data = [[1 if random.random() < 0.3 else 0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
        
        path_length = min(self.maze_width, self.maze_height) // 2
        for i in range(path_length):
            x = int(i * (self.maze_width-1) / (path_length-1))
            y = int(i * (self.maze_height-1) / (path_length-1))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                        self.maze_data[ny][nx] = 0

    def adjust_tile_size(self):
        max_possible = min(
            SCREEN_WIDTH // self.maze_width,
            (SCREEN_HEIGHT - UI_HEIGHT) // self.maze_height
        )
        self.tile_size = min(TILE_SIZE, max_possible)

    def convert_to_rects(self):
        self.walls = []
        self.holes = []
        
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size + UI_HEIGHT,
                    self.tile_size,
                    self.tile_size
                )
                tile = self.maze_data[y][x]
                
                if tile == 1:
                    self.walls.append(rect)
                elif tile == 2:
                    self.holes.append(rect)

    def start_transition(self):
        self.is_transitioning = True
        self.transition_alpha = 0

    def update_transition(self):
        if self.is_transitioning:
            self.transition_alpha += 255 // TRANSITION_DURATION
            if self.transition_alpha >= 255:
                self.is_transitioning = False

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for hole in self.holes:
            pygame.draw.rect(screen, (70, 70, 90), hole)
        
        if self.is_transitioning:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - self.transition_alpha)
            screen.blit(overlay, (0, 0))