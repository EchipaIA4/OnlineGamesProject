import pygame

class Slider():
    def __init__(self, x, y, width, height, initial_val = 50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = initial_val
        self.dragging = False
        
        self.slider_sprite = pygame.image.load("assets/sprites/ui/slider.png")
        self.slider_sprite = pygame.transform.scale(self.slider_sprite, (self.width, self.height))
        self.slider_rect = self.slider_sprite.get_rect(topleft = (self.x, self.y))
        
        self.knob_sprite = pygame.image.load("assets/sprites/ui/knob.png")
        self.knob_sprite = pygame.transform.scale(self.knob_sprite, (30, 30))
        self.knob_rect = self.knob_sprite.get_rect()
        self.update_knob()
    
    def update_knob(self):
        self.knob_rect.centerx = self.x + self.width * self.value / 100
        self.knob_rect.centery = self.y + self.slider_sprite.get_height() / 2
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.knob_rect.collidepoint(mouse_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            
            if self.dragging:
                x = max(self.x, min(mouse_pos[0], self.x + self.width))
                self.value = (x - self.x) * 100 / self.width
                self.update_knob()


    def render(self, screen):
        screen.blit(self.slider_sprite, (self.x, self.y))
        screen.blit(self.knob_sprite, self.knob_rect)
