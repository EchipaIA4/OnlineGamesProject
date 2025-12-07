import pygame
from entities.button import Button
from settings import screen_width, screen_height, bar_height, button_color, button_hover_color, text_color

class PauseMenu:
    def __init__(self, x, y, width, height, switch_scene, screen):
        self.screen = screen
        self.width = width
        self.height = height
        
        self.x = x
        self.y = y
        
        self.font = pygame.font.SysFont(None, (int)(22 * screen_width / 1031))
        self.switch_scene = switch_scene
        self.active = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.buttons = []
        log_out_button = Button(
            rect = (self.x + 20 * screen_width / 1031, self.y + 20 * screen_height / 580, self.width - 40 * screen_width / 1031, self.height / 6),
            text = "Log Out",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: (self.switch_scene("boot_menu"), self.toggle())
        )
        shutdown_button = Button(
            rect = (self.x + 20 * screen_width / 1031, self.y + 40 * screen_height / 580 + self.height / 6, self.width - 40 * screen_width / 1031, self.height / 6),
            text = "Shut down",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: (self.switch_scene("main_menu"), self.toggle())
        )
        self.buttons.append(shutdown_button)
        self.buttons.append(log_out_button)
    
    def toggle(self):
        self.active = not self.active
    
    def handle_event(self, event):
        if self.active:
            for button in self.buttons:
                button.handle_event(event)
    
    def update(self):
        if self.active:
            for button in self.buttons:
                button.update()
    
    def render(self):
        if self.active:
            pygame.draw.rect(self.screen, (25, 25, 25), self.rect, border_radius = (int)(5 * screen_width / 1031))
            for button in self.buttons:
                button.render(self.screen)
