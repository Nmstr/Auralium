from debugWindow import DebugWindow

import musicPlayerSqlHandler as sqlHandler
import songDataHandler

from songQueue import SongQueue
songQueue = SongQueue()

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene
from PyQt6.QtGui import QCloseEvent, QPixmap, QAction
from PyQt6.QtCore import QTimer
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
        self.ui.musicControlsLast.clicked.connect(songQueue.goToPreviousSong)
        self.ui.musicControlsGetQueue.clicked.connect(songQueue.getQueue)
        self.ui.musicControlsPlay.clicked.connect(songQueue.play)
        self.ui.musicControlsPause.clicked.connect(songQueue.pause)
        self.ui.musicControlsVolume.valueChanged.connect(songQueue.setVolume)
        self.ui.musicControlsTime.sliderReleased.connect(self.updateSliderPositionManual)

        # Connect play buttons on top results and set defalt text
        self.ui.searchTopResults0Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(sqlHandler.retrieveSongByTitle(self.ui.searchTopResult0Name.text())[3]))
        self.ui.searchTopResults1Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(sqlHandler.retrieveSongByTitle(self.ui.searchTopResult1Name.text())[3]))
        self.ui.searchTopResults2Play.clicked.connect(lambda: songQueue.addAndSetCurrentSong(sqlHandler.retrieveSongByTitle(self.ui.searchTopResult2Name.text())[3]))

        # Create a QTimer to update the time slider automatically every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimeSliderAuto)
        self.timer.start(1000)

        # Create value for song duration
        self.oldDuration = 0

        self.show()

    def updateSliderPositionManual(self):
        """
        Updates the slider position manually based on the value of musicControlsTime.
        Changes the position in the song.
        """
        timeInSeconds = self.ui.musicControlsTime.value()
        songQueue.setTime(timeInSeconds)

    def updateTimeSliderAuto(self):
        """
        Updates the time slider automatically based on the current song's duration.
        Adjusts the slider value and triggers actions based on song progress.
        """
        newValue = self.ui.musicControlsTime.value()
        if songQueue.playing:
            newValue += 1
            self.ui.musicControlsTime.setValue(newValue)

        try:
            newDuration = songDataHandler.getTag(songQueue.getCurrentSong()).duration
            if self.oldDuration != newDuration:
                self.ui.musicControlsTime.setValue(0)
                self.ui.musicControlsTime.setRange(0, int(newDuration))
            self.oldDuration = newDuration

            if newValue >= int(newDuration):
                self.ui.musicControlsTime.setValue(0)
                songQueue.goToNextSong()
        except Exception:
            pass #print('No song loaded')


    def searchBarTextChange(self, text):
        """
        This function handles the search functionality based on the search bar text.
        """
        try:
            allSongs = sqlHandler.retrieveAllSongs()
            # Create a list of concatenated title and artist for matching
            titlesArtists = [song[1] + " " + song[2] for song in allSongs]
            similarTitlesArtists = difflib.get_close_matches(text, titlesArtists, n=3, cutoff=0.05)
            
            # Map the similar strings back to the original song tuples
            similar = [song for song in allSongs if (song[1] + " " + song[2]) in similarTitlesArtists]

            similar = similar + [sqlHandler.retrieveRandomSong() for _ in range(3 - len(similar))]
        except Exception as e:
            # If there's an error, fill in with random songs
            similar = [sqlHandler.retrieveRandomSong() for _ in range(3)]
            print(e)

        # Update top results labels
        self.ui.searchTopResult0Name.setText(similar[0][1])  # Update to use the song title
        self.ui.searchTopResult1Name.setText(similar[1][1])
        self.ui.searchTopResult2Name.setText(similar[2][1])
        
        # Update top results images
        self.setSongImage(similar[0][1], self.ui.searchTopResults0Img)  # Update to use the song file path
        self.setSongImage(similar[1][1], self.ui.searchTopResults1Img)
        self.setSongImage(similar[2][1], self.ui.searchTopResults2Img)

    def setSongImage(self, songTitle: str, graphicsView):
        """
        A function that sets the image of a song in a graphics view.

        Parameters:
        - self: the object instance
        - songTitle: str, the title of the song to set the image for
        - graphicsView: the graphics view where the image will be set

        Returns:
        - None
        """
        graphicsScene = QGraphicsScene()
        pixmap = QPixmap()
        try:
            pixmap.loadFromData(songDataHandler.getImgData(sqlHandler.retrieveSongByTitle(songTitle)[3]))
        except Exception:
            pixmap.loadFromData(songDataHandler.getImgData('covers/default.png'))
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
        """
        Openes the debug window.
        """
        DebugWindow()
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """
        A function that handles the close event. Closes all top-level widgets except itself.
        """
        for widget in QApplication.topLevelWidgets():
            if widget is not self:
                widget.close()
        return super().closeEvent(a0)

if __name__ == '__main__':
    sqlHandler.createDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
