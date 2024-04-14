from debugWindow import DebugWindow

import musicPlayerSqlHandler as sqlHandler
import imgHandler as imgHandler

from songQueue import SongQueue
songQueue = SongQueue()

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QPushButton, QToolBar
from PyQt6.QtGui import QPixmap, QAction, QKeySequence
from PyQt6 import uic
import difflib
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Create hotkey action
        self.hotkeyAction = QAction(self)
        self.hotkeyAction.setShortcut("F12")
        self.hotkeyAction.triggered.connect(self.openDebugWindow)
        self.addAction(self.hotkeyAction)

        # Connect buttons for applications
        self.ui.homeBtn.clicked.connect(self.goHome)
        self.ui.searchBtn.clicked.connect(self.goSearch)

        # Connect buttons/text fields for search
        self.ui.searchBarTextChange('') # Trigger searchBarTextChange once on startup
        self.ui.searchBar.textChanged.connect(self.searchBarTextChange)
        self.ui.searchFilterAllBtn.clicked.connect(self.switchSearchFilter)
        self.ui.searchFilterSongsBtn.clicked.connect(self.switchSearchFilter)
        self.ui.searchFilterArtistsBtn.clicked.connect(self.switchSearchFilter)

        # Connect buttons for music controls
        self.ui.musicControlsNext.clicked.connect(songQueue.goToNextSong)
        self.ui.musicControlsLast.clicked.connect(songQueue.goToLastSong)
        self.ui.musicControlsGetQueue.clicked.connect(songQueue.getQueue)

        # Connect play buttons on top results
        self.ui.searchTopResults0Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(self.ui.searchTopResult0Name.text()))
        self.ui.searchTopResults1Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(self.ui.searchTopResult1Name.text()))
        self.ui.searchTopResults2Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(self.ui.searchTopResult2Name.text()))

        self.show()
    
    def searchBarTextChange(self, text):
        """
        This function handles the search functionality based on the search bar text.
        """
        allSongs = sqlHandler.retrieveAllSongTitles()
        simmilar = difflib.get_close_matches(text, allSongs, n=3, cutoff=0.05)
        simmilar = simmilar + [sqlHandler.retrieveRandomSong()[1] for _ in range(3 - len(simmilar))]

        # Update top results labels
        self.ui.searchTopResult0Name.setText(simmilar[0])
        self.ui.searchTopResult1Name.setText(simmilar[1])
        self.ui.searchTopResult2Name.setText(simmilar[2])
        # Update top results images
        self.setSongImage(simmilar[0], self.ui.searchTopResults0Img)
        self.setSongImage(simmilar[1], self.ui.searchTopResults1Img)
        self.setSongImage(simmilar[2], self.ui.searchTopResults2Img)

    def setSongImage(self, songTitle, graphicsView):
        graphicsScene = QGraphicsScene()
        pixmap = QPixmap()
        try:
            pixmap.loadFromData(imgHandler.getImgData(sqlHandler.retrieveSongByTitle(songTitle)[4]))
        except Exception:
            pixmap.loadFromData(imgHandler.getImgData('covers/default.png'))
        graphicsScene.addPixmap(pixmap)
        graphicsView.setScene(graphicsScene)

    def switchSearchFilter(self, filter):
        """
        This function handles the switching of search filters based on the senderName and the filter value.
        """
        senderName = self.sender().objectName()

        if senderName == 'searchFilterAllBtn' and filter == True:
            self.ui.searchFilterSongsBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)
        elif senderName == 'searchFilterSongsBtn' and filter == True:
            self.ui.searchFilterAllBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)
        elif senderName == 'searchFilterArtistsBtn' and filter == True:
            self.ui.searchFilterAllBtn.setChecked(False)
            self.ui.searchFilterSongsBtn.setChecked(False)
        else:
            self.ui.searchFilterAllBtn.setChecked(True)
            self.ui.searchFilterSongsBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)
    
    def goHome(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.home)

    def goSearch(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.search)
    
    def openDebugWindow(self):
        print('Open debug window')
        debugWindow = DebugWindow()
        #debugWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
