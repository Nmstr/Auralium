from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt

from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
UiCreatePlaylistPopover, BaseClass = uic.loadUiType('popovers/createPlaylistPopover/createPlaylistPopover.ui')

class CreatePlaylistPopover(BaseClass, UiCreatePlaylistPopover):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        self.importKeyCombo.addItem('title')
        self.importKeyCombo.addItem('filepath')
        self.importKeyCombo.addItem('sha256hash')
        self.createBtn.clicked.connect(lambda: self.createPlaylist())
        self.importBtn.clicked.connect(lambda: self.importPlaylist())

    def createPlaylist(self) -> None:
        """
        Create a new playlist.
        """
        playlistName = self.nameInput.text()
        if playlistName == '':
            return
        self.mainWindow.sqlHandler.playlists.create(playlistName, None, None, None)
        self.mainWindow.displayPlaylists()

        self.close()
    
    def importPlaylist(self) -> None:
        """
        Import a playlist.
        """
        
        # Read the file
        options = QFileDialog.Option.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "Open Playlist", "", "Playlist Files (*.json);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                data = f.read()
            data = json.loads(data)
            
            # Create the playlist
            playlistId = self.mainWindow.sqlHandler.playlists.create(data['name'], data['creator'], data['description'], None)
            for index, songDetails in data['songs'].items():
                try:
                    importKey = self.importKeyCombo.currentText()
                    if importKey == 'title':
                        songId = self.mainWindow.sqlHandler.songs.retrieveByTitle(songDetails['title'])[0]
                    elif importKey == 'filepath':
                        songId = self.mainWindow.sqlHandler.songs.retrieveByPath(songDetails['filepath'])[0]
                    elif importKey == 'sha256hash':
                        songId = self.mainWindow.sqlHandler.songs.retrieveBySha256Hash(songDetails['sha256hash'])[0]
                except TypeError as e:
                    print(e)
                    continue
                self.mainWindow.sqlHandler.playlists.addSong(playlistId, songId, int(index))
            self.mainWindow.displayPlaylists()

            self.close()

    def focusOutEvent(self, event) -> None:
        """
        Handle the focus out event.

        This method is called when the popover loses focus. It closes the popover and calls the parent's focus out event.
        """
        self.close()
        return super().focusOutEvent(event)
