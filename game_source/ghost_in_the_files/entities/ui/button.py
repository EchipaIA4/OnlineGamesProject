import pygame

class Button:
    def __init__(self, rect, text, color, hover_color, text_color, font, callback, sprite_render = True, sprite_path = "assets/sprites/ui/button.png", sprite_hover_path = "assets/sprites/ui/button_hovered.png", sprite_pressed_path = "assets/sprites/ui/button_clicked.png"):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.no_callback = False
        self.callback = callback
        
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite_hover = pygame.image.load(sprite_hover_path).convert_alpha()
        self.sprite_pressed = pygame.image.load(sprite_pressed_path).convert_alpha()
        self.sprite_render = sprite_render
        
        self.hovered = False
        self.pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.hovered = self.rect.collidepoint((pos[0], pos[1]))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.hovered and not self.no_callback:
                self.callback()
            self.pressed = False
    
    def update(self):
        pass
    
    def render(self, surface):
        if self.sprite_render == True:
            if self.pressed and self.sprite_pressed:
                sprite = self.sprite_pressed
            elif self.hovered and self.sprite_hover:
                sprite = self.sprite_hover
            else:
                sprite = self.sprite
            
            if sprite:
                surface.blit(pygame.transform.scale(sprite, self.rect.size), self.rect.topleft)
        
        if self.text:
            label = self.font.render(self.text, True, self.text_color)
            pos = [self.rect.x + self.rect.width / 2 - self.font.size(self.text)[0] / 2, self.rect.y + self.rect.height / 2 - self.font.size(self.text)[1] / 2]
            if self.pressed:
                pos[0] += self.rect.width / 200 * 2
                pos[1] += self.rect.height / 50 * 2
            surface.blit(label, pos)
