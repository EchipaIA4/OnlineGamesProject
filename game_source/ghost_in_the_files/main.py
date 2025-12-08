import pygame
from settings import screen_width, screen_height
from scenes.main_menu import MainMenu
from scenes.boot_menu import BootMenu
from scenes.final_menu import FinalMenu
from scenes.desktop import Desktop
from entities.desktop.cursor import Cursor
from entities.inventory.inventory import Inventory

pygame.init()
surface = pygame.Surface((screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

current_scene = None
cursor = Cursor()
inventory = Inventory()
pygame.mouse.set_visible(False)

scenes = {}

def switch_scene(scene_name):
    global current_scene
    if scene_name == "quit":
        pygame.quit()
        exit()
    current_scene = scenes[scene_name]

scenes["main_menu"] = MainMenu(surface, switch_scene, cursor)
scenes["boot_menu"] = BootMenu(surface, switch_scene, cursor)
scenes["os1"] = Desktop(surface, inventory, switch_scene, cursor, "os1")
scenes["os2"] = Desktop(surface, inventory, switch_scene, cursor, "os2")
scenes["final_menu"] = FinalMenu(surface, switch_scene, cursor, inventory, scenes)

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
