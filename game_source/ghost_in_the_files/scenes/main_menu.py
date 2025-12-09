import pygame
from settings import screen_width, screen_height, button_color, button_hover_color, text_color
from entities.ui.button import Button

class MainMenu:
    def __init__(self, screen, switch_scene, cursor, music):
        self.screen = screen
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, (int)(44 * screen_width / 1031))
        self.cursor = cursor
        self.music = music
        
        self.background = pygame.image.load("assets/sprites/backgrounds/main_menu.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.arrow = pygame.image.load("assets/sprites/ui/arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (32 * 1031 / 1536, 48 * 580 / 1024))
        
        # button rendering variables
        self.button_size = [180, 45]
        self.gap = 90
        
        self.buttons = []
        start_button = Button(
            rect = (screen_width - self.button_size[0] - 180, screen_height / 2, self.button_size[0], self.button_size[1]),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.start_game(),
            sprite_path = "assets/sprites/ui/start_button.png",
            sprite_hover_path = "assets/sprites/ui/start_button.png",
            sprite_pressed_path = "assets/sprites/ui/start_button.png",
        )

        exit_button = Button(
            rect = (screen_width - self.button_size[0] - 180, screen_height / 2 + self.gap, self.button_size[0] - 15, self.button_size[1]),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("quit"),
            sprite_path = "assets/sprites/ui/quit_button.png",
            sprite_hover_path = "assets/sprites/ui/quit_button.png",
            sprite_pressed_path = "assets/sprites/ui/quit_button.png"
        )
        self.buttons.append(start_button)
        self.buttons.append(exit_button)
        self.selected_index = 0
    
    def start_game(self):
        self.switch_scene("boot_menu")
        self.music.play("assets/sounds/gameplay.ogg")
    
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
        
        self.screen.blit(self.arrow, (self.buttons[self.selected_index].rect.x - 50, self.buttons[self.selected_index].rect.y + self.buttons[self.selected_index].rect.height / 2 - self.arrow.get_height() / 2))
        
        self.cursor.render(self.screen)
