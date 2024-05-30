from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContextPopover, BaseClass = uic.loadUiType('contextPopover/contextPopover.ui')

class ContextPopover(BaseClass, UiContextPopover):
    def __init__(self, mainWindow, song, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler
        self.song = song

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        # Add all playlists to combo box
        playlists = self.sqlHandler.playlists.retrieveAll()
        for playlist in playlists:
            self.playlistInputComboBox.addItem(playlist[1], userData=playlist[0])

        self.playBtn.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(song[3]))
        self.addToQueueBtn.clicked.connect(lambda: self.mainWindow.songQueue.addSong(self.song[3]))
        self.addToPlaylistBtn.clicked.connect(lambda: self.addSongToPlaylist())

    def addSongToPlaylist(self):
        playlistId = self.playlistInputComboBox.currentData()
        playlist = self.sqlHandler.playlists.retrieve(playlistId)
        # Add the song to the in database playlist
        if playlist[5] is None or playlist[5] == []:
            self.sqlHandler.playlists.addSong(playlist[0], self.song[0], 0)
        else:
            self.sqlHandler.playlists.addSong(playlist[0], self.song[0], len(playlist[5]))

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            self.close()
        super().mousePressEvent(event)

    def focusOutEvent(self, event):
        # Close the popover when it loses focus
        self.close()
        super().focusOutEvent(event)
