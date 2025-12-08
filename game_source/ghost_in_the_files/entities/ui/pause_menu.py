import pygame
from entities.ui.button import Button
from settings import screen_width, screen_height, bar_height, button_color, button_hover_color, text_color

class PauseMenu:
    def __init__(self, x, y, width, height, switch_scene, screen):
        self.screen = screen
        self.width = width
        self.height = height
        
        self.x = x
        self.y = y
        
        self.font = pygame.font.SysFont(None, (int)(20 * screen_width / 1031))
        self.switch_scene = switch_scene
        self.active = False
        
        self.box_sprite = pygame.image.load("assets/sprites/blocks/text_box.png")
        self.box_sprite = pygame.transform.scale(self.box_sprite, (self.width, self.height))
        
        self.buttons = []
        log_out_button = Button(
            rect = (self.x + 20 * screen_width / 1031, self.y + 25 * screen_height / 580, self.width - 40 * screen_width / 1031, 42),
            text = "Log Out",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: (self.switch_scene("boot_menu"), self.toggle())
        )
        shutdown_button = Button(
            rect = (self.x + 20 * screen_width / 1031, self.y + 50 * screen_height / 580 + self.height / 6, self.width - 40 * screen_width / 1031, 42),
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
        if not self.active:
            return
        
        self.screen.blit(self.box_sprite, (self.x, self.y))
        for button in self.buttons:
            button.render(self.screen)
