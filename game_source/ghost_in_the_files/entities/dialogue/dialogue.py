import pygame
from pathlib import Path
from settings import screen_width, screen_height, text_color

class Dialogue:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.active = False
        
        self.current_line = 0
        self.lines = []
        
        self.width = 600
        self.height = 200
        
        self.dialogue_box_sprite = pygame.image.load("assets/sprites/blocks/text_box.png")
        self.dialogue_box_sprite = pygame.transform.scale(self.dialogue_box_sprite, (self.width, self.height))
        self.dialogue_box_rect = self.dialogue_box_sprite.get_rect(midbottom = (screen_width / 2, screen_height - 10))
        
        self.ghost_sprite = pygame.image.load("assets/sprites/ghost_sprite.png")
        self.ghost_sprite = pygame.transform.scale(self.ghost_sprite, (165, 220))
        
        self.padding = 30

    def start_dialogue(self, dialogue_file):
        path = Path(dialogue_file)
        if path.exists():
            with open(path, "r", encoding = "utf-8") as f:
                self.lines = [line.strip() for line in f if line.strip()]
            self.current_line = 0
            self.active = True
    
    def advance_line(self):
        self.current_line += 1
        if self.current_line >= len(self.lines):
            self.active = False
            self.lines = []
            self.current_line = 0
    
    def wrap_text(self, text, length):
        words = text.split(" ")
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (word + " ")
            if self.font.size(test_line)[0] <= length:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        return lines
           
    def handle_event(self, event):
        if not self.active:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.advance_line()
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.lines = []
                self.current_line = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if self.dialogue_box_rect.collidepoint(mouse_pos):
                self.advance_line()
    
    def render(self):
        if not self.active:
            return
        
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
                
        self.screen.blit(self.dialogue_box_sprite, self.dialogue_box_rect)
        
        if self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            words = line.split(" ")
            max_length = self.dialogue_box_rect.width - self.ghost_sprite.get_width() - 2 * self.padding - 10
            current_line = ""
            wrapped_lines = self.wrap_text(line, max_length)

            for i, line in enumerate(wrapped_lines):
                text = self.font.render(line, True, text_color)
                x = self.dialogue_box_rect.x + self.padding + 25
                y = self.dialogue_box_rect.y + self.padding + i * (self.font.get_height() + 5)
                self.screen.blit(text, (x, y))
        
        ghost_rect = self.ghost_sprite.get_rect(topright = (self.dialogue_box_rect.x + self.dialogue_box_rect.width + 10, self.dialogue_box_rect.y - 70))
        self.screen.blit(self.ghost_sprite, ghost_rect.topleft)
