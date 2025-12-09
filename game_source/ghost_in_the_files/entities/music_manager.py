import pygame

class MusicManager():
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
    
    def play(self, track_path, volume = 0.5):
        if self.current_track == track_path:
            return
        
        self.current_track = track_path
        pygame.mixer.music.fadeout(400)
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, fade_ms = 400)
    
    def stop(self):
        pygame.mixer.music.fadeout(400)
        self.current_track = None
