import pygame
from settings import screen_width, screen_height, bar_height, slot_count

class Inventory:
    def __init__(self):
        self.items = []
        
        self.margin = 15 * screen_width / 1031
        self.gap = 8 * screen_width / 1031
        self.slot_size = (int)((screen_height - (slot_count + 1) * self.gap - 2 * self.margin) / slot_count)
        
        self.x = screen_width - self.slot_size - 10 * screen_width / 1031
        self.y = bar_height
        
        self.font = pygame.font.SysFont(None, (int)(22 * screen_width / 1031))
        self.hovered_slot = None
        
        self.slot_sprite = pygame.image.load("assets/sprites/ui/inventory_slot.png")
        self.slot_sprite = pygame.transform.scale(self.slot_sprite, (self.slot_size, self.slot_size))
        self.name_visible_until = 0
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_8:
                if event.key - pygame.K_1 == self.hovered_slot:
                    self.hovered_slot = None
                else:
                    self.hovered_slot = event.key - pygame.K_1
                    self.name_visible_until = pygame.time.get_ticks() + 2500
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i in range(slot_count):
                rect = pygame.Rect(self.x, self.y + i * (self.slot_size) + (i - 1) * self.gap + self.margin, self.slot_size, self.slot_size)
                if rect.collidepoint(mouse_pos):
                    self.hovered_slot = i
                    if i < len(self.items):
                        self.name_visible_until = pygame.time.get_ticks() + 2500
    
    def render(self, screen):
        for i in range(slot_count):
            rect = pygame.Rect(self.x, self.y + i * (self.slot_size + self.gap) + self.margin, self.slot_size, self.slot_size)
            
            screen.blit(self.slot_sprite, rect.topleft)
            
            if self.hovered_slot == i:
                border = 10
                inner_rect = pygame.Rect(rect.x + border, rect.y + border, rect.width - 2 * border, rect.height - 2 * border)
                overlay = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
                overlay.fill((100, 100, 100, 100))
                screen.blit(overlay, inner_rect.topleft)
            
            if i < len(self.items):
                item = self.items[i]
                item_sprite = pygame.transform.scale(item.sprite, (self.slot_size * 0.5, self.slot_size * 0.5))
                screen.blit(item_sprite, (rect.centerx - item_sprite.get_width() / 2, rect.centery - item_sprite.get_height() / 2))
                
                if self.hovered_slot == i and pygame.time.get_ticks() <= self.name_visible_until:
                    item_name = self.font.render(self.items[i].name, True, (255, 255, 255))
                    screen.blit(item_name, (rect.centerx - item_name.get_width() / 2, rect.y + item_name.get_height() * 0.5))
