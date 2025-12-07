import pygame
from settings import screen_width, screen_height, button_color, button_hover_color, text_color
from entities.game_state import GameState
from entities.button import Button

class BootMenu:
    def __init__(self, screen, switch_scene, cursor):
        self.screen = screen
        self.switch_scene = switch_scene
        self.cursor = cursor
        self.font = pygame.font.SysFont("Courier", 28)
        
        self.background = pygame.image.load("assets/sprites/background.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.arrow = pygame.image.load("assets/sprites/arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (32 * 1031 / 1536, 48 * 580 / 1024))
        self.boot_text = pygame.image.load("assets/sprites/boot_text.png")
        self.boot_text = pygame.transform.scale(self.boot_text, (400, 90))
        
        self.button_size = [180, 45]
        self.gap = 80
        
        self.buttons = []
        os1_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2 - self.arrow.get_width() / 2 - 10, screen_height / 2.2, self.button_size[0], self.button_size[1]),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("os1"),
            sprite_path = "assets/sprites/ciphershell_button.png",
            sprite_hover_path = "assets/sprites/ciphershell_button.png",
            sprite_pressed_path = "assets/sprites/ciphershell_button.png",
        )
        
        os2_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2 - self.arrow.get_width() / 2 - 10, screen_height / 2.2 + self.gap, self.button_size[0] - 7, self.button_size[1] - 7),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("os2"),
            sprite_path = "assets/sprites/kernelgate_button.png",
            sprite_hover_path = "assets/sprites/kernelgate_button.png",
            sprite_pressed_path = "assets/sprites/kernelgate_button.png"
        )
        
        exit_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2 - self.arrow.get_width() / 2 - 10, screen_height / 2.2 + 2 * self.gap, self.button_size[0] - 107, self.button_size[1] - 15),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("main_menu"),
            sprite_path = "assets/sprites/exit_button.png",
            sprite_hover_path = "assets/sprites/exit_button.png",
            sprite_pressed_path = "assets/sprites/exit_button.png"
        )
        self.buttons.append(os1_button)
        self.buttons.append(os2_button)
        self.buttons.append(exit_button)
        self.selected_index = 0
        
        GameState.add_log("Boot sequence initialized.")
        GameState.add_log("Desktop environment loaded successfully!")
    
    def handle_event(self, event):
        self.cursor.handle_event(event)
        for button in self.buttons:
            button.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_index].callback()
    
    def update(self):
        self.cursor.update()
        for i, button in enumerate(self.buttons):
            button.update()
            if button.hovered:
                self.selected_index = i
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        
        for button in self.buttons:
            button.render(self.screen)
        
        self.screen.blit(self.boot_text, (screen_width / 2 - self.boot_text.get_width() / 2, screen_height / 6))
        self.screen.blit(self.arrow, (self.buttons[self.selected_index].rect.x - 50, self.buttons[self.selected_index].rect.y + self.buttons[self.selected_index].rect.height / 2 - self.arrow.get_height() / 2))
        
        self.cursor.render(self.screen)
