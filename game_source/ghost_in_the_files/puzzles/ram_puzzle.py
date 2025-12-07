import pygame
from settings import screen_width, screen_height, program_width, program_height, program_header_height, button_color, button_hover_color, text_color
from entities.game_state import GameState
from entities.null_pointer import NullPointer
from entities.program_window import ProgramWindow
from entities.button import Button

class RamPuzzle():
    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory
        
        self.window = ProgramWindow(
            "RamPuzzle",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
        
        self.rows, self.cols, self.cell_size = 6, 6, 45
        self.grid = GameState.ram_puzzle_state["grid"] 
        self.grid_x = self.window.rect.x + 75
        self.grid_y = self.window.rect.y + 125
        self.gap = 3
        
        self.empty_block_sprite = pygame.image.load("assets/sprites/empty_block.png")
        self.empty_block_sprite = pygame.transform.scale(self.empty_block_sprite, (self.cell_size, self.cell_size))
        self.full_block_sprite = pygame.image.load("assets/sprites/full_block.png")
        self.full_block_sprite = pygame.transform.scale(self.full_block_sprite, (self.cell_size, self.cell_size))
        
        self.big_block_sprite = pygame.image.load("assets/sprites/big_block.png")
        self.big_block_sprite = pygame.transform.scale(self.big_block_sprite, (self.cols * self.cell_size + (self.cols - 1) * self.gap, self.rows * self.cell_size + (self.rows - 1) * self.gap))
        self.big_block_rect = pygame.Rect(self.grid_x, self.grid_y, self.big_block_sprite.get_width(), self.big_block_sprite.get_height())
        
        self.slot_rect = pygame.Rect(self.grid_x + self.cols * self.cell_size + self.cols * self.gap + 90, self.grid_y + self.rows * self.cell_size / 1.5, 150, 60)
        
        self.button_size = [200, 60]
        self.start_button = Button(
            rect = (screen_width - self.button_size[0] * 2.3, screen_height / 3, self.button_size[0], self.button_size[1]),
            text = "Start",
            color = button_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = pygame.font.SysFont(None, 24),
            callback = lambda: self.start_game(),
        )
    
    def start_game(self):
        if not GameState.ram_puzzle_state["memory_chip_inserted"]:
            return
        GameState.ram_puzzle_state["game_started"] = True
        
        self.grid = [
            [0, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 0]
        ]
        GameState.ram_puzzle_state["grid"] = self.grid
    
    def toggle_cell(self, row, col):
        if not GameState.ram_puzzle_state["game_started"]:
            return
        
        if GameState.ram_puzzle_state["win"] == True and GameState.ram_puzzle_state["big_block_appeared"] == False:
            GameState.ram_puzzle_state["big_block_appeared"] = True
        
        dx = [-1, 0, 0, 1]
        dy = [0, -1, 1, 0]
        for i in range(4):
            new_pos = (row + dx[i], col + dy[i])
            if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols:
                self.grid[new_pos[0]][new_pos[1]] ^= 1
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] ^= 1
        
        if self.check_win():
            GameState.ram_puzzle_state["win"] = True
            self.start_button.no_callback = True
    
    def on_item_use(self, item):
        if item.name.lower() == "memory chip":
            self.inventory.remove_item(item)
            GameState.ram_puzzle_state["memory_chip_inserted"] = True
    
    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    return False
        return True
    
    def handle_event(self, event):
        if not self.window.active:
            return
        
        self.start_button.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos   
            if self.slot_rect.collidepoint(mouse_pos) and GameState.ram_puzzle_state["memory_chip_inserted"] == False:
                if self.inventory.hovered_slot is not None and self.inventory.hovered_slot < len(self.inventory.items):
                    item = self.inventory.items[self.inventory.hovered_slot]
                    if isinstance(item, type(None)) is False:
                        self.on_item_use(item)
            
            if GameState.ram_puzzle_state["game_started"]:
                if GameState.ram_puzzle_state["big_block_appeared"] == False:
                    for i in range(self.rows):
                        for j in range(self.cols):
                            rect = pygame.Rect(self.grid_x + j * self.cell_size + j * self.gap, self.grid_y + i * self.cell_size + i * self.gap, self.cell_size, self.cell_size)
                            if rect.collidepoint(mouse_pos):
                                self.toggle_cell(i, j)
                                GameState.ram_puzzle_state["grid"] = self.grid
                elif GameState.ram_puzzle_state["big_block_appeared"] == True and GameState.ram_puzzle_state["reward_given"] == False:
                    if self.big_block_rect.collidepoint(mouse_pos):
                        GameState.ram_puzzle_state["reward_given"] = True
                        null_pointer = NullPointer(slot_size = self.inventory.slot_size)
                        self.inventory.add_item(null_pointer)

    
    def update(self):
        if not self.window.active:
            return
        self.start_button.update()
       
    def render(self, rect):
        if not self.window.active:
            return
        self.start_button.render(self.screen)
        
        if GameState.ram_puzzle_state["big_block_appeared"] == False:
            for i in range(self.rows):
                for j in range(self.cols):
                    sprite = self.full_block_sprite if self.grid[i][j] == 1 else self.empty_block_sprite
                    self.screen.blit(sprite, (self.grid_x + j * self.cell_size + j * self.gap, self.grid_y + i * self.cell_size + i * self.gap))
        elif GameState.ram_puzzle_state["big_block_appeared"] == True and GameState.ram_puzzle_state["reward_given"] == False:
            self.screen.blit(self.big_block_sprite, (self.grid_x, self.grid_y))
        
        color = (0, 180, 80) if GameState.ram_puzzle_state["memory_chip_inserted"] else (80, 80, 80)
        pygame.draw.rect(self.screen, color, self.slot_rect, border_radius = 6)
        
        label = pygame.font.SysFont(None, 20).render("Memory Chip Slot", True, text_color)
        self.screen.blit(label, (self.slot_rect.centerx - label.get_width() / 2, self.slot_rect.y - 25))
