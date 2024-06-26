from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContextPopover, BaseClass = uic.loadUiType('popovers/contextPopover/contextPopover.ui')

class ContextPopover(BaseClass, UiContextPopover):
    def __init__(self, mainWindow, song):
        self.mainWindow = mainWindow
        self.song = song

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        # Add all playlists to combo box
        playlists = self.mainWindow.sqlHandler.playlists.retrieveAll()
        for playlist in playlists:
            self.playlistInputComboBox.addItem(playlist[1], userData=playlist[0])

        self.playBtn.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(song['data'][3]))
        self.addToQueueBtn.clicked.connect(lambda: self.mainWindow.songQueue.addSong(self.song['data'][3]))
        self.addToPlaylistBtn.clicked.connect(lambda: self.addSongToPlaylist())

    def addSongToPlaylist(self) -> None:
        """
        A function to add a song to a playlist in the database.
        """
        playlistId = self.playlistInputComboBox.currentData()
        playlist = self.mainWindow.sqlHandler.playlists.retrieve(playlistId)
        # Add the song to the in database playlist
        if playlist[5] is None or playlist[5] == []:
            self.mainWindow.sqlHandler.playlists.addSong(playlist[0], self.song['data'][0], 0)
        else:
            self.mainWindow.sqlHandler.playlists.addSong(playlist[0], self.song['data'][0], len(playlist[5]))

    def mousePressEvent(self, event) -> None:
        """
        Close the context popover when the user right clicks
        """
        if event.button() == Qt.MouseButton.RightButton:
            self.close()
        return super().mousePressEvent(event)

    def focusOutEvent(self, event):
        """
        Close the context popover when the user clicks outside of it
        """
        self.close()
        return super().focusOutEvent(event)
