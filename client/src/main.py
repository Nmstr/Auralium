from debug.debugWindow import DebugWindow

from content.contentPlaylist import ContentPlaylistWidget
from content.contentSearch import ContentSearchWidget
from content.contentHome import ContentHomeWidget

from content.playlists.playlistItem import PlaylistItemWidget
from bottomBar.bottomBar import bottomBarWidget
from sqlHandler import sqlHandler
from songQueue import SongQueue
import songDataHandler

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QVBoxLayout
from PyQt6.QtGui import QCloseEvent, QPixmap, QAction
from PyQt6 import uic

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Create song queue
        self.songQueue = SongQueue()

        # Set the main content and add the bottom bar
        self.setMainContentDisplay("home")
        self.addBottomBarWidget()

        # Create hotkey action
        self.hotkeyAction = QAction(self)
        self.hotkeyAction.setShortcut("F12")
        self.hotkeyAction.triggered.connect(lambda: DebugWindow())
        self.addAction(self.hotkeyAction)

        # Connect buttons for applications
        self.ui.homeBtn.clicked.connect(lambda: self.setMainContentDisplay('home'))
        self.ui.searchBtn.clicked.connect(lambda: self.setMainContentDisplay('search'))

        # Connect playlist buttons
        self.ui.playlistsCreateBtn.clicked.connect(lambda: sqlHandler.playlists.create('dadwdaddawkuuhku', None, None, None))
        self.ui.playlistsCreateBtn.clicked.connect(lambda: self.displayPlaylists())

        # Call the method to display playlists at initialization
        self.displayPlaylists()

        # Load stylesheet from file
        with open('style.qss', 'r') as f:
            app.setStyleSheet(f.read())

        self.show()

    def addBottomBarWidget(self) -> None:
        """
        Add bnottom bar widget to the UI.
        - None
        """
        container = self.ui.bottomBar
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)
        # Create the bottom bar
        self.bottomBar = bottomBarWidget(self)
        layout.addWidget(self.bottomBar)

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

    def setSongImage(self, songTitle: str, graphicsView, resolution: list = [150, 150]):
        """
        A function that sets the image of a song in a graphics view.

        Parameters:
        - songTitle: str, the title of the song to set the image for
        - graphicsView: the graphics view where the image will be set
        - resolution: list, the resolution of the image

        Returns:
        - None
        """
        graphicsScene = QGraphicsScene()
        pixmap = QPixmap()
        try:
            pixmap.loadFromData(songDataHandler.getImgData(sqlHandler.songs.retrieveByTitle(songTitle)[3], resolution))
        except Exception as e:
            pixmap.loadFromData(songDataHandler.getImgData('covers/default.png'))
        graphicsScene.addPixmap(pixmap)
        graphicsView.setScene(graphicsScene)

    def setMainContentDisplay(self, content) -> None:
        """
        A function that sets the main content display based on the content parameter.

        Parameters:
        - content: the type of content to display
        """
        container = self.ui.mainContent
        layout = container.layout()
        # Create a new layout if it doesn't exist
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())): 
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                layoutItem.widget().deleteLater()

        # Change the mainContent widget
        if content == "home":
            self.homeDisplay = ContentHomeWidget(self)
            layout.addWidget(self.homeDisplay)
        elif content == "search":
            self.searchDisplay = ContentSearchWidget(self)
            layout.addWidget(self.searchDisplay)
        elif content == "playlist":
            self.playlistDisplay = ContentPlaylistWidget(self)
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
