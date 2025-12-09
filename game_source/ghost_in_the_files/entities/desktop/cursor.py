import pygame
from entities.game_state import GameState

class Cursor:
    def __init__(self, path = "assets/sprites/cursor.png"):
        self.sprite = pygame.image.load(path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (24, 24))
        self.pos = pygame.mouse.get_pos()
        
        self.click_in_sound = pygame.mixer.Sound("assets/sounds/ui/click_in.ogg")
        self.click_out_sound = pygame.mixer.Sound("assets/sounds/ui/click_out.ogg")
        self.volume = GameState.sfx_volume / 100
        self.master_volume = 1.0
        self.click_in_sound.set_volume(self.volume * self.master_volume)
        self.click_out_sound.set_volume(self.volume * self.master_volume)
        self.mouse_clicked = False

    def set_volume(self, volume, master_volume):
        self.click_in_sound.set_volume(volume * master_volume)
        self.click_out_sound.set_volume(volume * master_volume)
        self.volume = volume
        self.master_volume = master_volume

    def change_volume(self, volume):
        self.click_in_sound.set_volume(self.volume * volume)
        self.click_out_sound.set_volume(self.volume * volume)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_in_sound.play()
            self.mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_out_sound.play()
            self.mouse_clicked = False
    
    def update(self):
        pos = pygame.mouse.get_pos()
        self.pos = (pos[0], pos[1])
    
    def render(self, surface):
        surface.blit(self.sprite, self.pos)
