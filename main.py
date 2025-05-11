import pygame
import tkinter as tk
from tkinter import messagebox
import sys
from settings import *
from game.player import Player
from game.target import Target
from game.ui import UI
from game.map import Map

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BlokŚmierci")
    clock = pygame.time.Clock()
    
    game_map = Map()
    player = Player()
    target = Target(game_map.walls)  # Przekazanie ścian
    ui = UI()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player.move(keys, game_map.walls)
        
        if player.rect.colliderect(target.rect):
            ui.update_score(1)
            target = Target(game_map.walls)  # Ponowne przekazanie ścian
        
        screen.fill(BG_COLOR)
        game_map.draw(screen)
        target.draw(screen)
        player.draw(screen)
        ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

root = tk.Tk()
root.withdraw()
response = messagebox.askyesno(
    "BlokŚmierci",
    "Czy chcesz rozpocząć grę?",
    icon='question'
)

if response:
    run_game()
else:
    sys.exit()