import pygame
from settings import screen_width, screen_height, program_width, program_height, program_header_height, button_color, button_hover_color, text_color
from entities.ui.button import Button

class ProgramWindow:
    def __init__(self, title, content_callback = None, process_event = None, process_update = None):
        self.title = title
        self.x = screen_width / 2 - program_width / 2
        self.y = screen_height / 2 - program_height / 2
        self.rect = pygame.Rect(self.x, self.y, program_width, program_height)
        self.header_rect = pygame.Rect(self.x, self.y, program_width, program_header_height)
        
        self.window_sprite = pygame.image.load("assets/sprites/program_window.png")
        self.window_sprite = pygame.transform.scale(self.window_sprite, (program_width, program_height))
        
        self.font = pygame.font.SysFont(None, (int)(24 * screen_width / 1031))
        self.button_size = 30 * screen_width / 1031
        self.exit_button = Button(
            rect = (self.x + program_width - self.button_size * 2.2, self.y + (program_header_height - self.button_size) / 2 + 10, self.button_size, self.button_size),
            text = "X",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = pygame.font.SysFont(None, (int)(12 * screen_width / 1031)),
            callback = lambda: self.exit()
        )
        
        self.process_event = process_event
        self.process_update = process_update
        self.content_callback = content_callback
        self.active = True
    
    def exit(self):
        self.active = False
    
    def handle_event(self, event):
        if not self.active:
            return
        self.exit_button.handle_event(event)
        if self.process_event:
            self.process_event(event)
    
    def update(self):
        if not self.active:
            return
        self.exit_button.update()
        if self.process_update:
            self.process_update()
    
    def render(self, screen):
        if not self.active:
            return
        
        screen.blit(self.window_sprite, self.rect.topleft)
        
        self.exit_button.render(screen)
        
        if self.content_callback:
            self.content_callback()
