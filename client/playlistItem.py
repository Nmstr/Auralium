from songItem import SongItemWidget

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
Ui_PlaylistItem, BaseClass = uic.loadUiType('playlistsEntry.ui')

class PlaylistItemWidget(BaseClass, Ui_PlaylistItem):
    def __init__(self, playlist, mainWindow):
        self.playlist = playlist # Assign playlist to self.playlist to make it accessible in other functions
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(playlist[1])
        self.creatorLabel.setText(playlist[2])

        # Enable mouse tracking
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event) -> None:
        """
        Handle the mouse press event.

        This function is called when a mouse button is pressed. It checks if the left mouse button was pressed and if so, executes the function.

        Parameters:
            event (QMouseEvent): The mouse event that triggered the function.

        Returns:
            None
        """
        if event.button() == Qt.MouseButton.LeftButton:
            print("Frame clicked!")
            print(self.playlist)
            self.mainWindow.ui.mainContentStack.setCurrentWidget(self.mainWindow.ui.playlistView)
            self.mainWindow.ui.playlistIdLabel.setText(str(self.playlist[0]))
            self.mainWindow.ui.playlistNameLabel.setText(self.playlist[1])
            self.mainWindow.ui.playlistCreatorLabel.setText(self.playlist[2])
            self.mainWindow.ui.playlistDescriptionLabel.setText(self.playlist[3])
            self.mainWindow.setSongImage(self.playlist[1], self.mainWindow.ui.playlistImg) # TODO: actually add proper img support instead of using placeholder img from song img recovery
            self.displaySongsInPlaylist()

    def enterEvent(self, event):
        """
        Handle the mouse enter event.

        Parameters:
            event (QEnterEvent): The enter event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("background-color: #333;")

    def leaveEvent(self, event):
        """
        Handle the mouse leave event.

        Parameters:
            event (QEvent): The leave event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("")

    def displaySongsInPlaylist(self) -> None:
        # Get the container widget
        container = self.mainWindow.ui.playlistSongs
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
        if self.playlist[5] is None:
            print("No songs in playlist")
        else:
            for song in json.loads(self.playlist[5]):
                playlistWidget = SongItemWidget(song, self.mainWindow)
                layout.addWidget(playlistWidget)