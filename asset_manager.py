# Loads and manages game assets (images, sounds).

import pygame

class ImageManager:
    def __init__(self):
        self.images = {}

    def load_image(self, key: str, path: str):
        # Load an image from the disk and store it in the dictionary
        image = pygame.image.load(path)
        self.images[key] = image

    def get_image(self, key: str):
        # Retrieve an image from the dictionary
        return self.images.get(key)

    def scale_image(self, key, new_size):
        # Scale an image to a new size
        if key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], new_size)

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_files = {}  # key: str, value: filepath

    def load_music(self, key: str, music_file: str):
        self.music_files[key] = music_file

    def play_music(self, key, loops=0):
        if key in self.music_files:
            pygame.mixer.music.load(self.music_files[key])
            pygame.mixer.music.play(loops)
        else:
            print(f"Music key '{key}' not found.")

    def set_volume(self, volume):
        if 0.0 <= volume <= 1.0:
            pygame.mixer.music.set_volume(volume)
        else:
            print("Volume must be between 0.0 and 1.0")
    
    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()