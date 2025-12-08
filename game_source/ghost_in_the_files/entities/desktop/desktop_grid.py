import pygame
from settings import screen_width, screen_height, bar_height, desktop_grid_rows, desktop_grid_cols
from entities.inventory.inventory import Inventory

class DesktopGrid:
    def __init__(self, screen, inventory, rows = desktop_grid_rows, cols = desktop_grid_cols, margin = 5):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.files = []
        self.margin = margin
        self.block_size = ((screen_width - (cols + 1) * margin - inventory.slot_size * 1.5) / cols, (screen_height - bar_height - (rows + 1) * margin) / rows)
        self.bar_offset = bar_height
        
        self.blocks = []
        for i in range(rows):
            for j in range(cols):
                x = margin + j * (self.block_size[0] + self.margin)
                y = self.bar_offset + self.margin + i * (self.block_size[1] + self.margin)
                self.blocks.append(pygame.Rect(x, y, self.block_size[0], self.block_size[1]))
    
    def is_block_occupied(self, block, files, ignore_file = None):
        for file in files:
            if file is not ignore_file and file.block == block:
                return True
        return False
    
    def get_block_center(self, block):
        return block.center
    
    def get_hovered_block(self, mouse_pos):
        for block in self.blocks:
            if block.collidepoint(mouse_pos):
                return block
        return None
    
    def render(self):
        drag_highlight = None
        highlight = None
        
        for file in self.files:
            if file.dragging:
                drag_highlight = file.block_snap
                break
            elif file.hovered:
                highlight = file.block
        
        for block in self.blocks:
            overlay = None
            if block == drag_highlight:
                overlay = (120, 120, 120, 80)
            elif block == highlight:
                overlay = (140, 140, 140, 60)
            
            if overlay:
                surface = pygame.Surface((self.block_size[0], self.block_size[1]), pygame.SRCALPHA)
                surface.fill(overlay)
                self.screen.blit(surface, block.topleft)
