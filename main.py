import pygame
from game.menu import MainMenu
from game.player import Player
from game.map import Map
from game.target import Target
from game.ui import UI
from settings import *

def run_game(screen):  # Dodajemy screen jako argument
    """Główna pętla gry (zgodna z Twoją implementacją)"""
    game_map = Map()
    player = Player()  # Teraz bez przekazywania game_map
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
        
        if player.rect.colliderect(target.rect):
            target = Target(game_map.walls)
            ui.add_score(1)
        
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
    pygame.display.set_caption("Kostka Śmierci")
    
    menu = MainMenu(screen)
    if menu.run():
        run_game(screen)  # Przekazujemy screen do gry

if __name__ == "__main__":
    main()