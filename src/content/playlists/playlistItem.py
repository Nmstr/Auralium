from content.playlists.songItem import SongItemWidget

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
UiPlaylistItem, BaseClass = uic.loadUiType('content/playlists/playlistsEntry.ui')

class PlaylistItemWidget(BaseClass, UiPlaylistItem):
    def __init__(self, playlist, mainWindow, sqlHandler):
        self.playlist = playlist # Assign playlist to self.playlist to make it accessible in other functions
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(playlist[1])
        self.creatorLabel.setText(playlist[2])

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
            self.mainWindow.setMainContentDisplay('playlist')
            self.mainWindow.playlistDisplay.playlistIdLabel.setText(str(self.playlist[0]))
            self.mainWindow.playlistDisplay.playlistNameLabel.setText(self.playlist[1])
            self.mainWindow.playlistDisplay.playlistCreatorLabel.setText(self.playlist[2])
            self.mainWindow.playlistDisplay.playlistDescriptionLabel.setText(self.playlist[3])
            self.mainWindow.songDataHandler.setSongImage(self.playlist[1], self.mainWindow.playlistDisplay.playlistImg) # TODO: actually add proper img support instead of using placeholder img from song img recovery
            self.playlist = self.sqlHandler.playlists.retrieve(self.playlist[0])
            if self.playlist[5]:
                self.mainWindow.playlistDisplay.playlistLengthLabel.setText('Songs: ' + str(len(json.loads(self.playlist[-1]))))
            else:
                self.mainWindow.playlistDisplay.playlistLengthLabel.setText('Songs: 0')
            self.mainWindow.playlistDisplay.playBtn.clicked.connect(lambda: self.playPlaylist())
            
            self.displaySongsInPlaylist()
            return super().mousePressEvent(event)

    def playPlaylist(self) -> None:
        """
        Play the playlist
        """
        if self.playlist[5]:
            playlist = json.loads(self.playlist[-1])
            song = self.sqlHandler.songs.retrieveById(playlist[0])
            self.mainWindow.songQueue.addAndSetCurrentSong(song[3])
            self.mainWindow.songQueue.playingPlaylist = [self.playlist, 0]

    def enterEvent(self, event) -> None:
        """
        Handle the mouse enter event.

        Parameters:
            event (QEnterEvent): The enter event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("background-color: #333;")
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """
        Handle the mouse leave event.

        Parameters:
            event (QEvent): The leave event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("")
        return super().leaveEvent(event)

    def displaySongsInPlaylist(self) -> None:
        """
        Displays the songs in the playlist in the playlist display widget.

        This function retrieves the container widget for the playlist display and checks if it has a layout. If not, a new QVBoxLayout is set.
        Existing content in the layout is cleared.
        Then, custom widgets are dynamically added to the layout for each song in the playlist.
        """
        container = self.mainWindow.playlistDisplay.playlistSongs

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
        if not self.playlist[5] is None:
            for songIndex, song in enumerate(json.loads(self.playlist[5])):
                playlistWidget = SongItemWidget(song, songIndex, self.mainWindow, self, self.sqlHandler)
                layout.addWidget(playlistWidget)
