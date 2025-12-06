import pygame
from settings import screen_width, program_header_height
from .program_window import ProgramWindow
from .button import Button

class LockedProgram:
    def __init__(self, screen, file_icon, code = "9345"):
        self.screen = screen
        self.file_icon = file_icon
        self.code = code
        self.input = ["-", "-", "-", "-"]
        self.message = ""
        self.font = pygame.font.SysFont(None, int(48 * screen_width / 1031))
        self.msg_font = pygame.font.SysFont(None, int(24 * screen_width / 1031))
        self.window = ProgramWindow(
            f"{self.file_icon.name} [LOCKED]",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
        
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for i in range(3, -1, -1):
                    if self.input[i] != "-":
                        self.input[i] = "-"
                        break
            elif event.unicode.isdigit():
                for i in range(4):
                    if self.input[i] == "-":
                        self.input[i] = event.unicode
                        break
    
    def update(self):
        self.enter_button.update()
    
    def check_code(self):
        if "".join(self.input) == self.code:
            self.message = "Correct"
            self.file_icon.locked = False
        else:
            self.message = "Wrong code!"
    
    def render(self, rect):
        label = self.font.render("".join(self.input), True, (255, 255, 255))
        self.screen.blit(label, (rect.centerx - label.get_width() / 2, rect.y + program_header_height + rect.height / 3))
        
        if self.message:
            color = (0, 255, 0) if "Correct" in self.message else (255, 0, 0)
            msg_label = self.msg_font.render(self.message, True, color)
            self.screen.blit(msg_label, (rect.centerx - msg_label.get_width() / 2, rect.y + program_header_height + rect.height / 2))
        
        self.enter_button.render(self.screen)
