from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiDeletePlaylistPopover, BaseClass = uic.loadUiType('popovers/deletePlaylistPopover/deletePlaylistPopover.ui')

class DeletePlaylistPopover(BaseClass, UiDeletePlaylistPopover):
    def __init__(self, mainWindow, sqlHandler, playlist):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler
        self.playlist = playlist

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        self.deleteBtn.clicked.connect(lambda: self.deletePlaylist())

    def deletePlaylist(self) -> None:
        """
        Create a new playlist.
        """
        playlistName = self.nameInput.text()
        if playlistName != self.playlist[1]:
            return
        self.sqlHandler.playlists.delete(self.playlist[0])
        self.mainWindow.displayPlaylists()
        self.mainWindow.setMainContentDisplay('home')

        self.close()
    
    def focusOutEvent(self, event) -> None:
        """
        Handle the focus out event.

        This method is called when the popover loses focus. It closes the popover and calls the parent's focus out event.
        """
        self.close()
        return super().focusOutEvent(event)
