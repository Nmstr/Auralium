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