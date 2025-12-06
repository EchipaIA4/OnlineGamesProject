import pygame, base64, binascii
from settings import screen_width, screen_height, program_header_height
from entities.program_window import ProgramWindow
from entities.button import Button
from entities.file_menu import FileMenu
from entities.fake_file import FakeFile

class ConvertorProgram:
    def __init__(self, screen, desktop_files):
        self.screen = screen
        self.desktop_files = [file for file in desktop_files if file.name != "Convertor.exe"]
        self.selected_file = None
        self.font = pygame.font.SysFont(None, (int)(24 * screen_width / 1031))
        self.msg_font = pygame.font.SysFont(None, (int)(32 * screen_width / 1031))
        self.error_message = ""
        self.message = ""
        self.window = ProgramWindow(
            "Convertor",
            lambda: self.render(self.window.rect),
            process_event = self.handle_event,
            process_update = self.update
        )
        self.mode = "Base64"
        
        gap = 100 * screen_width / 1031
        button_size = (160 * screen_width / 1031, 40 * screen_height / 580)
        button_rect = (self.window.rect.centerx - gap / 2 - button_size[0], self.window.rect.y + self.window.rect.height * 4 /7)
        mode_button_rect = (self.window.rect.centerx - button_size[0] / 2, self.window.rect.y + self.window.rect.height / 2.4)
        self.mode_menu = FileMenu(self.screen, [FakeFile("Base64"), FakeFile("XOR7")], mode_button_rect[0], mode_button_rect[1] + button_size[1])
        self.file_menu = FileMenu(self.screen, self.desktop_files, button_rect[0], button_rect[1] + button_size[1])
        self.mode_button = Button(
            rect=(self.window.rect.centerx - button_size[0] / 2, self.window.rect.y + self.window.rect.height / 2.8, button_size[0], button_size[1]),
            text="Mode",
            color=(80, 80, 80),
            hover_color=(120, 120, 120),
            text_color=(255, 255, 255),
            font=self.font,
            callback=self.open_mode_menu
        )
        
        self.upload_button = Button(
            rect=(self.window.rect.centerx - gap / 2 - button_size[0], self.window.rect.y + self.window.rect.height * 4 / 7, button_size[0], button_size[1]),
            text="Upload",
            color=(80, 80, 80),
            hover_color=(120, 120, 120),
            text_color=(255, 255, 255),
            font=self.font,
            callback=self.open_file_menu
        )
        
        self.decode_button = Button(
            rect=(self.window.rect.centerx + gap / 2, self.window.rect.y + self.window.rect.height * 4 / 7, button_size[0], button_size[1]),
            text="Decode",
            color=(80, 80, 80),
            hover_color=(120, 120, 120),
            text_color=(255, 255, 255),
            font=self.font,
            callback=self.decode_file
        )
    
    def open_mode_menu(self):
        self.mode_menu.toggle()
    
    def open_file_menu(self):
        self.file_menu.toggle()
    
    def decode_file(self):
        if not self.selected_file:
            self.error_message = "Upload a file!"
            self.message = ""
            return
        
        if self.selected_file.name != "README.md" and self.selected_file.name != "encrypted_note.txt":
            self.error_message = "Bad file!"
            self.message = ""
            return
        
        if self.mode == "Base64":
            try:
                decoded_bytes = base64.b64decode(self.selected_file.text)
                decoded_text = decoded_bytes.decode("utf-8")
                self.selected_file.text = decoded_text
                
                self.error_message = ""
                self.message = "File decoded successfully!"
            except binascii.Error as e:
                self.message = ""
                if "Incorrect padding" in str(e):
                    self.error_message = "File already decoded!"
                else:
                    self.error_message = f"Error decoding file!" 
            except Exception as e:
                self.message = ""
                self.error_message = f"Unexpected error!"
        elif self.mode == "XOR7":
            try:
                text = "".join(chr(ord(c) ^ 7) for c in self.selected_file.text)
                #if (any(ord(c) < 32 for c in text)):
                #    self.error_message = "Data unreadable. Maybe decode Base64 first?"
                #    self.message = ""
                #    return
                
                self.selected_file.text = text
                self.message = "XOR7 decoded!"
                self.error_message = ""
            except Exception as e:
                self.error_message = f"XOR error!"
                self.message = ""    
    
    def handle_event(self, event):
        self.mode_button.handle_event(event)
        self.upload_button.handle_event(event)
        self.decode_button.handle_event(event)
        
        if self.file_menu:
            self.file_menu.handle_event(event)
            if self.file_menu and not self.file_menu.active:
                self.selected_file = self.file_menu.selected_file
        
        if self.mode_menu:
            self.mode_menu.handle_event(event)
            if self.mode_menu and not self.mode_menu.active:
                if self.mode_menu.selected_file is not None:
                    self.mode = self.mode_menu.selected_file.name
    
    def update(self):
        self.mode_button.update()
        self.upload_button.update()
        self.decode_button.update()
    
    def render(self, rect):
        rect_size = (260 * screen_width / 1031, 60 * screen_height / 580)
        pygame.draw.rect(self.screen, (50, 50, 50), (rect.centerx - rect_size[0] / 2, rect.y + program_header_height + rect.height / 8, rect_size[0], rect_size[1]))
        file_title = self.selected_file.name if self.selected_file else ""
        label = self.msg_font.render(file_title, True, (255, 255, 255))
        self.screen.blit(label, (rect.centerx - label.get_width() / 2, rect.y + program_header_height + rect.height / 8 + rect_size[1] / 2 - label.get_height() / 2))
        
        mode_rect_size = (140 * screen_width / 1031, 35 * screen_height / 580)
        pygame.draw.rect(self.screen, (50, 50, 50), (rect.centerx - mode_rect_size[0] / 2, rect.y + program_header_height + rect.height / 2.45, mode_rect_size[0], mode_rect_size[1]))
        mode_label = self.font.render(self.mode, True, (255, 255, 255))
        self.screen.blit(mode_label, (rect.centerx - mode_label.get_width() / 2, rect.y + program_header_height + rect.height / 2.45 + mode_rect_size[1] / 2 - mode_label.get_height() / 2))
        
        self.mode_button.render(self.screen)
        self.upload_button.render(self.screen)
        self.decode_button.render(self.screen)
        
        if self.message:
            msg_label = self.font.render(self.message, True, (0, 255, 0))
            self.screen.blit(msg_label, (rect.centerx - msg_label.get_width() / 2, rect.y + program_header_height + rect.height * 5 / 7))
        
        if self.error_message:
            msg_label = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(msg_label, (rect.centerx - msg_label.get_width() / 2, rect.y + program_header_height + rect.height * 5 / 7))
        
        if self.file_menu:
            self.file_menu.render()
        
        if self.mode_menu:
            self.mode_menu.render()
