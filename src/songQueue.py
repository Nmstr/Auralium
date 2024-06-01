import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import json

class SongQueue():
    def __init__(self, sqlHandler):
        self.sqlHandler = sqlHandler
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1) # Temp
        self.queue = []
        self.currentSongIndex = 0
        self.playing = False
        self.playingPlaylist = None

    def play(self) -> None:
        """
        Plays the current song in the queue.
        """
        self.playing = True
        pygame.mixer.music.unpause()
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(self.queue[self.currentSongIndex])
            pygame.mixer.music.play()
    
    def pause(self) -> None:
        """
        Pauses the current song in the queue.
        """
        self.playing = False
        pygame.mixer.music.pause()
    
    def getTime(self) -> int:
        """
        Returns the current position of the song in the queue.
        """
        return pygame.mixer.music.get_pos()
    
    def setTime(self, time: int) -> None:
        """
        Sets the current position of the song in the queue.
        """
        pygame.mixer.music.set_pos(time)
    
    def getVolume(self) -> float:
        """
        Returns the current volume of the song in the queue.
        """
        return pygame.mixer.music.get_volume()
    
    def setVolume(self, volume: float) -> None:
        """
        Sets the current volume of the song in the queue.
        """
        pygame.mixer.music.set_volume(volume / 100)

    def addSong(self, song: str) -> None:
        """
        A function that adds a song to the song queue.

        Parameters:
        - song: str, the song to be added to the queue
        """
        self.queue.append(song)

    def addAndSetCurrentSong(self, song: str) -> None:
        """
        A function that adds a song to the song queue and sets it as the current song.

        Parameters:
        - song: str, the song to be added to the queue
        """
        self.playingPlaylist = None
        self.addSong(song)
        self.currentSongIndex = len(self.queue) - 1

        pygame.mixer.music.load(self.queue[self.currentSongIndex])
        pygame.mixer.music.play()
        self.playing = True

    def getCurrentSong(self) -> str:
        """
        A function that returns the current song from the queue.

        Returns:
        - The current song from the queue if available
        """
        if self.currentSongIndex < len(self.queue):
            return self.queue[self.currentSongIndex]
        else:
            pass #print('No more songs in the queue')

    def goToNextSong(self) -> None:
        """
        A function that advances to the next song in the queue.
        """
        if self.playingPlaylist is not None:
            if not self.queue[self.currentSongIndex+1:]:
                if len(json.loads(self.playingPlaylist[0][5])) > self.playingPlaylist[1] + 1: # If there are more songs in the playlist
                    self.playingPlaylist[1] += 1 # Advance to the next song in the playlist
                    nextSong = self.sqlHandler.songs.retrieveById(json.loads(self.playingPlaylist[0][5])[self.playingPlaylist[1]])
                    if nextSong[7] == 1: # If the song is disabled, skip it
                        self.goToNextSong()
                    else:
                        self.addSong(nextSong[3]) # Add the next song to the queue

        if self.currentSongIndex < len(self.queue) - 1:
            self.currentSongIndex += 1
        else:
            self.playing = False

        if self.playing:
            pygame.mixer.music.load(self.queue[self.currentSongIndex])
            pygame.mixer.music.play()
    
    def goToPreviousSong(self) -> None:
        """
        A function that goes to the previous song in the queue if available.
        """
        if self.playingPlaylist is not None:
            if self.playingPlaylist[1] > 0:
                self.playingPlaylist[1] -= 1 # Go to the previous song in the playlist
        if self.currentSongIndex > 0:
            self.currentSongIndex -= 1
            self.queue.pop(self.currentSongIndex + 1)
        else:
            self.playing = False
            print('No more songs in the queue')
        if self.playing:
            pygame.mixer.music.load(self.queue[self.currentSongIndex])
            pygame.mixer.music.play()
    
    def getQueue(self) -> list:
        """
        A function that returns the current song queue along with its current index in the queue.
        """
        print('-----')
        print(self.queue)
        print(self.currentSongIndex)
        print(self.getCurrentSong())
        print(self.playing)
        print(self.playingPlaylist)
        print('-----')
        return self.queue, self.currentSongIndex
