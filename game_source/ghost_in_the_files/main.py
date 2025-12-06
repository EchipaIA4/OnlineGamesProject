import pygame
from settings import screen_width, screen_height, scale_factor
from scenes.main_menu import MainMenu
from scenes.boot_menu import BootMenu
from scenes.desktop import Desktop
from entities.cursor import Cursor
from entities.inventory import Inventory

pygame.init()
surface = pygame.Surface((screen_width, screen_height))
screen = pygame.display.set_mode((screen_width * scale_factor, screen_height * scale_factor))
# screen = pygame.display.set_mode((screen_width, screen_height)) 
clock = pygame.time.Clock()

current_scene = None
cursor = Cursor()
inventory = Inventory()
pygame.mouse.set_visible(False)

def switch_scene(scene_name):
    global current_scene
    if scene_name == "main_menu":
        current_scene = MainMenu(surface, switch_scene, cursor)
    elif scene_name == "os1":
        current_scene = Desktop(surface, inventory, switch_scene, cursor, "os1")
    elif scene_name == "os2":
        current_scene = Desktop(surface, inventory, switch_scene, cursor, "os2")
    elif scene_name == "boot_menu":
        current_scene = BootMenu(surface, switch_scene)
    elif scene_name == "quit":
        pygame.quit()
        exit()

switch_scene("main_menu")

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
