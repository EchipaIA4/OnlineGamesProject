import pygame

class Cursor:
    def __init__(self, path = "assets/sprites/cursor.png"):
        self.sprite = pygame.image.load(path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (24, 24))
        self.pos = pygame.mouse.get_pos()
        
        self.click_in_sound = pygame.mixer.Sound("assets/sounds/click_in.wav")
        self.click_out_sound = pygame.mixer.Sound("assets/sounds/click_out.wav")
        self.click_in_sound.set_volume(0.15)
        self.click_out_sound.set_volume(0.15)
        self.mouse_clicked = False
    
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
