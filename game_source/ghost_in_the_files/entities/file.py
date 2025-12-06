import pygame
from pygame.time import wait
from settings import text_color, scale_factor

class FileIcon:
    def __init__(self, block, font, name = "File", on_double_click = None, locked = False):
        self.block = block
        self.name = name
        self.font = font
        self.hovered = False
        self.toggled = False
        self.on_double_click = on_double_click
        self.last_click_time = 0
        self.on_double_click_delay = 400
        self.locked = locked
        self.text = ""

        if self.locked:
            path = "assets/sprites/file_locked.png"
        else:
            path = "assets/sprites/file.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.rect = self.sprite.get_rect(center=self.block.center)
        
        self.dragging = False
        self.off_x = 0
        self.off_y = 0
        self.block_snap = self.block
    
    def handle_event(self, event, desktop_grid = None, inventory = None):
        if desktop_grid:
            pos = pygame.mouse.get_pos()
            hovered_block = desktop_grid.get_hovered_block((pos[0] / scale_factor, pos[1] / scale_factor))
            self.hovered = hovered_block == self.block
        
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.hovered = self.rect.collidepoint((pos[0] / scale_factor, pos[1] / scale_factor))
            if self.dragging:
                self.rect.center = (event.pos[0] - self.off_x, event.pos[1] - self.off_y)
                
                if desktop_grid:
                    pos = event.pos
                    hovered_block = desktop_grid.get_hovered_block((pos[0] / scale_factor, pos[1] / scale_factor))
                    if hovered_block:
                        self.block_snap = hovered_block
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                if inventory and inventory.hovered_slot is not None and inventory.hovered_slot < len(inventory.items):
                    item = inventory.items[inventory.hovered_slot]
                    if isinstance(item, type(None)) is False:
                        self.on_item_use(item, inventory)
                now = pygame.time.get_ticks()
                
                if now - self.last_click_time < self.on_double_click_delay:
                    if not self.locked:
                        if self.on_double_click:
                            self.on_double_click()
                
                self.last_click_time = now
                self.toggled = True
                
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.off_x = mouse_x - self.rect.centerx
                self.off_y = mouse_y - self.rect.centery
            else:
                self.toggled = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                if desktop_grid and desktop_grid.is_block_occupied(self.block_snap, desktop_grid.files, ignore_file = self):
                    self.rect.center = self.block.center
                else:
                    self.rect.center = self.block_snap.center
                    self.block = self.block_snap
                self.dragging = False
    
    def on_item_use(self, item, inventory = None):
        if self.locked and item.name.lower() == "key" and "secret" in self.name.lower():
            self.locked = False
            if inventory:
                inventory.remove_item(item)
            self.sprite = pygame.image.load("assets/sprites/file.png").convert_alpha()
            self.rect = self.sprite.get_rect(center=self.block.center)
       
    def render(self, surface):
        surface.blit(self.sprite, self.rect.topleft)
        label = self.font.render(self.name, True, text_color)
        surface.blit(label, (self.rect.centerx - label.get_width() / 2, self.rect.bottom + 6))
