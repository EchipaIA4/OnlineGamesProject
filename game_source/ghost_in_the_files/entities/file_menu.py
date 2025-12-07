import pygame
from settings import file_width, file_height, text_color, slot_color, screen_width, scale_factor

class FileMenu:
    def __init__(self, screen, files, x, y, width=260):
        self.screen = screen
        self.files = files
        
        self.x = x
        self.y = y
        self.width = width
        self.height = file_height - 5
        
        self.rects = []
        self.font = pygame.font.SysFont(None, 24)
        self.active = False
        self.selected_file = None
            
        for i, f in enumerate(files):
            rect = pygame.Rect(self.x, self.y + i * (self.height), self.width, self.height)
            self.rects.append(rect)
    
    def toggle(self):
        self.active = not self.active
    
    def handle_event(self, event):
        if not self.active:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered_index = None
            for i, rect in enumerate(self.rects):
                pos = event.pos
                if rect.collidepoint((pos[0] / scale_factor, pos[1] / scale_factor)):
                    self.hovered_index = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            for i, rect in enumerate(self.rects):
                pos = event.pos
                if rect.collidepoint((pos[0] / scale_factor, pos[1] / scale_factor)):
                    self.selected_file = self.files[i]
                    self.active = False
    
    def render(self):
        if not self.active:
            return
        
        for i, rect in enumerate(self.rects):
            color = (100, 100, 100) if getattr(self, "hovered_index", None) == i else (60, 60, 60)
            pygame.draw.rect(self.screen, color, rect)
            
            icon_rect = pygame.Rect(rect.x + 5, rect.y + 5, file_width / 2, file_height / 2)
            pygame.draw.rect(self.screen, (150, 150, 150), icon_rect)
            
            label = self.font.render(self.files[i].name, True, text_color)
            self.screen.blit(label, (rect.x + 50, rect.y + (self.height - label.get_height()) / 2))
