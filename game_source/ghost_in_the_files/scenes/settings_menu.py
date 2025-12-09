import pygame
from settings import screen_width, screen_height, button_color, button_hover_color, text_color
from entities.game_state import GameState
from entities.ui.button import Button
from entities.ui.slider import Slider

class SettingsMenu:
    def __init__(self, screen, switch_scene, cursor, music):
        self.screen = screen
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, (int)(44 * screen_width / 1031))
        self.cursor = cursor
        self.music = music
        
        self.background = pygame.image.load("assets/sprites/backgrounds/settings_menu.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.arrow = pygame.image.load("assets/sprites/ui/arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (32 * 1031 / 1536, 48 * 580 / 1024))
        
        # button rendering variables
        self.button_size = [100, 35]
        self.gap = 90
        
        self.slider_size = [300, 25]
        self.sliders = []
        master_slider = Slider(
            x = screen_width / 2 - self.slider_size[0] / 2,
            y = 220,
            width = self.slider_size[0],
            height = self.slider_size[1],
            initial_val = GameState.master_volume
        )
        
        music_slider = Slider(
            x = screen_width / 2 - self.slider_size[0] / 2,
            y = 330,
            width = self.slider_size[0],
            height = self.slider_size[1],
            initial_val = GameState.music_volume
        )

        sfx_slider = Slider(
            x = screen_width / 2 - self.slider_size[0] / 2,
            y = 440,
            width = self.slider_size[0],
            height = self.slider_size[1],
            initial_val = GameState.sfx_volume
        )

        self.sliders.append(master_slider)
        self.sliders.append(music_slider)
        self.sliders.append(sfx_slider)
        
        self.buttons = []
        back_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2, screen_height - 70, self.button_size[0], self.button_size[1]),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("main_menu"),
            sprite_path = "assets/sprites/ui/back_button.png",
            sprite_hover_path = "assets/sprites/ui/back_button.png",
            sprite_pressed_path = "assets/sprites/ui/back_button.png",
        )
        self.buttons.append(back_button)
        self.selected_index = 0

    def handle_event(self, event):
        self.cursor.handle_event(event)
        for button in self.buttons:
            button.handle_event(event)
        for slider in self.sliders:
            slider.handle_event(event)
        
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
        
        GameState.master_volume = self.sliders[0].value
        GameState.music_volume = self.sliders[1].value
        GameState.sfx_volume = self.sliders[2].value
        
        self.music.set_volume(GameState.music_volume / 100, GameState.master_volume / 100)
        self.cursor.set_volume(GameState.sfx_volume / 100, GameState.master_volume / 100)
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        
        for button in self.buttons:
            button.render(self.screen)
        for slider in self.sliders:
            slider.render(self.screen)
        
        self.screen.blit(self.arrow, (self.buttons[self.selected_index].rect.x - 50, self.buttons[self.selected_index].rect.y + self.buttons[self.selected_index].rect.height / 2 - self.arrow.get_height() / 2))
        
        self.cursor.render(self.screen)
