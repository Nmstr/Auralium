from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
UiSongEntry, BaseClass = uic.loadUiType('content/playlists/songEntry.ui')

class SongEntryWidget(BaseClass, UiSongEntry):
    def __init__(self, song, songIndex, mainWindow, parent):
        self.mainWindow = mainWindow
        self.song = self.mainWindow.sqlHandler.songs.retrieveById(song)
        self.songIndex = songIndex
        self.parent = parent

        super().__init__()
        self.setupUi(self)

        # Set song info
        self.nameLabel.setText(self.song[1])
        self.artistLabel.setText(self.song[2])
        self.mainWindow.songDataHandler.setSongImage(self.song[1], self.coverImg, [100, 100])

        duration = round(self.mainWindow.songDataHandler.getTag(self.song[3]).duration)
        minutes, seconds = divmod(duration, 60)
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        self.lengthLabel.setText(f'{minutes}:{seconds}')
        self.lengthLabel.setToolTip(f'{duration} seconds')

        # Connect move button
        self.goUpBtn.clicked.connect(lambda: self.goSongUp(self.songIndex))
        self.goDownBtn.clicked.connect(lambda: self.goSongDown(self.songIndex))

        # Grey out if disabled
        if self.song[7] == 1:
            self.setEnabled(False)

        # Create the context menu
        self.mainContextMenu = QMenu(self)
        self.addSongToPlaylistContextMenu = QMenu(self)
        # Add actions to the context menu
        addSongToQueue = self.mainContextMenu.addAction("Add to queue")
        removeSongFromPlaylist = self.mainContextMenu.addAction("Remove from this playlist")
        addSongToPlaylist = self.mainContextMenu.addMenu("Add to playlist")

        playlists = self.mainWindow.sqlHandler.playlists.retrieveAll()
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

    def goSongUp(self, songIndex: int) -> None:
        """
        Move the song up in the playlist.

        Parameters:
        - songIndex: int, the index of the song in the playlist
        """
        moveDistance = self.goDistanceInput.value()
        if moveDistance == 0:
            return
        if songIndex - moveDistance < 0:
            return
        self.mainWindow.sqlHandler.playlists.moveSong(self.parent.playlist[0], songIndex, songIndex - moveDistance)
        self.parent.playlist = self.mainWindow.sqlHandler.playlists.retrieve(self.parent.playlist[0])
        self.parent.displaySongsInPlaylist()

    def goSongDown(self, songIndex: int) -> None:
        """
        Move the song down in the playlist.

        Parameters:
        - songIndex: int, the index of the song in the playlist
        """
        moveDistance = self.goDistanceInput.value()
        if moveDistance == 0:
            return
        if songIndex + moveDistance >= len(self.parent.playlist[5]):
            return
        self.mainWindow.sqlHandler.playlists.moveSong(self.parent.playlist[0], songIndex, songIndex + moveDistance)
        self.parent.playlist = self.mainWindow.sqlHandler.playlists.retrieve(self.parent.playlist[0])
        self.parent.displaySongsInPlaylist()

    def addSongToPlaylist(self, playlist: tuple, song: tuple) -> None:
        """
        Add the song to the playlist.

        Parameters:
        - playlist: tuple, the playlist to add the song to
        - song: tuple, the song to add to the playlist
        """
        # Add the song to the in database playlist
        self.mainWindow.sqlHandler.playlists.addSong(playlist[0], song[0], len(playlist[5]))

    def removeSong(self) -> None:
        """
        Remove the song from the playlist.
        """
        self.mainWindow.sqlHandler.playlists.removeSong(self.parent.playlist[0], self.songIndex) # Remove the song from the database playlist
        
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
            return super().mousePressEvent(event)

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
 
    def contextMenuEvent(self, event) -> None:
        self.mainContextMenu.exec(event.globalPos())
        return super().contextMenuEvent(event)
