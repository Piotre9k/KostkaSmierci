import pygame
from .settings import *

class OwnerConsole:
    def __init__(self, game_state):
        self.game_state = game_state
        self.active = False
        self.input_text = ""
        self.font = pygame.font.SysFont("Courier New", 20)
        self.command_history = []
        self.history_index = 0
        self.visible_history = []
        
    def toggle(self):
        self.active = not self.active
        if self.active:
            pygame.key.set_repeat(500, 50)
        else:
            pygame.key.set_repeat(0)

    def handle_event(self, event):
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.execute_command()
                return True
            elif event.key == pygame.K_ESCAPE:
                self.toggle()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_UP:
                if self.command_history:
                    self.history_index = max(0, self.history_index - 1)
                    self.input_text = self.command_history[self.history_index]
            elif event.key == pygame.K_DOWN:
                if self.command_history:
                    self.history_index = min(len(self.command_history)-1, self.history_index + 1)
                    self.input_text = self.command_history[self.history_index]
            else:
                self.input_text += event.unicode
        return False

    def execute_command(self):
        if not self.input_text:
            return
            
        self.command_history.append(self.input_text)
        self.history_index = len(self.command_history)
        
        parts = self.input_text.lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        response = ""
        
        if cmd == "help":
            response = "Dostępne komendy:\n" \
                     "add_score X - dodaj punkty\n" \
                     "add_coins X - dodaj monety\n" \
                     "set_level X - ustaw poziom\n" \
                     "teleport X Y - teleportuj gracza\n" \
                     "clear - wyczyść konsolę"
        
        elif cmd == "add_score" and args:
            try:
                amount = int(args[0])
                self.game_state['set_score'](self.game_state['score'] + amount)
                response = f"Dodano {amount} punktów"
            except ValueError:
                response = "Błędna wartość"
                
        elif cmd == "add_coins" and args:
            try:
                amount = int(args[0])
                self.game_state['set_coins'](self.game_state['coins'] + amount)
                response = f"Dodano {amount} monet"
            except ValueError:
                response = "Błędna wartość"
                
        elif cmd == "set_level" and args:
            try:
                level = int(args[0])
                self.game_state['set_level'](level)
                response = f"Ustawiono poziom {level}"
            except ValueError:
                response = "Błędna wartość"
                
        elif cmd == "teleport" and len(args) >= 2:
            try:
                x = int(args[0])
                y = int(args[1])
                self.game_state['set_player_pos'](x, y)
                response = f"Teleportowano na ({x}, {y})"
            except ValueError:
                response = "Błędne współrzędne"
                
        elif cmd == "clear":
            self.visible_history = []
            response = ""
        else:
            response = "Nieznana komenda. Wpisz 'help' aby uzyskać pomoc"
            
        if response:
            self.visible_history.append(f"> {self.input_text}")
            self.visible_history.append(response)
            
        self.input_text = ""

    def draw(self, screen):
        if not self.active:
            return
            
        console_rect = pygame.Rect(50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100)
        pygame.draw.rect(screen, CONSOLE_BG_COLOR, console_rect)
        pygame.draw.rect(screen, (70, 70, 90), console_rect, 2)
        
        y_pos = console_rect.y + 10
        for line in self.visible_history[-10:]:
            text = self.font.render(line, True, CONSOLE_TEXT_COLOR)
            screen.blit(text, (console_rect.x + 10, y_pos))
            y_pos += 25
            
        pygame.draw.rect(screen, (40, 40, 60), 
                        (console_rect.x, console_rect.bottom - 40, 
                         console_rect.width, 30))
        input_text = self.font.render("> " + self.input_text, True, (255, 255, 255))
        screen.blit(input_text, (console_rect.x + 10, console_rect.bottom - 35))
        
        hint = self.font.render("ESC - zamknij konsolę", True, (150, 150, 150))
        screen.blit(hint, (console_rect.right - 200, console_rect.bottom - 35))