import pygame
from settings import program_width
from entities.game_state import GameState
from entities.programs.program_window import ProgramWindow
from entities.submit_score import submit_score_native
import asyncio

class KernelPuzzle():
    def __init__(self, screen, switch_scene, inventory, music):
        self.screen = screen
        self.switch_scene = switch_scene
        self.inventory = inventory
        self.music = music
        
        self.window = ProgramWindow(
            "KernelPuzzle",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
        
        self.x = self.window.x + program_width / 2
        self.y = self.window.y + 160
        self.empty_slot_sprite = pygame.image.load("assets/sprites/nodes/null_empty_node.png")
        self.empty_slot_sprite = pygame.transform.scale(self.empty_slot_sprite, (210, 210))
        self.empty_rect = self.empty_slot_sprite.get_rect(topleft=(self.x - self.empty_slot_sprite.get_width() / 2, self.y))
    
    def on_item_use(self, item):
        if item.name.lower() == "system core":
            self.inventory.remove_item(item)
            self.switch_scene("final_menu")
            self.music.play("assets/sounds/final_menu.ogg")
            if GameState.score_submitted == False:
                score = (GameState.game_time_minutes - 6 * 60) // 10
                asyncio.create_task(submit_score_native(max(100 - score, 0)))
                GameState.score_submitted = True

    
    def handle_event(self, event):
        if not self.window.active:
            return
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.empty_rect.collidepoint(mouse_pos):
                if self.inventory.hovered_slot is not None and self.inventory.hovered_slot < len(self.inventory.items):
                    item = self.inventory.items[self.inventory.hovered_slot]
                    if isinstance(item, type(None)) is False:
                        self.on_item_use(item)
    
    def update(self):
        pass
    
    def render(self, rect):
        if not self.window.active:
            return
        
        self.screen.blit(self.empty_slot_sprite, self.empty_rect)

