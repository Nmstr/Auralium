from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiCreatePlaylistPopover, BaseClass = uic.loadUiType('popovers/createPlaylistPopover/createPlaylistPopover.ui')

class CreatePlaylistPopover(BaseClass, UiCreatePlaylistPopover):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        self.createBtn.clicked.connect(lambda: self.createPlaylist())

    def createPlaylist(self) -> None:
        """
        Create a new playlist.
        """
        playlistName = self.nameInput.text()
        if playlistName == '':
            return
        self.sqlHandler.playlists.create(playlistName, None, None, None)
        self.mainWindow.displayPlaylists()

        self.close()

    def focusOutEvent(self, event) -> None:
        """
        Handle the focus out event.

        This method is called when the popover loses focus. It closes the popover and calls the parent's focus out event.
        """
        self.close()
        return super().focusOutEvent(event)
