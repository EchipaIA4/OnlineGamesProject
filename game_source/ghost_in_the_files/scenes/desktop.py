import pygame
from settings import bar_color, screen_width, screen_height, bar_height, text_color, button_hover_color, desktop_grid_rows, desktop_grid_cols
from entities.game_state import GameState
from entities.program_window import ProgramWindow
from entities.button import Button
from entities.file import FileIcon
from entities.cursor import Cursor
from entities.pause_menu import PauseMenu
from entities.desktop_grid import DesktopGrid
from entities.inventory import Inventory
from entities.key import Key
from entities.text_viewer_program import TextViewerProgram
from entities.convertor_program import ConvertorProgram
from entities.log_viewer_program import LogViewerProgram
from entities.locked_program import LockedProgram

class Desktop:
    def __init__(self, screen, inventory, switch_scene, cursor, os = "os1"):
        self.screen = screen
        self.switch_scene = switch_scene
        self.cursor = cursor
        self.font = pygame.font.SysFont(None, (int)(24 * screen_width / 1031))
        self.inventory = inventory
        self.grid = DesktopGrid(screen, self.inventory)
        self.active_program = None
        
        self.files = []
        self.file_font = pygame.font.SysFont(None, (int)(22 * screen_width / 1031))
        
        self.pause_menu = PauseMenu(screen_width * 3 / 4, bar_height, screen_width / 4 - self.inventory.slot_size * 1.5, screen_height / 3, self.switch_scene, self.screen)
        self.menu_button_rect = pygame.Rect(screen_width * 3 / 4 + 15, bar_height / 4, screen_width / 4 - 40, bar_height / 2)
        self.menu_button = Button(
            rect = pygame.Rect(screen_width * 3 / 4, 0, screen_width / 4 - 10, bar_height),
            text = "",
            color = bar_color,
            hover_color = button_hover_color,
            text_color = text_color,
            font = self.font,
            callback = self.pause_menu.toggle,
            sprite_render = False
        )
        
        self.background = pygame.image.load("assets/sprites/background.png").convert()
        self.background = pygame.transform.scale(self.background, (self.grid.block_size[0] * desktop_grid_cols + (desktop_grid_cols + 1) * self.grid.margin, self.grid.block_size[1] * desktop_grid_rows + (desktop_grid_rows + 1) * self.grid.margin))
        
        if os == "os1":
            master_key = Key(slot_size = self.inventory.slot_size)
            self.inventory.add_item(master_key)
           
            self.readme_content = "VG8gZmluZCB0aGUga2V5LCByZWFkIHRoZSBsb2dzLi4u"
            readme = FileIcon(
                self.grid.blocks[0],
                self.file_font,
                "README.md",
                lambda: self.open_program("README.md")
            )
            readme.text = self.readme_content
            secret_file = FileIcon(
                self.grid.blocks[1],
                self.file_font,
                "Secret.exe",
                lambda: self.open_program("Secret.exe"),
                True
            )
            convertor_file = FileIcon(
                self.grid.blocks[self.grid.cols],
                self.file_font,
                "Convertor.exe",
                lambda: self.open_program("Convertor.exe")
            )
            log_file = FileIcon(
                self.grid.blocks[2],
                self.file_font,
                "log.txt",
                lambda: self.open_program("log.txt")
            )
            self.encrypted_content = "U29iJ2RoY2InbnQ9Jz40MzIK"
            encrypted_file = FileIcon(
                self.grid.blocks[self.grid.cols - 1],
                self.file_font,
                "encrypted_note.txt",
                lambda: self.open_program("encrypted_note.txt"),
            )
            encrypted_file.text = self.encrypted_content
            
            self.files.append(secret_file)
            self.files.append(readme)
            self.files.append(convertor_file)
            self.files.append(log_file)
            self.files.append(encrypted_file)
            self.grid.files = self.files
        else:
            kernel_file = FileIcon(
                self.grid.blocks[0],
                self.file_font,
                "kernel.mem",
                lambda: self.open_program("kernel.mem")
            )
            
            self.files.append(kernel_file)
        
        
        GameState.set_flag("found_key")
    
    def open_program(self, title, content_callback = None):
        if self.active_program is not None:
            return
        
        if title == "README.md":
            readme = next((file for file in self.files if file.name == "README.md"), None)
            if readme:
                viewer = TextViewerProgram(self.screen, readme.text)
                self.active_program = ProgramWindow(title, lambda: viewer.render(self.active_program.rect))
        elif title == "Convertor.exe":
            convertor = ConvertorProgram(self.screen, self.files)
            self.active_program = convertor.window
        elif title == "log.txt":
            log_viewer = LogViewerProgram(self.screen)
            self.active_program = ProgramWindow(title, lambda: log_viewer.render(self.active_program.rect))
        elif title == "encrypted_note.txt":
            note = next((file for file in self.files if file.name == "encrypted_note.txt"), None)
            if note:
                viewer = TextViewerProgram(self.screen, note.text)
                self.active_program = ProgramWindow(title, lambda: viewer.render(self.active_program.rect))
        elif title == "kernel.mem":
            locked_file = next((file for file in self.files if file.name == "kernel.mem"), None)
            if locked_file:
                program = LockedProgram(self.screen, locked_file)
                self.active_program = program.window
        else:
            self.active_program = ProgramWindow(title)
        self.active_program.active = True
        
    
    def handle_event(self, event):
        self.cursor.handle_event(event)
        if self.active_program and self.active_program.active:
            self.active_program.handle_event(event)
        elif self.active_program and not self.active_program.active:
            self.active_program = None
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.active_program and self.active_program.active:
                self.active_program.active = False
                self.active_program = None
            else:
                self.pause_menu.toggle()
        
        self.menu_button.handle_event(event)
        self.pause_menu.handle_event(event)
        if not isinstance(self.active_program, LockedProgram) or not self.active_program.active:
            self.inventory.handle_event(event)
        for file in self.files:
            file.handle_event(event, self.grid, self.inventory)
    
    def update(self):
        self.cursor.update()
        self.pause_menu.update()
        self.menu_button.update()
        if self.active_program and self.active_program.active:
            self.active_program.update()
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, bar_height))
        pygame.draw.rect(self.screen, bar_color, (0, 0, screen_width, bar_height))
        
        clock_label = self.font.render(str(pygame.time.get_ticks() // 1000), True, text_color)
        self.screen.blit(clock_label, (screen_width / 2 - self.font.size(str(pygame.time.get_ticks()))[0] / 2, bar_height / 2 - self.font.size(str(pygame.time.get_ticks()))[1] / 2))
        
        self.grid.render()
        
        self.menu_button.render(self.screen)
        pygame.draw.rect(self.screen, (180, 180, 180), self.menu_button_rect)
        
        for file in self.files:
            file.render(self.screen)
        
        if self.active_program and self.active_program.active:
            self.active_program.render(self.screen)
        
        self.inventory.render(self.screen)
        self.pause_menu.render()
        self.cursor.render(self.screen)
