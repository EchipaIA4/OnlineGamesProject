import pygame
from entities.game_state import GameState

class MusicManager():
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.master_volume = 1.0
        self.volume = GameState.music_volume / 100
    
    def play(self, track_path):
        if self.current_track == track_path:
            return
        
        self.current_track = track_path
        pygame.mixer.music.fadeout(400)
        pygame.mixer.music.load(track_path)
        if self.current_track == "assets/sounds/final_menu.ogg":
            pygame.mixer.music.set_volume(self.volume * self.master_volume * 0.4)
        else:
            pygame.mixer.music.set_volume(self.volume * self.master_volume)
        pygame.mixer.music.play(-1, fade_ms = 400)
    
    def stop(self):
        pygame.mixer.music.fadeout(400)
        self.current_track = None
    
    def set_volume(self, volume, master_volume):
        self.volume = volume
        self.master_volume = master_volume
        pygame.mixer.music.set_volume(self.volume * self.master_volume)
