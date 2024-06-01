from debug.debugWindow import DebugWindow

from content.contentPlaylist import ContentPlaylistWidget
from content.contentSearch import ContentSearchWidget
from content.contentHome import ContentHomeWidget
from settings.settings import SettingsWidget

from content.playlists.playlistItem import PlaylistItemWidget
from bars.bottomBar.bottomBar import BottomBarWidget
from bars.sidebar.sidebar import SidebarWidget

from preferenceHandler import PreferenceHandler
from songDataHandler import SongDataHandler
from songQueue import SongQueue
import sqlHandler

from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QVBoxLayout
from PyQt6.QtGui import QCloseEvent, QPixmap, QAction
from PyQt6 import uic

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        # Create song queue
        self.sqlHandler = sqlHandler
        self.songQueue = SongQueue(self.sqlHandler)
        self.songDataHandler = SongDataHandler(self.sqlHandler)

        # Add preference handler to self
        self.preferenceHandler = preferenceHandler

        # Set the main content and add the bars
        self.setMainContentDisplay("home")
        self.addBottomBarWidget()
        self.addSidebarWidget()

        # Create hotkey action
        self.hotkeyAction = QAction(self)
        self.hotkeyAction.setShortcut("F12")
        self.hotkeyAction.triggered.connect(lambda: DebugWindow(self.sqlHandler))
        self.addAction(self.hotkeyAction)

        # Connect top bar buttons
        self.ui.homeBtn.clicked.connect(lambda: self.setMainContentDisplay('home'))
        self.ui.searchBtn.clicked.connect(lambda: self.setMainContentDisplay('search'))
        self.ui.settingsBtn.clicked.connect(lambda: self.setMainContentDisplay('settings'))

        # Call the method to display playlists at initialization
        self.displayPlaylists()

        self.show()

    def addBottomBarWidget(self) -> None:
        """
        Add bottom bar widget to the UI.
        - None
        """
        container = self.ui.bottomBar
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)
        # Create the bottom bar
        self.bottomBar = BottomBarWidget(self, self.sqlHandler)
        layout.addWidget(self.bottomBar)

    def addSidebarWidget(self) -> None:
        """
        Add sidebar widget to the UI.
        - None
        """
        container = self.ui.sidebarContainer
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)
        # Create the sidebar
        self.sidebar = SidebarWidget(self, self.sqlHandler)
        layout.addWidget(self.sidebar)

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
        playlists = self.sqlHandler.playlists.retrieveAll()

        # Get the container widget
        container = self.sidebar.playlistsScrollAreaWidgetContents
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
            playlistWidget = PlaylistItemWidget(playlist, self, self.sqlHandler)
            layout.addWidget(playlistWidget)

    def setMainContentDisplay(self, content: str) -> None:
        """
        A function that sets the main content display based on the content parameter.

        Parameters:
        - content: (str) the type of content to display
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
            self.homeDisplay = ContentHomeWidget(self, self.sqlHandler)
            layout.addWidget(self.homeDisplay)
        elif content == "search":
            self.searchDisplay = ContentSearchWidget(self, self.sqlHandler)
            layout.addWidget(self.searchDisplay)
        elif content == "playlist":
            self.playlistDisplay = ContentPlaylistWidget(self)
            layout.addWidget(self.playlistDisplay)
        elif content == "settings":
            self.settingsDisplay = SettingsWidget(self)
            layout.addWidget(self.settingsDisplay)

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
    preferenceHandler = PreferenceHandler(QApplication=QApplication, app=app)
    window = MainWindow()
    sys.exit(app.exec())
