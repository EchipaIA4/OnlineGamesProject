import pygame
from settings import screen_width, screen_height

class Item:
    def __init__(self, name, description = "", path = "", slot_size = None):
        self.name = name
        self.description = description
        self.color = (200, 200, 0)
        self.sprite = pygame.image.load(path).convert_alpha()
        if slot_size:
            self.sprite = pygame.transform.scale(self.sprite, (slot_size, slot_size))
    
    def render(self, screen, rect):
        screen.blit(self.sprite, rect.topleft)
