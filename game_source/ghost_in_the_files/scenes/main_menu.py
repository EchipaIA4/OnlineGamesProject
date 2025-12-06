import pygame
from settings import screen_width, screen_height, button_color, button_hover_color, text_color
from entities.button import Button

class MainMenu:
    def __init__(self, screen, switch_scene, cursor):
        self.screen = screen
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, (int)(44 * screen_width / 1031))
        self.cursor = cursor
        self.buttons = []
        
        # button rendering variables
        self.button_width = 300 * screen_width / 1031
        self.button_height = 75 * screen_height / 580
        self.gap = 100 * screen_width / 1031
        
        start_button = Button(
            rect = (screen_width / 2 - self.button_width - self.gap / 2, screen_height / 1.75, self.button_width, self.button_height),
            text = "Start",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("boot_menu")
        )
        
        exit_button = Button(
            rect = (screen_width / 2 + self.gap / 2, screen_height / 1.75, self.button_width, self.button_height),
            text = "Exit",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("quit")
        )
        self.buttons.append(start_button)
        self.buttons.append(exit_button)
    
    def handle_event(self, event):
        self.cursor.handle_event(event)
        for button in self.buttons:
            button.handle_event(event)
    
    def update(self):
        self.cursor.update()
        for button in self.buttons:
            button.update()
    
    def render(self):
        self.screen.fill((0, 0, 0))
        for button in self.buttons:
            button.render(self.screen)
        self.cursor.render(self.screen)
