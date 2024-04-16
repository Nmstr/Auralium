import musicPlayerSqlHandler as sqlHandler
import songDataHandler

from PyQt6.QtCore import QThread, pyqtSlot
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

import os


class IndexSongsThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        songs = os.listdir('music')
        numberOfSongs = len(songs)
        processedSongs = 0
        for song in songs:
            processedSongs += 1
            hash = sqlHandler.hashFile(os.path.join('music', song))
            if not sqlHandler.retrieveSongBySha256hash(hash):
                #sqlHandler.insertSong(song, os.path.join('music', song), source='local')
                songData = songDataHandler.getTag(os.path.join('music', song))
                sqlHandler.insertSong(
                    title=songData.title,
                    filePath=os.path.join('music', song),
                    artist=songData.artist,
                    source='local',
                    releaseDate=songData.year
                )

            print(f'Processed {processedSongs}/{numberOfSongs} songs')

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('debug.ui', self)

        self.indexSongsThread = IndexSongsThread()
        self.ui.debugIndexSongs.clicked.connect(self.startIndexing)

        self.show()

    @pyqtSlot()
    def startIndexing(self):
        if not self.indexSongsThread.isRunning():
            self.indexSongsThread.start()

