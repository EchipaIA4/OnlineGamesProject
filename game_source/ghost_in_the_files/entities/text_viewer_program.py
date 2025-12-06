import pygame
from settings import screen_width, screen_height, program_width, program_height, program_header_height, text_color

class TextViewerProgram:
    def __init__(self, screen, text):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont(None, (int)(24 * screen_width / 1031))
        self.x = (screen_width - program_width) / 2
        self.y = (screen_height - program_height) / 2 + program_header_height
        self.line_height = 25 * screen_height / 580
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
        
    def render(self, rect):
        lines = self.text.split("\n")
        off_y = rect.y + program_header_height + 20 * screen_height / 580
        for line in lines:
            self.screen.blit(self.font.render(line, True, text_color), (rect.x + 20 * screen_width / 1031, off_y))
            off_y += self.line_height
