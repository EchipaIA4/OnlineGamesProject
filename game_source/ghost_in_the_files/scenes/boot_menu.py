import pygame
from settings import screen_width, screen_height
from entities.game_state import GameState

class BootMenu:
    def __init__(self, screen, switch_scene):
        self.screen = screen
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont("Courier", 28)
        self.title_font = pygame.font.SysFont("Courier", 34)
        self.options = ["OS 1.0", "OS 2.0", "Quit"]
        self.selected_option = 0
        
        GameState.add_log("Boot sequence initialized.")
        GameState.add_log("Desktop environment loaded successfully!")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_option] == "OS 1.0":
                    self.switch_scene("os1")
                elif self.options[self.selected_option] == "OS 2.0":
                    self.switch_scene("os2")
                else:
                    self.switch_scene("main_menu")
    
    def update(self):
        pass
    
    def render(self):
        self.screen.fill((0, 0, 0))

        title_text = self.font.render("Boot Loader", True, (200, 200, 200))
        self.screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))

        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = (100, 100, 100)
            else:
                color = (75, 75, 75)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (screen_width / 2 - text.get_width() / 2 - 30, 200 + i * 50))
            
            if i == self.selected_option:
                self.screen.blit(self.font.render(">", True, (255, 255, 255)), (screen_width / 2 - text.get_width() / 2 - 55, 200 + 50 * i))

