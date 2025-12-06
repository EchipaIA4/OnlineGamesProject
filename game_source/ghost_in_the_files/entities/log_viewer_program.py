import pygame
from settings import screen_width, screen_height, program_width, program_height, program_header_height, text_color
from entities.game_state import GameState

class LogViewerProgram:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 22)
        self.x = (screen_width - program_width) / 2
        self.y = (screen_height - program_height) / 2 + program_header_height
        self.line_height = 25
        self.scroll_offset = 0
        self.scroll_speed = self.line_height
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
    
    def update(self):
        pass
    
    def render(self, rect):
        logs = GameState.get_logs()
        off_y = rect.y + program_header_height + 20 + self.scroll_offset
        for line in logs:
            self.screen.blit(self.font.render(line, True, text_color), (rect.x + 20, off_y))
            off_y += self.line_height
