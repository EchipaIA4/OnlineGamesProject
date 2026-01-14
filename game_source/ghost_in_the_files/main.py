import pygame
from settings import screen_width, screen_height
from scenes.main_menu import MainMenu
from scenes.boot_menu import BootMenu
from scenes.final_menu import FinalMenu
from scenes.settings_menu import SettingsMenu
from scenes.desktop import Desktop
from entities.desktop.cursor import Cursor
from entities.inventory.inventory import Inventory
from entities.dialogue.dialogue import Dialogue
from entities.music_manager import MusicManager

pygame.init()
surface = pygame.Surface((screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

music = MusicManager()
music.play("assets/sounds/main_menu.ogg")

current_scene = None
cursor = Cursor()
inventory = Inventory()
font = pygame.font.SysFont(None, 28)
dialogue = Dialogue(surface, font)
pygame.mouse.set_visible(False)

scenes = {}

def switch_scene(scene_name):
    global current_scene
    if scene_name == "quit":
        pygame.quit()
        exit()
    current_scene = scenes[scene_name]

scenes["main_menu"] = MainMenu(surface, switch_scene, cursor, music)
scenes["boot_menu"] = BootMenu(surface, switch_scene, cursor, dialogue, music)
scenes["os1"] = Desktop(surface, inventory, switch_scene, cursor, "os1", dialogue, music)
scenes["os2"] = Desktop(surface, inventory, switch_scene, cursor, "os2", dialogue, music)
scenes["final_menu"] = FinalMenu(surface, switch_scene, cursor, inventory, scenes, dialogue, music)
scenes["settings_menu"] = SettingsMenu(surface, switch_scene, cursor, music)

current_scene = scenes["main_menu"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_scene.handle_event(event)
    
    current_scene.update()
    current_scene.render()
    
    scaled_surface = pygame.transform.scale(surface, screen.get_size())
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
