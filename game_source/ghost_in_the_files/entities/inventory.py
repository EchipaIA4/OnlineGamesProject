import pygame
from settings import screen_width, screen_height, bar_height, slot_count, slot_color, slot_hovered_color, text_color

class Inventory:
    def __init__(self):
        self.items = []
        self.margin = 50 * screen_width / 1031
        self.gap = 8 * screen_width / 1031
        self.slot_size = (int)((screen_height - (slot_count + 1) * self.gap - 2 * self.margin) / slot_count)
        self.x = screen_width - self.slot_size - 10 * screen_width / 1031
        self.y = bar_height
        self.font = pygame.font.SysFont(None, (int)(20 * screen_width / 1031))
        self.hovered_slot = None
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_8:
                self.hovered_slot = event.key - pygame.K_1
    
    def render(self, screen):
        for i in range(slot_count):
            if self.hovered_slot == i:
                color = slot_hovered_color
            else:
                color = slot_color
            rect = pygame.Rect(self.x, self.y + i * (self.slot_size + self.gap) + self.margin, self.slot_size, self.slot_size)
            pygame.draw.rect(screen, color, rect)
            
            if i < len(self.items):
                self.items[i].render(screen, rect)
                if self.hovered_slot == i:
                    item_name = self.font.render(self.items[i].name, True, text_color)
                    screen.blit(item_name, (rect.centerx - item_name.get_width() / 2, rect.y - item_name.get_height() * 1.5))
