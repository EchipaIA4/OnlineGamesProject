import pygame
from settings import screen_width, screen_height, button_color, button_hover_color, text_color
from entities.game_state import GameState
from scenes.desktop import Desktop
from entities.inventory.inventory import Inventory
from entities.ui.button import Button

class FinalMenu:
    def __init__(self, screen, switch_scene, cursor, inventory, scenes, dialogue, music):
        self.screen = screen
        self.switch_scene = switch_scene
        self.inventory = inventory
        self.font = pygame.font.SysFont(None, (int)(44 * screen_width / 1031))
        self.cursor = cursor
        self.dialogue = dialogue
        self.music = music
        self.scenes = scenes
        
        self.background = pygame.image.load("assets/sprites/backgrounds/final_menu.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.arrow = pygame.image.load("assets/sprites/ui/arrow.png")
        self.arrow = pygame.transform.scale(self.arrow, (32 * 1031 / 1536, 48 * 580 / 1024))
        
        # button rendering variables
        self.button_size = [180, 45]
        self.gap = 90
        
        self.buttons = []
        restart_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2, screen_height / 2 + 50, self.button_size[0], self.button_size[1]),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.reset(),
            sprite_path = "assets/sprites/ui/restart_button.png",
            sprite_hover_path = "assets/sprites/ui/restart_button.png",
            sprite_pressed_path = "assets/sprites/ui/restart_button.png",
        )

        exit_button = Button(
            rect = (screen_width / 2 - self.button_size[0] / 2, screen_height / 2 + self.gap + 50, self.button_size[0] - 60, self.button_size[1] - 5),
            text = "",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = lambda: self.switch_scene("quit"),
            sprite_path = "assets/sprites/ui/quit2_button.png",
            sprite_hover_path = "assets/sprites/ui/quit2_button.png",
            sprite_pressed_path = "assets/sprites/ui/quit2_button.png"
        )
        self.buttons.append(restart_button)
        self.buttons.append(exit_button)
        self.selected_index = 0
    
    def reset(self):
        GameState.reset()
        
        self.inventory = Inventory()
        
        self.scenes["os1"] = Desktop(self.screen, self.inventory, self.switch_scene, self.cursor, "os1", self.dialogue, self.music)
        self.scenes["os2"] = Desktop(self.screen, self.inventory, self.switch_scene, self.cursor, "os2", self.dialogue, self.music)
        self.switch_scene("main_menu")
        self.music.play("assets/sounds/main_menu.ogg")
          
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
