from sqlHandler import sqlHandler

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic

# Load the .ui file and get the base class and form class
Ui_PlaylistItem, BaseClass = uic.loadUiType('playlistSongEntry.ui')

class SongItemWidget(BaseClass, Ui_PlaylistItem):
    def __init__(self, song, mainWindow):
        self.song = sqlHandler.songs.retrieveById(song[0])
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(self.song[1])
        self.artistLabel.setText(self.song[2])
        self.mainWindow.setSongImage(self.song[1], self.coverImg, [100, 100])

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