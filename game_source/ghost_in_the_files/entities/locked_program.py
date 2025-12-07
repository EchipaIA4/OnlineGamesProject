import pygame
from settings import screen_width, program_header_height
from entities.game_state import GameState
from .program_window import ProgramWindow
from .button import Button
from .memory_chip import MemoryChip

class LockedProgram:
    def __init__(self, screen, file_icon, inventory, code = "9345"):
        self.screen = screen
        self.file_icon = file_icon
        self.inventory = inventory
        
        self.code = code
        self.input = GameState.locked_program_state.get("input", ["-", "-", "-", "-"]).copy()
        self.guessed = GameState.locked_program_state.get("guessed", False)
        
        self.message = ""
        self.font = pygame.font.SysFont(None, int(48 * screen_width / 1031))
        self.msg_font = pygame.font.SysFont(None, int(24 * screen_width / 1031))
        
        self.window = ProgramWindow(
            f"{self.file_icon.name} [LOCKED]",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
        self.window.program = self
        
        self.enter_button = Button(
            rect = (self.window.rect.centerx - 120 / 2, self.window.rect.y + self.window.rect.height / 2 + 80, 120, 40),
            text = "Enter",
            color = (80, 80, 80),
            hover_color = (120, 120, 120),
            text_color = (255, 255, 255),
            font = self.msg_font,
            callback = self.check_code
        )
    
    def handle_event(self, event):
        self.enter_button.handle_event(event)
        
        if GameState.locked_program_state["guessed"] == True:
            return
        
        changed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for i in range(3, -1, -1):
                    if self.input[i] != "-":
                        self.input[i] = "-"
                        changed = True
                        break
            elif event.unicode.isdigit():
                for i in range(4):
                    if self.input[i] == "-":
                        self.input[i] = event.unicode
                        changed = True
                        break
            elif event.key == pygame.K_RETURN:
                self.check_code()
        
        if changed:
            GameState.locked_program_state["input"] = self.input.copy()
    
    def update(self):
        self.enter_button.update()
    
    def check_code(self):
        if "".join(self.input) == self.code and GameState.locked_program_state["guessed"] == False:
            self.message = "Correct"
            self.file_icon.locked = False
            self.guessed = True
            GameState.locked_program_state["guessed"] = True
            GameState.locked_program_state["input"] = self.input.copy()
            self.enter_button.no_callback = True
            
            memory_chip = MemoryChip(slot_size = self.inventory.slot_size)
            self.inventory.add_item(memory_chip)
        else:
            self.message = "Wrong code!"
            
            # Reset input after wrong guess
            self.input = ["-", "-", "-", "-"]
            GameState.locked_program_state["input"] = self.input.copy()
    
    def render(self, rect):
        title_label = self.msg_font.render("Enter code:", True, (255, 255, 255))
        self.screen.blit(title_label, (rect.centerx - title_label.get_width() / 2, rect.y + program_header_height + rect.height / 4))
        
        spacing = 30
        for i, digit in enumerate(self.input):
            label = self.font.render(digit, True, (255, 255, 255))
            self.screen.blit(label, (rect.centerx - spacing * 3 / 2 + i * spacing - label.get_width() / 2, rect.y + program_header_height + rect.height / 3 + 20))
        
        if GameState.locked_program_state["guessed"] == True:
            self.message = "Correct"
        
        if self.message or GameState.locked_program_state["guessed"] == True:
            color = (0, 255, 0) if "Correct" in self.message else (255, 0, 0)
            msg_label = self.msg_font.render(self.message, True, color)
            self.screen.blit(msg_label, (rect.centerx - msg_label.get_width() / 2, rect.y + program_header_height + rect.height / 2))
        
        self.enter_button.render(self.screen)
