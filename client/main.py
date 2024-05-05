from debugWindow import DebugWindow

from playlistItem import PlaylistItemWidget
from sqlHandler import sqlHandler
from songQueue import SongQueue
import songDataHandler

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QVBoxLayout
from PyQt6.QtGui import QCloseEvent, QPixmap, QAction
from PyQt6.QtCore import QTimer
from PyQt6 import uic

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Set the main content
        self.setMainContentDisplay("home")

        # Create song queue
        self.songQueue = SongQueue()

        # Create hotkey action
        self.hotkeyAction = QAction(self)
        self.hotkeyAction.setShortcut("F12")
        self.hotkeyAction.triggered.connect(lambda: DebugWindow())
        self.addAction(self.hotkeyAction)

        # Connect buttons for applications
        self.ui.homeBtn.clicked.connect(lambda: self.setMainContentDisplay('home'))
        self.ui.searchBtn.clicked.connect(lambda: self.setMainContentDisplay('search'))

        # Connect buttons for music controls
        self.ui.musicControlsNext.clicked.connect(self.songQueue.goToNextSong)
        self.ui.musicControlsLast.clicked.connect(self.songQueue.goToPreviousSong)
        self.ui.musicControlsGetQueue.clicked.connect(self.songQueue.getQueue)
        self.ui.musicControlsPlay.clicked.connect(self.songQueue.play)
        self.ui.musicControlsPause.clicked.connect(self.songQueue.pause)
        self.ui.musicControlsVolume.valueChanged.connect(self.songQueue.setVolume)
        self.ui.musicControlsTime.sliderReleased.connect(self.updateSliderPositionManual)

        # Create a QTimer to update the time slider automatically every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimeSliderAuto)
        self.timer.start(1000)

        # Create value for song duration
        self.oldDuration = 0

        # Connect playlist buttons
        self.ui.playlistsCreateBtn.clicked.connect(lambda: sqlHandler.playlists.create('dadwdaddawkuuhku', None, None, None))
        self.ui.playlistsCreateBtn.clicked.connect(lambda: self.displayPlaylists())

        # Call the method to display playlists at initialization
        self.displayPlaylists()

        self.show()

    def displayPlaylists(self) -> None:
        """
        Display the playlists in the UI.

        This function retrieves all playlists from the database and dynamically adds custom widgets for each playlist in the UI.

        Parameters:
        - self: The instance of the class.

        Return:
        - None
        """
        # Retrieve all playlists from the database
        playlists = sqlHandler.playlists.retrieveAll()

        # Get the container widget
        container = self.ui.playlistsScrollAreaWidgetContents
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())): 
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                layoutItem.widget().deleteLater()

        # Dynamically add custom widgets for each playlist
        for playlist in playlists:
            playlistWidget = PlaylistItemWidget(playlist, self)
            layout.addWidget(playlistWidget)

    def updateSliderPositionManual(self):
        """
        Updates the slider position manually based on the value of musicControlsTime.
        Changes the position in the song.
        """
        timeInSeconds = self.ui.musicControlsTime.value()
        self.songQueue.setTime(timeInSeconds)

    def updateTimeSliderAuto(self):
        """
        Updates the time slider automatically based on the current song's duration.
        Adjusts the slider value and triggers actions based on song progress.
        """
        newValue = self.ui.musicControlsTime.value()
        if self.songQueue.playing:
            newValue += 1
            self.ui.musicControlsTime.setValue(newValue)

        try:
            newDuration = songDataHandler.getTag(self.songQueue.getCurrentSong()).duration
            if self.oldDuration != newDuration:
                self.ui.musicControlsTime.setValue(0)
                self.ui.musicControlsTime.setRange(0, int(newDuration))
            self.oldDuration = newDuration

            if newValue >= int(newDuration):
                self.ui.musicControlsTime.setValue(0)
                self.songQueue.goToNextSong()
        except Exception:
            pass #print('No song loaded')

    def setSongImage(self, songTitle: str, graphicsView, resolution: list = [150, 150]):
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
            pixmap.loadFromData(songDataHandler.getImgData(sqlHandler.songs.retrieveByTitle(songTitle)[3], resolution))
        except Exception:
            pixmap.loadFromData(songDataHandler.getImgData('covers/default.png'))
        graphicsScene.addPixmap(pixmap)
        graphicsView.setScene(graphicsScene)

    def setMainContentDisplay(self, content) -> None:
        container = self.ui.mainContent
        def clearContent(layout) -> None:
            # Clear existing content in the layout
            for i in reversed(range(layout.count())): 
                layoutItem = layout.itemAt(i)
                if layoutItem.widget() is not None:
                    layoutItem.widget().deleteLater()

        self.currentDisplayContent = content
        if content == "home":
            layout = container.layout()
            if layout is None:
                layout = QVBoxLayout()
                container.setLayout(layout)
            clearContent(layout)

            from contentHome import contentHomeWidget
            self.homeDisplay = contentHomeWidget(self)
            layout.addWidget(self.homeDisplay)

        elif content == "search":
            layout = self.ui.mainContent.layout()
            if layout is None:
                layout = QVBoxLayout()
                container.setLayout(layout)
            clearContent(layout)

            from contentSearch import contentSearchWidget
            self.searchDisplay = contentSearchWidget(self)
            layout.addWidget(self.searchDisplay)

        elif content == "playlist":
            layout = self.ui.mainContent.layout()
            if layout is None:
                layout = QVBoxLayout()
                container.setLayout(layout)
            clearContent(layout)

            from contentPlaylist import contentPlaylistWidget
            self.playlistDisplay = contentPlaylistWidget(self)
            layout.addWidget(self.playlistDisplay)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        """
        A function that handles the close event. Closes all top-level widgets except itself.
        """
        for widget in QApplication.topLevelWidgets():
            if widget is not self:
                widget.close()
        return super().closeEvent(a0)

if __name__ == '__main__':
    sqlHandler.database.createDB()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
