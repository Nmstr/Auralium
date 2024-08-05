import pygame
import time

class AudioPlayer:
    def __init__(self, _file_path):
        pygame.mixer.init()
        self._file_path = _file_path
        self._is_paused = False
        self._start_time = 0
        self._pause_time = 0

    def play(self):
        if self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
        else:
            pygame.mixer.music.load(self._file_path)
            pygame.mixer.music.play()
            self._start_time = time.time()

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self._pause_time = time.time() - self._start_time
            self._is_paused = True

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self._is_paused = False
            self._pause_time = 0

    @property
    def position(self):
        if self._is_paused:
            return self._pause_time
        elif pygame.mixer.music.get_busy():
            return time.time() - self._start_time
        else:
            return 0

    @position.setter
    def position(self, position):
        if pygame.mixer.music.get_busy() or self._is_paused:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=position)
            self._start_time = time.time() - position
            if self._is_paused:
                pygame.mixer.music.pause()

    @property
    def volume(self):
        return pygame.mixer.music.get_volume()

    @volume.setter
    def volume(self, volume):
        pygame.mixer.music.set_volume(volume)

# Usage
player = AudioPlayer("mysound.wav")
player.play()
print("Current volume:", player.volume)
player.volume = 0.05
print("Current volume:", player.volume)
time.sleep(5)
print("Current position:", player.position)
print("Current volume:", player.volume)
player.pause()
time.sleep(2)
print("Current position:", player.position)
player.volume = 0.025
print("Current volume:", player.volume)
player.play()
print("Current position:", player.position)
time.sleep(5)
player.volume = 0.05
player.position = 30
print("Current position:", player.position)
time.sleep(5)
print("Current position:", player.position)
player.stop()
