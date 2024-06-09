from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiGenericTextInputPopover, BaseClass = uic.loadUiType('popovers/genericTextInputPopover/genericTextInputPopover.ui')

class GenericTextInputPopover(BaseClass, UiGenericTextInputPopover):
    def __init__(self, mainWindow, *, popoverType, **kwargs):
        self.mainWindow = mainWindow

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        if popoverType == 'deletePlaylist':
            self.playlist = kwargs['playlist']
            self.textInput.setPlaceholderText("Enter playlist name")
            self.informationLabel.setText("Delete Playlist")
            self.confirmBtn.setText("Delete")
            self.confirmBtn.clicked.connect(lambda: self.deletePlaylist())
        elif popoverType == 'renamePlaylist':
            self.playlist = kwargs['playlist']
            self.textInput.setPlaceholderText("Enter new playlist name")
            self.informationLabel.setText("Rename Playlist")
            self.confirmBtn.setText("Rename")
            self.confirmBtn.clicked.connect(lambda: self.renamePlaylist())

    def deletePlaylist(self) -> None:
        """
        Create a new playlist.
        """
        playlistName = self.textInput.text()
        if playlistName != self.playlist[1]:
            return
        self.mainWindow.sqlHandler.playlists.delete(self.playlist[0])
        self.mainWindow.displayPlaylists()
        self.mainWindow.setMainContentDisplay('home')

        self.close()
    
    def renamePlaylist(self) -> None:
        """
        Create a new playlist.
        """
        playlistName = self.textInput.text()
        if playlistName == '':
            return
        self.mainWindow.sqlHandler.playlists.rename(self.playlist[0], playlistName)
        self.mainWindow.displayPlaylists()
        self.playlist = self.mainWindow.sqlHandler.playlists.retrieve(self.mainWindow.playlistDisplay.playlist[0])
        self.mainWindow.playlistDisplay.updatePlaylist(self.playlist)

        self.close()

    def focusOutEvent(self, event) -> None:
        """
        Handle the focus out event.

        This method is called when the popover loses focus. It closes the popover and calls the parent's focus out event.
        """
        self.close()
        return super().focusOutEvent(event)
