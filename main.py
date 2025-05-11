import pygame
from game.menu import MainMenu
from game.player import Player
from game.map import Map
from game.target import Target
from game.ui import UI
from settings import *

def run_game(screen):
    """Główna pętla gry"""
    game_map = Map()
    player = Player(game_map.walls, game_map.holes)
    target = Target(game_map.walls, game_map.holes)
    ui = UI()
    
    clock = pygame.time.Clock()
    score = 0
    level = 1
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                player.handle_event(event)
            
            selected_color = ui.handle_event(event)
            if selected_color:
                player.color = ui.get_current_color()
        
        player.update_position()
        
        if player.rect.colliderect(target.rect):
            score += 1
            ui.update_score(1)
            target = Target(game_map.walls, game_map.holes)
            
            if score % 10 == 0:
                level += 1
                game_map = Map("SPECJALNA" if level % 3 == 0 else None)
                player = Player(game_map.walls, game_map.holes)
                game_map.start_transition()
        
        game_map.update_transition()
        
        # Renderowanie
        screen.fill(BG_COLOR)
        game_map.draw(screen)
        target.draw(screen)
        player.draw(screen)
        ui.draw(screen)
        
        # Wyświetlanie poziomu
        font = pygame.font.SysFont("Arial", 24)
        level_text = font.render(f"Poziom: {level}", True, (255, 255, 255))
        screen.blit(level_text, (SCREEN_WIDTH//2 - 50, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kostka Śmierci")
    
    menu = MainMenu(screen)
    if menu.run():
        run_game(screen)
    
    pygame.quit()

if __name__ == "__main__":
    main()