import pygame
import sys
import random

try:
    from game.menu import MainMenu
    from game.settings import *
    from game.player import Player
    from game.map import Map
    from game.target import Target, Coin
    from game.ui import UI
    from game.ai_agent import AIAgent, AITrainer
    from game.owner import OwnerConsole
    from game.maze_presets import ALL_MAZES
except ImportError:
    from menu import MainMenu
    from settings import *
    from player import Player
    from map import Map
    from target import Target, Coin
    from ui import UI
    from ai_agent import AIAgent, AITrainer
    from owner import OwnerConsole
    from maze_presets import ALL_MAZES


def run_game(screen, training_mode=False):
    map_keys = list(ALL_MAZES.keys())
    current_map_name = random.choice(map_keys)
    game_map = Map(current_map_name)
    
    player = Player(game_map.walls, game_map.holes) if not training_mode else None
    target = Target(game_map.walls, game_map.holes)
    ui = UI()
    if player:
        player.set_color(ui.get_current_color())
        
    coins = []
    clock = pygame.time.Clock()
    
    start_pos = (TILE_SIZE, UI_HEIGHT + TILE_SIZE)
    if player:
        player.rect.x, player.rect.y = start_pos
    
    ai_trainer = AITrainer()
    if training_mode:
        ai_trainer.start_training(AI_AGENT_COUNT, game_map.walls, game_map.holes, start_pos)

    game_state = {
        'score': ui.score,
        'coins': ui.coins,
        'player_pos': (player.rect.x, player.rect.y) if player else (0, 0),
        'set_score': ui.update_score,
        'set_coins': ui.add_coins,
        'set_player_pos': lambda x, y: setattr(player.rect, 'x', x) or setattr(player.rect, 'y', y)
    }
    owner_console = OwnerConsole(game_state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not owner_console.active:
                if player:
                    player.handle_event(event)
                
                selected_color = ui.handle_event(event)
                if selected_color and player:
                    player.set_color(selected_color)

            if event.type == pygame.KEYDOWN:
                if (event.key == CONSOLE_HOTKEY[0] and 
                    pygame.key.get_mods() & CONSOLE_HOTKEY[1]):
                    owner_console.toggle()
            
            if owner_console.active:
                owner_console.handle_event(event)
        
        if player:
            player.update_position()
            game_state['player_pos'] = (player.rect.x, player.rect.y)
            
            if player.rect.colliderect(target.rect):
                ui.update_score(1)
                
                if ui.score > 0 and ui.score % 5 == 0:
                    current_map_name = random.choice(map_keys)
                    game_map = Map(current_map_name)
                    player.walls = game_map.walls
                    player.holes = game_map.holes
                    player.rect.x, player.rect.y = start_pos
                
                target = Target(game_map.walls, game_map.holes)
                
                coins.clear()
                for _ in range(random.randint(1, 3)):
                    x = random.randint(2*TILE_SIZE, SCREEN_WIDTH - 2*TILE_SIZE)
                    y = random.randint(UI_HEIGHT + 2*TILE_SIZE, SCREEN_HEIGHT - 2*TILE_SIZE)
                    coins.append(Coin(x, y))
            
            for coin in coins[:]:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    ui.add_coins(1)
        
        if training_mode:
            ai_trainer.update(target.rect)
        
        coins = [coin for coin in coins if coin.update()]
        
        screen.fill(BG_COLOR)
        game_map.draw(screen)
        target.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
        
        if player:
            player.draw(screen)
        
        if training_mode:
            ai_trainer.draw(screen)
        
        ui.draw(screen)
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