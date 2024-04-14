class QueueEndReached(Exception):
    pass

class SongQueue():
    def __init__(self):
        self.queue = []
        self.currentSongIndex = 0

    def addSong(self, song: str):
        """
        A function that adds a song to the song queue.

        Parameters:
        - song: str, the song to be added to the queue

        Returns:
        - None
        """
        self.queue.append(song)

    def addAndSetCurrentSong(self, song: str):
        """
        A function that adds a song to the song queue and sets it as the current song.

        Parameters:
        - song: str, the song to be added to the queue

        Returns:
        - None
        """
        self.addSong(song)
        self.currentSongIndex = len(self.queue) - 1

        print(self.queue)
        print(self.currentSongIndex)
        print(self.getCurrentSong())

    def getCurrentSong(self):
        """
        A function that returns the current song from the queue.

        Returns:
        - The current song from the queue if available
        - Raises QueueEndReached exception if no more songs in the queue
        """
        if self.currentSongIndex < len(self.queue):
            return self.queue[self.currentSongIndex]
        else:
            raise QueueEndReached('No more songs in the queue')

    def goToNextSong(self):
        """
        A function that advances to the next song in the queue.

        Returns:
        - None
        """
        if self.currentSongIndex < len(self.queue) - 1:
            self.currentSongIndex += 1
        else:
            raise QueueEndReached('No more songs in the queue')
    
    def goToPreviousSong(self):
        """
        A function that goes to the previous song in the queue if available.

        Returns:
        - None
        - Raises QueueEndReached exception if no more songs in the queue
        """
        if self.currentSongIndex > 0:
            self.currentSongIndex -= 1
        else:
            raise QueueEndReached('No more songs in the queue')
    
    def getQueue(self):
        """
        A function that returns the current song queue along with its current index in the queue.
        """
        print(self.queue)
        print(self.currentSongIndex)
        print(self.getCurrentSong())
        return self.queue, self.currentSongIndex
