import pygame
import random
from .settings import *

class AIAgent:
    def __init__(self, walls, holes=None):
        self.rect = pygame.Rect(
            random.randint(2*TILE_SIZE, SCREEN_WIDTH - 2*TILE_SIZE),
            random.randint(UI_HEIGHT + 2*TILE_SIZE, SCREEN_HEIGHT - 2*TILE_SIZE),
            TILE_SIZE // 2, 
            TILE_SIZE // 2
        )
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.walls = walls
        self.holes = holes if holes else []
        self.speed = TILE_SIZE // 10
        self.lifetime = 5 * FPS
        self.alive = True
        self.fitness = 0
        self.brain = self.create_brain()

    def create_brain(self):
        return {
            'weights': [[random.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
        }

    def think(self, target_rect):
        inputs = [
            self.get_distance(self.rect.left, 'left'),
            self.get_distance(self.rect.right, 'right'),
            self.get_distance(self.rect.top, 'up'),
            self.get_distance(self.rect.bottom, 'down')
        ]
        
        inputs = [x / (SCREEN_WIDTH / 2) for x in inputs]
        
        outputs = [0, 0, 0, 0]
        for i in range(4):
            for j in range(4):
                outputs[i] += inputs[j] * self.brain['weights'][j][i]
        
        direction = outputs.index(max(outputs))
        
        target_dir_x = target_rect.x - self.rect.x
        target_dir_y = target_rect.y - self.rect.y
        target_dist = (target_dir_x**2 + target_dir_y**2)**0.5
        if target_dist > 0:
            self.fitness += (1 / target_dist) * 0.1
        
        return direction

    def get_distance(self, pos, direction):
        if direction == 'left':
            return pos
        elif direction == 'right':
            return SCREEN_WIDTH - pos
        elif direction == 'up':
            return pos - UI_HEIGHT
        else:
            return SCREEN_HEIGHT - pos

    def update(self, target_rect):
        if not self.alive:
            return False
            
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False
            return False
            
        direction = self.think(target_rect)
        
        old_pos = self.rect.copy()
        
        if direction == 0:
            self.rect.x -= self.speed
        elif direction == 1:
            self.rect.x += self.speed
        elif direction == 2:
            self.rect.y -= self.speed
        elif direction == 3:
            self.rect.y += self.speed
            
        if any(self.rect.colliderect(wall) for wall in self.walls):
            self.rect = old_pos
            self.fitness -= 0.1
            
        if self.holes and any(self.rect.colliderect(hole) for hole in self.holes):
            self.rect.x = SCREEN_WIDTH - self.rect.x
            self.rect.y = SCREEN_HEIGHT - self.rect.y
            
        return True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)
            life_width = (self.rect.width * self.lifetime) / (5 * FPS)
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 5, life_width, 2))

class AITrainer:
    def __init__(self):
        self.agents = []
        self.generation = 0
        self.best_score = 0
        self.running = False
        self.auto_mode = False
        self.total_time = 0
        self.total_rounds = 0
        
    def start_training(self, num_agents, walls, holes):
        self.agents = [AIAgent(walls, holes) for _ in range(num_agents)]
        self.running = True
        self.generation += 1
        
    def update(self, target_rect):
        if not self.running:
            return
            
        self.total_time += 1 / FPS
        
        alive_count = 0
        for agent in self.agents:
            if agent.update(target_rect):
                alive_count += 1
                
        if alive_count == 0:
            self.next_generation()
            self.total_rounds += 1
            
    def next_generation(self):
        if not self.agents:
            return
            
        self.agents.sort(key=lambda x: x.fitness, reverse=True)
        best_agents = self.agents[:len(self.agents)//2]
        self.best_score = max(self.best_score, best_agents[0].fitness)
        
        new_agents = []
        for _ in range(len(self.agents)):
            parent1, parent2 = random.choices(best_agents, k=2)
            child = AIAgent(self.agents[0].walls, self.agents[0].holes)
            
            for i in range(4):
                for j in range(4):
                    if random.random() < 0.5:
                        child.brain['weights'][i][j] = parent1.brain['weights'][i][j]
                    else:
                        child.brain['weights'][i][j] = parent2.brain['weights'][i][j]
                    
                    if random.random() < 0.1:
                        child.brain['weights'][i][j] += random.uniform(-0.5, 0.5)
                        
            new_agents.append(child)
            
        self.agents = new_agents
        self.generation += 1
        
    def draw(self, screen):
        if not self.running:
            return
            
        for agent in self.agents:
            agent.draw(screen)
            
        font = pygame.font.SysFont("Arial", 20)
        stats = [
            f"Pokolenie: {self.generation}",
            f"Agenty: {len([a for a in self.agents if a.alive])}/{len(self.agents)}",
            f"Najlepszy wynik: {self.best_score:.2f}",
            f"Czas: {self.total_time:.1f}s",
            f"Rundy: {self.total_rounds}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH - 200, UI_HEIGHT + 20 + i * 25))