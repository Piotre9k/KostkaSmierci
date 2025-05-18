import pygame
import random
from game.menu import MainMenu
from game.player import Player
from game.map import Map
from game.target import Target, Coin
from game.ui import UI
from settings import *

def run_game(screen):
    """Główna pętla gry"""
    game_map = Map()
    player = Player(game_map.walls, game_map.holes)
    target = Target(game_map.walls, game_map.holes)
    ui = UI()
    coins = []
    clock = pygame.time.Clock()
    score = 0
    level = 1
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            player.handle_event(event)
            
            selected_color = ui.handle_event(event)
            if selected_color:
                player.set_color(ui.get_current_color())
        
        player.update_position()
        
        # Sprawdzanie kolizji z targetem
        if player.rect.colliderect(target.rect):
            score += 1
            ui.update_score(1)
            target = Target(game_map.walls, game_map.holes)
            target.change_color()
            
            # Losowanie monet (1-3)
            coins.clear()
            num_coins = random.randint(1, 3)
            for _ in range(num_coins):
                x = random.randint(2*TILE_SIZE, SCREEN_WIDTH - 2*TILE_SIZE - COIN_SIZE)
                y = random.randint(UI_HEIGHT + 2*TILE_SIZE, SCREEN_HEIGHT - 2*TILE_SIZE - COIN_SIZE)
                coins.append(Coin(x, y))
            
            if score % 10 == 0:
                level += 1
                game_map = Map("SPECJALNA" if level % 3 == 0 else None)
                player = Player(game_map.walls, game_map.holes)
                game_map.start_transition()
        
        # Sprawdzanie kolizji z monetami
        for coin in coins[:]:
            if not coin.collected and player.rect.colliderect(coin.rect):
                coin.collected = True
                ui.add_coins(1)
        
        # Aktualizacja monet (usuwanie zebranych i tych z wygasłym czasem)
        coins = [coin for coin in coins if coin.update()]
        
        game_map.update_transition()
        
        # Renderowanie
        screen.fill(BG_COLOR)
        game_map.draw(screen)
        target.draw(screen)
        
        # Rysowanie monet z timerem
        for coin in coins:
            coin.draw(screen)
            # Rysowanie paska czasu (tylko dla aktywnych monet)
            if not coin.collected:
                timer_width = COIN_SIZE * (coin.lifetime / COIN_DURATION)
                pygame.draw.rect(screen, (200, 200, 200), (coin.x, coin.y - 5, COIN_SIZE, 3))
                pygame.draw.rect(screen, (0, 255, 0), (coin.x, coin.y - 5, timer_width, 3))
        
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