import pygame
from settings import file_width, file_height, text_color, slot_color, screen_width

class FileMenu:
    def __init__(self, screen, files, x, y, width=260, display_file_icon = True):
        self.screen = screen
        self.files = files
        
        self.x = x
        self.y = y
        self.width = width
        self.height = file_height - 5
        self.display_file_icon = display_file_icon
        
        self.rects = []
        self.font = pygame.font.SysFont(None, 24)
        self.active = False
        self.selected_file = None
        self.box_sprite = pygame.image.load("assets/sprites/blocks/text_box.png")
        self.box_sprite = pygame.transform.scale(self.box_sprite, (self.width, self.height))
            
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
                if rect.collidepoint((pos[0], pos[1])):
                    self.hovered_index = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                pos = event.pos
                if rect.collidepoint((pos[0], pos[1])):
                    self.selected_file = self.files[i]
                    self.active = False
    
    def render(self):
        if not self.active:
            return
        
        for i, rect in enumerate(self.rects):
            self.screen.blit(self.box_sprite, rect.topleft)
            
            if getattr(self, "hovered_index", None) == i:
                color = (50, 50, 50, 100)
            else:
                color =  (0, 0, 0, 0)
            border_size = [14 * self.width / 260 , 4]
            pygame.draw.rect(self.screen, color, pygame.Rect(rect.x + border_size[0], rect.y + border_size[1], rect.width - 2 * border_size[0], rect.height - 2 * border_size[1]))
            
            if self.display_file_icon:
                icon_sprite = pygame.transform.scale(self.files[i].sprite, (file_width / 2, file_height / 2))
                self.screen.blit(icon_sprite, (rect.x + 30, rect.centery - icon_sprite.get_height() / 2))
            
                label = self.font.render(self.files[i].name, True, text_color)
                self.screen.blit(label, (rect.x + 70, rect.y + (self.height - label.get_height()) / 2))
            else:
                label = self.font.render(self.files[i].name, True, text_color)
                self.screen.blit(label, (rect.x + 52, rect.y + (self.height - label.get_height()) / 2))
