from sqlHandler import sqlHandler

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic

from PyQt6.QtWidgets import QWidget, QMenu, QApplication

import json
import sys

# Load the .ui file and get the base class and form class
UiSongItem, BaseClass = uic.loadUiType('playlistSongEntry.ui')

class SongItemWidget(BaseClass, UiSongItem):
    def __init__(self, song, songIndex, mainWindow, parent):
        self.song = sqlHandler.songs.retrieveById(song)
        self.mainWindow = mainWindow
        self.songIndex = songIndex
        self.parent = parent

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(self.song[1])
        self.artistLabel.setText(self.song[2])
        self.mainWindow.setSongImage(self.song[1], self.coverImg, [100, 100])

        # Create the context menu
        self.mainContextMenu = QMenu(self)
        self.addSongToPlaylistContextMenu = QMenu(self)
        # Add actions to the context menu
        addSongToQueue = self.mainContextMenu.addAction("Add to queue")
        removeSongFromPlaylist = self.mainContextMenu.addAction("Remove from this playlist")
        addSongToPlaylist = self.mainContextMenu.addMenu("Add to playlist")

        playlists = sqlHandler.playlists.retrieveAll()
        # Clear existing actions from the submenu
        self.addSongToPlaylistContextMenu.clear()

        # Add actions to the submenu
        for playlist in playlists:
            action = self.addSongToPlaylistContextMenu.addAction(f'{playlist[1]} ({playlist[0]})')
            addSongToPlaylist.addAction(action)
            action.triggered.connect(lambda checked, p=playlist, s=self.song: self.addSongToPlaylist(p, s))

        # Connect the actions to methods
        addSongToQueue.triggered.connect(lambda: self.mainWindow.songQueue.addSong(self.song[3]))
        removeSongFromPlaylist.triggered.connect(self.removeSong)

    def addSongToPlaylist(self, playlist, song):
        # Add the song to the in database playlist
        sqlHandler.playlists.addSong(playlist[0], song[0], len(playlist[5]))

    def removeSong(self):
        # Remove the song from the in database playlist
        sqlHandler.playlists.removeSong(self.parent.playlist[0], self.songIndex) # Remove the song from the database playlist
        
        # Remove the song from the in memory playlist
        playlist = list(self.parent.playlist) # Convert the tuple to a list
        songs = json.loads(playlist[5])
        songs.pop(self.songIndex)
        playlist[5] = json.dumps(songs)
        self.parent.playlist = tuple(playlist) # Convert the list back to a tuple

        # Re-display the songs in the playlist
        self.parent.displaySongsInPlaylist()

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
            self.mainWindow.songQueue.addAndSetCurrentSong(self.song[3])
            self.mainWindow.songQueue.playingPlaylist = [self.parent.playlist, self.songIndex]

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
 
    def contextMenuEvent(self, event):
        # Show the context menu
        self.mainContextMenu.exec(event.globalPos())
 