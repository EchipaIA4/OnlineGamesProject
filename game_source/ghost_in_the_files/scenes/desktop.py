import pygame
from settings import bar_color, screen_width, screen_height, bar_height, text_color, button_hover_color, desktop_grid_rows, desktop_grid_cols
from entities.game_state import GameState
from entities.programs.program_window import ProgramWindow
from entities.ui.button import Button
from entities.desktop.file import FileIcon
from entities.desktop.cursor import Cursor
from entities.ui.pause_menu import PauseMenu
from entities.desktop.desktop_grid import DesktopGrid
from entities.inventory.inventory import Inventory
from entities.items.entropy_flask import EntropyFlask
from entities.programs.text_viewer_program import TextViewerProgram
from entities.programs.convertor_program import ConvertorProgram
from entities.programs.log_viewer_program import LogViewerProgram
from puzzles.disk_puzzle import DiskPuzzle
from puzzles.ram_puzzle import RamPuzzle
from puzzles.cpu_puzzle import CpuPuzzle
from puzzles.network_puzzle import NetworkPuzzle
from puzzles.kernel_puzzle import KernelPuzzle

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
        
        self.pause_menu = PauseMenu(screen_width * 3 / 4, bar_height, screen_width / 4 - self.inventory.slot_size * 1.1, screen_height / 4.25, self.switch_scene, self.screen)
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
        
        self.background = pygame.image.load("assets/sprites/backgrounds/background.png").convert()
        self.background = pygame.transform.scale(self.background, (screen_width, self.grid.block_size[1] * desktop_grid_rows + (desktop_grid_rows + 1) * self.grid.margin))
               
        if os == "os1":
            entropy_flask = EntropyFlask(slot_size = self.inventory.slot_size)
            self.inventory.add_item(entropy_flask)
           
            self.readme_content = "TGV0IGFsbCBiZSBlbXB0eSEgQTB8QUJ8QUR8Q0R8QzAK"
            readme = FileIcon(
                self.grid.blocks[0],
                self.file_font,
                "README.md",
                lambda: self.open_program("README.md")
            )
            readme.text = self.readme_content
            kernel_file = FileIcon(
                self.grid.blocks[1],
                self.file_font,
                "kernel.mem",
                lambda: self.open_program("kernel.mem"),
                locked = True,
            )
            convertor_file = FileIcon(
                self.grid.blocks[self.grid.cols],
                self.file_font,
                "Convertor.exe",
                lambda: self.open_program("Convertor.exe"),
                system_file = True
            )
            log_file = FileIcon(
                self.grid.blocks[2],
                self.file_font,
                "log.txt",
                lambda: self.open_program("log.txt"),
                system_file = True
            )
            self.encrypted_content = "U29iJ2RoY2InbnQnPjQzMiYK"
            encrypted_file = FileIcon(
                self.grid.blocks[self.grid.cols - 1],
                self.file_font,
                "encrypted_note.txt",
                lambda: self.open_program("encrypted_note.txt"),
            )
            encrypted_file.text = self.encrypted_content
            
            self.files.append(kernel_file)
            self.files.append(readme)
            self.files.append(convertor_file)
            self.files.append(log_file)
            self.files.append(encrypted_file)
            self.grid.files = self.files
        else:
            disk_file= FileIcon(
                self.grid.blocks[0],
                self.file_font,
                "disk.mem",
                lambda: self.open_program("disk.mem"),
                system_file = True
            )
            
            ram_file = FileIcon(
                self.grid.blocks[1],
                self.file_font,
                "ram.mem",
                lambda: self.open_program("ram.mem"),
                system_file = True
            )
            
            cpu_file = FileIcon(
                self.grid.blocks[2],
                self.file_font,
                "cpu.mem",
                lambda: self.open_program("cpu.mem"),
                system_file = True
            )
            
            network_file = FileIcon(
                self.grid.blocks[self.grid.cols],
                self.file_font,
                "network.exe",
                lambda: self.open_program("network.exe")
            )
            
            self.files.append(disk_file)
            self.files.append(ram_file)
            self.files.append(cpu_file)
            self.files.append(network_file)
    
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
        elif title == "disk.mem":
            locked_file = next((file for file in self.files if file.name == "disk.mem"), None)
            if locked_file:
                program = DiskPuzzle(self.screen, locked_file, self.inventory)
                self.active_program = program.window
        elif title == "ram.mem":
            ram = next((file for file in self.files if file.name == "ram.mem"), None)
            if ram:
                program = RamPuzzle(self.screen, self.inventory)
                self.active_program = program.window
        elif title == "cpu.mem":
            cpu = next((file for file in self.files if file.name == "cpu.mem"), None)
            if cpu:
                program = CpuPuzzle(self.screen, self.inventory)
                self.active_program = program.window
        elif title == "network.exe":
            network = next((file for file in self.files if file.name == "network.exe"), None)
            if network:
                program = NetworkPuzzle(self.screen, self.inventory)
                self.active_program = program.window
        elif title == "kernel.mem":
            kernel = next((file for file in self.files if file.name == "kernel.mem"), None)
            if kernel:
                program = KernelPuzzle(self.screen, self.switch_scene, self.inventory)
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
        if not (hasattr(self.active_program, "program") and isinstance(self.active_program.program, DiskPuzzle) and self.active_program.active):
            self.inventory.handle_event(event)
        for file in self.files:
            file.handle_event(event, self.grid, self.inventory)
    
    def update(self):
        self.cursor.update()
        self.pause_menu.update()
        self.menu_button.update()
        if self.active_program and self.active_program.active:
            self.active_program.update()
        
        now = pygame.time.get_ticks()
        if now - GameState.time_update >= 1000:
            GameState.game_time_minutes += 1
            GameState.time_update = now
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, bar_height))
        pygame.draw.rect(self.screen, bar_color, (0, 0, screen_width, bar_height))
        
        clock_label = self.font.render(f"{(GameState.game_time_minutes // 60) % 24:02d}:{GameState.game_time_minutes % 60:02d}", True, (255, 255, 255))
        self.screen.blit(clock_label, (screen_width / 2 - clock_label.get_width() / 2, bar_height / 2 - clock_label.get_height() / 2))
        
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
