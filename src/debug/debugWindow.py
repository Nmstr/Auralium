from debug.indexSongs import DebugIndexSongsWindow
from debug.indexArtists import IndexArtistsThread

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSlot

from PyQt6 import uic

class DebugWindow(QWidget):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.ui = uic.loadUi('debug/debugWindow.ui', self)

        self.ui.indexSongs.clicked.connect(lambda: DebugIndexSongsWindow(self.mainWindow))

        self.indexArtistsThread = IndexArtistsThread(debugWindow=self, mainWindow=self.mainWindow)
        self.ui.indexArtists.clicked.connect(lambda: self.startIndexing())

        self.show()

    @pyqtSlot()
    def startIndexing(self):
        if not self.indexArtistsThread.isRunning():
            self.indexArtistsThread.start()

    def closeEvent(self, event):
        self.indexArtistsThread.stop()
        return super().closeEvent(event)