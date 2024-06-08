from PyQt6.QtCore import Qt

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiPlaylistEntry, BaseClass = uic.loadUiType('content/playlists/playlistEntry.ui')

class PlaylistEntryWidget(BaseClass, UiPlaylistEntry):
    def __init__(self, playlist, mainWindow):
        self.mainWindow = mainWindow
        self.playlist = playlist

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
            self.mainWindow.playlistDisplay.updatePlaylist(self.playlist)

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
