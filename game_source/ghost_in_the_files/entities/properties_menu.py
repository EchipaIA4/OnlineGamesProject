import pygame

class PropertiesMenu:
    def __init__(self, x, y, file, callback, font):
        self.x = x
        self.y = y
        self.file = file
        self.active = True
        self.font = font

