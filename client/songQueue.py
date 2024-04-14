class QueueEndReached(Exception):
    pass

class SongQueue():
    def __init__(self):
        self.queue = []
        self.currentSongIndex = 0

    def addSong(self, song):
        self.queue.append(song)

    def addAndSetCurrentSong(self, song):
        self.addSong(song)
        self.currentSongIndex = len(self.queue) - 1

        print(self.queue)
        print(self.currentSongIndex)
        print(self.getCurrentSong())

    def getCurrentSong(self):
        if self.currentSongIndex < len(self.queue):
            return self.queue[self.currentSongIndex]
        else:
            raise QueueEndReached('No more songs in the queue')

    def goToNextSong(self):
        if self.currentSongIndex < len(self.queue) - 1:
            self.currentSongIndex += 1
        else:
            raise QueueEndReached('No more songs in the queue')
    
    def goToLastSong(self):
        if self.currentSongIndex > 0:
            self.currentSongIndex -= 1
        else:
            raise QueueEndReached('No more songs in the queue')
    
    def getQueue(self):
        print(self.queue)
        print(self.currentSongIndex)
        print(self.getCurrentSong())
        return self.queue
    

"""queue = SongQueue()
queue.addSong('test')
queue.addSong('test2')
print(queue.getQueue())
print(queue.getCurrentSong())
queue.goToNextSong()
print(queue.getCurrentSong())
queue.goToNextSong()
print(queue.getCurrentSong())
"""