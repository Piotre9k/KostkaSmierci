import pygame
from game.menu import MainMenu
from game.player import Player
from game.map import GameMap
from game.target import Target
from game.ui import UI
from settings import *

def run_game():
    """Główna pętla gry (oryginalna logika)"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kostka Śmierci")
    
    game_map = GameMap()
    player = Player(game_map)
    target = Target(game_map.walls)
    ui = UI()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            player.handle_event(event)
        
        player.update()
        
        # Kolizja z celem
        if player.rect.colliderect(target.rect):
            target = Target(game_map.walls)
            ui.add_score(1)
        
        # Renderowanie
        screen.fill((30, 30, 40))
        game_map.draw(screen)
        target.draw(screen)
        player.draw(screen)
        ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Ekran startowy
    menu = MainMenu(screen)
    if menu.run():
        run_game()

if __name__ == "__main__":
    main()