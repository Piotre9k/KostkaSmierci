import pygame
import sys
import os
import random
from game.menu import MainMenu
from game.settings import *
from game.player import Player
from game.map import Map
from game.target import Target, Coin
from game.ui import UI
from game.owner import OwnerConsole
from game.ai_agent import AIAgent, AITrainer

def run_game(screen, training_mode=False):
    maze_type = "TRAIN_1" if training_mode else DEFAULT_MAZE_TYPE
    maze_size = "SMALL"
    
    game_map = Map(maze_type, maze_size)
    player = Player(game_map.walls, game_map.holes) if not training_mode else None
    target = Target(game_map.walls, game_map.holes)
    ui = UI()
    coins = []
    clock = pygame.time.Clock()
    level = 1
    
    ai_trainer = AITrainer()
    if training_mode:
        ai_trainer.start_training(ui.ai_agent_count, game_map.walls, game_map.holes)
    
    game_state = {
        'score': 0,
        'coins': 0,
        'level': level,
        'player_pos': (player.rect.x, player.rect.y) if player else (0, 0),
        'set_score': ui.update_score,
        'set_coins': ui.add_coins,
        'set_level': lambda l: None,
        'set_player_pos': lambda x, y: None
    }
    owner_console = OwnerConsole(game_state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if player:
                player.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if (event.key == CONSOLE_HOTKEY[0] and 
                    pygame.key.get_mods() & CONSOLE_HOTKEY[1]):
                    owner_console.toggle()
            
            if owner_console.active:
                owner_console.handle_event(event)
            else:
                selected_color = ui.handle_event(event)
                if selected_color and player:
                    player.set_color(ui.get_current_color())
        
        if player:
            player.update_position()
        
        game_state['score'] = ui.score
        game_state['coins'] = ui.coins
        game_state['level'] = level
        if player:
            game_state['player_pos'] = (player.rect.x, player.rect.y)
        
        if training_mode:
            ai_trainer.update(target.rect)
        
        if player and player.rect.colliderect(target.rect):
            ui.update_score(1)
            target = Target(game_map.walls, game_map.holes)
            target.change_color()
            
            coins.clear()
            num_coins = random.randint(1, 3)
            for _ in range(num_coins):
                x = random.randint(2*game_map.tile_size, SCREEN_WIDTH - 2*game_map.tile_size - COIN_SIZE)
                y = random.randint(UI_HEIGHT + 2*game_map.tile_size, SCREEN_HEIGHT - 2*game_map.tile_size - COIN_SIZE)
                coins.append(Coin(x, y))
            
            if ui.score % 10 == 0:
                level += 1
                game_map = Map("SPECJALNA" if level % 3 == 0 else None)
                player = Player(game_map.walls, game_map.holes)
                target = Target(game_map.walls, game_map.holes)
                if training_mode:
                    ai_trainer.start_training(ui.ai_agent_count, game_map.walls, game_map.holes)
                game_map.start_transition()
        
        if player:
            for coin in coins[:]:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    ui.add_coins(1)
        
        coins = [coin for coin in coins if coin.update()]
        
        game_map.update_transition()
        
        screen.fill(BG_COLOR)
        game_map.draw(screen)
        target.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
            if not coin.collected:
                timer_width = COIN_SIZE * (coin.lifetime / COIN_DURATION)
                pygame.draw.rect(screen, (200, 200, 200), (coin.x, coin.y - 5, COIN_SIZE, 3))
                pygame.draw.rect(screen, (0, 255, 0), (coin.x, coin.y - 5, timer_width, 3))
        
        if player:
            player.draw(screen)
        
        if training_mode:
            ai_trainer.draw(screen)
        
        ui.draw(screen)
        
        font = pygame.font.SysFont("Arial", 24)
        level_text = font.render(f"Poziom: {level}", True, (255, 255, 255))
        screen.blit(level_text, (SCREEN_WIDTH//2 - 50, 10))
        
        owner_console.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kostka Śmierci")
    
    try:
        icon = pygame.image.load('assets/kostka.ico')
        pygame.display.set_icon(icon)
    except:
        pass
    
    menu = MainMenu(screen)
    play_game, training_mode = menu.run()
    if play_game:
        run_game(screen, training_mode)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()