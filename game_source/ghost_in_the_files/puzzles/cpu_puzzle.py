import pygame
from entities.game_state import GameState
from entities.items.system_core import SystemCore
from entities.programs.program_window import ProgramWindow

class CpuPuzzle():
    def __init__(self, screen, inventory, dialogue):
        self.screen = screen
        self.inventory = inventory
        self.dialogue = dialogue
        self.font = pygame.font.SysFont(None, 22)

        self.cpu_cores = GameState.cpu_puzzle_state["cpu_cores"]
        
        self.window = ProgramWindow(
            "CpuPuzzle",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
                             
        self.x = self.window.rect.x + 90
        self.y = self.window.rect.y + 175
        self.gap = 40
        
        self.core1_sprite = pygame.image.load("assets/sprites/cores/core1.png")
        self.core1_sprite = pygame.transform.scale(self.core1_sprite, (110, 110))
        
        self.core2_sprite = pygame.image.load("assets/sprites/cores/core2.png")
        self.core2_sprite = pygame.transform.scale(self.core2_sprite, (110, 110))
        
        self.core3_sprite = pygame.image.load("assets/sprites/cores/core3.png")
        self.core3_sprite = pygame.transform.scale(self.core3_sprite, (110, 110))
        
        self.core4_sprite = pygame.image.load("assets/sprites/cores/core4.png")
        self.core4_sprite = pygame.transform.scale(self.core4_sprite, (110, 110))
        
        self.core4_broken_sprite = pygame.image.load("assets/sprites/cores/core4_broken.png")
        self.core4_broken_sprite = pygame.transform.scale(self.core4_broken_sprite, (110, 110))
        
        self.heart_sprite = pygame.image.load("assets/sprites/items/system_core.png")
        self.heart_sprite = pygame.transform.scale(self.heart_sprite, (60, 60))
        
        self.core1_rect = self.core1_sprite.get_rect(topleft=(self.x, self.y))
        self.core2_rect = self.core2_sprite.get_rect(topleft=(self.x + self.core1_sprite.get_width() + self.gap, self.y))
        self.core3_rect = self.core3_sprite.get_rect(topleft=(self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + 2 * self.gap, self.y))
        self.core4_rect = self.core4_sprite.get_rect(topleft=(self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() + 3 * self.gap, self.y))
        self.core4_broken_rect = self.core4_broken_sprite.get_rect(topleft=(self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() + 3 * self.gap, self.y))
        self.heart_rect = self.heart_sprite.get_rect(topleft=(self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + 3 * self.gap / 2 - self.heart_sprite.get_width() / 2, self.y + self.core1_sprite.get_height() + 90))
    
    def on_item_use(self, item):
        if item.name.lower() == "entropy flask":
            self.inventory.remove_item(item)
            GameState.cpu_puzzle_state["item_used"] = True
            self.cpu_cores[3] = 25
            GameState.cpu_puzzle_state["cpu_cores"] = self.cpu_cores
            GameState.add_log("[SYSTEM] Core 4 restored! CPU cores are now reactive.")
    
    def handle_event(self, event):
        if not self.window.active:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if GameState.cpu_puzzle_state["item_used"] == True and GameState.cpu_puzzle_state["win"] == False:
                if self.core1_rect.collidepoint(mouse_pos):
                    self.cpu_cores[0] = max(self.cpu_cores[0] - 15, 0)
                    self.cpu_cores[1] = min(self.cpu_cores[1] + 10, 100)
                elif self.core2_rect.collidepoint(mouse_pos):
                    self.cpu_cores[1] = max(self.cpu_cores[1] - 10, 0)
                    self.cpu_cores[2] = min(self.cpu_cores[2] + 10, 100)
                elif self.core3_rect.collidepoint(mouse_pos):
                    self.cpu_cores[2] = max(self.cpu_cores[2] - 10, 0)
                    self.cpu_cores[3] = min(self.cpu_cores[3] + 10, 100)
                elif self.core4_rect.collidepoint(mouse_pos):
                    self.cpu_cores[3] = max(self.cpu_cores[3] - 15, 0)
                    self.cpu_cores[0] = min(self.cpu_cores[0] + 5, 100)
                
                GameState.cpu_puzzle_state["cpu_cores"] = self.cpu_cores
                if self.cpu_cores[0] <= 30 and self.cpu_cores[1] <= 30 and self.cpu_cores[2] <= 30 and self.cpu_cores[3] <= 30:
                    GameState.cpu_puzzle_state["win"] = True
                    GameState.add_log("[SYSTEM] All CPU cores stabilized below safe threshold.")
                    self.dialogue.start_dialogue("assets/dialogues/cpu_puzzle_dialogue.txt")
            
            elif GameState.cpu_puzzle_state["item_used"] == False:
                if self.core4_broken_rect.collidepoint(mouse_pos):
                    if self.inventory.hovered_slot is not None and self.inventory.hovered_slot < len(self.inventory.items):
                        item = self.inventory.items[self.inventory.hovered_slot]
                        if isinstance(item, type(None)) is False:
                            self.on_item_use(item)
            elif GameState.cpu_puzzle_state["win"] == True and GameState.cpu_puzzle_state["reward_given"] == False:
                if self.heart_rect.collidepoint(mouse_pos):
                    GameState.cpu_puzzle_state["reward_given"] = True
                    system_core = SystemCore(slot_size = self.inventory.slot_size)
                    self.inventory.add_item(system_core)
    
    def update(self):
        pass
    
    def render(self, rect):
        if not self.window.active:
            return
        
        self.screen.blit(self.core1_sprite, (self.x, self.y))
        self.screen.blit(self.core2_sprite, (self.x + self.core1_sprite.get_width() + self.gap, self.y))
        self.screen.blit(self.core3_sprite, (self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + 2 * self.gap, self.y))
        
        if GameState.cpu_puzzle_state["item_used"] == False:
            self.screen.blit(self.core4_broken_sprite, (self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() +3 * self.gap, self.y))
        else:
            self.screen.blit(self.core4_sprite, (self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() +3 * self.gap, self.y))
        
        for i in range(4):
            if i == 3 and GameState.cpu_puzzle_state["item_used"] == False:
                core_label = self.font.render("BROKEN", True, (255, 255, 255))
            else:
                core_label = self.font.render(f"{GameState.cpu_puzzle_state["cpu_cores"][i]}%", True, (255, 255, 255))
            x = self.x + self.core1_sprite.get_width() / 2
            if i == 1:
                x = self.x + self.core1_sprite.get_width() + self.gap + self.core2_sprite.get_width() / 2
            elif i == 2:
                x = self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + 2 * self.gap + self.core3_sprite.get_width() / 2
            elif i == 3:
                if GameState.cpu_puzzle_state["item_used"] == True:
                    x = self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() + 3 * self.gap + self.core4_sprite.get_width() / 2
                else:
                    x = self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + self.core3_sprite.get_width() + 3 * self.gap + self.core4_broken_sprite.get_width() / 2
            self.screen.blit(core_label, (x - core_label.get_width() / 2, self.y + self.core1_sprite.get_height() + 25))
            
            rect_size = [15, 15]
            if GameState.cpu_puzzle_state["cpu_cores"][i] <= 30:
                if i == 3 and GameState.cpu_puzzle_state["item_used"] == False:
                    color = (240, 140, 109)
                else:
                    color = (135, 200, 179)
            elif GameState.cpu_puzzle_state["cpu_cores"][i] >= 80:
                color = (240, 140, 109)
            else:
                color = (240, 201, 127)
            rect = pygame.Rect(x - rect_size[0] / 2, self.y + self.core1_sprite.get_height() + 45, rect_size[0], rect_size[1])
            pygame.draw.rect(self.screen, color, rect)
        
        if GameState.cpu_puzzle_state["win"] == True and GameState.cpu_puzzle_state["reward_given"] == False:
            self.screen.blit(self.heart_sprite, (self.x + self.core1_sprite.get_width() + self.core2_sprite.get_width() + 3 * self.gap / 2 - self.heart_sprite.get_width() / 2, self.y + self.core1_sprite.get_height() + 90))
