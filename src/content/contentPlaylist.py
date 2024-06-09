from popovers.genericTextInputPopover.genericTextInputPopover import GenericTextInputPopover
from content.playlists.songEntry import SongEntryWidget

from PyQt6.QtWidgets import QVBoxLayout, QFileDialog
from PyQt6.QtCore import QPoint

from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
UiContentPlaylist, BaseClass = uic.loadUiType('content/contentPlaylist.ui')

class ContentPlaylistWidget(BaseClass, UiContentPlaylist):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.playlist = None

        super().__init__()
        self.setupUi(self)

        self.deleteBtn.clicked.connect(lambda: self.showPlaylistActionPopover(action='delete'))
        self.renameBtn.clicked.connect(lambda: self.showPlaylistActionPopover(action='rename'))
        self.playBtn.clicked.connect(lambda: self.playPlaylist())
        self.exportBtn.clicked.connect(lambda: self.exportPlaylist)

    def updatePlaylist(self, playlist):
        self.playlist = playlist
        self.mainWindow.playlistDisplay.playlistIdLabel.setText(str(self.playlist[0]))
        self.mainWindow.playlistDisplay.playlistNameLabel.setText(self.playlist[1])
        self.mainWindow.playlistDisplay.playlistNameLabelImg.setText(self.playlist[1])
        self.mainWindow.playlistDisplay.playlistCreatorLabel.setText(self.playlist[2])
        self.mainWindow.playlistDisplay.playlistDescriptionLabel.setText(self.playlist[3])
        self.mainWindow.songDataHandler.setSongImage(self.playlist[1], self.mainWindow.playlistDisplay.playlistImg) # TODO: actually add proper img support instead of using placeholder img from song img recovery
        self.playlist = self.mainWindow.sqlHandler.playlists.retrieve(self.playlist[0])
        if self.playlist[5]:
            self.mainWindow.playlistDisplay.playlistLengthLabel.setText('Songs: ' + str(len(json.loads(self.playlist[-1]))))
        else:
            self.mainWindow.playlistDisplay.playlistLengthLabel.setText('Songs: 0')

        self.displaySongsInPlaylist()

    def playPlaylist(self) -> None:
        """
        Play the playlist
        """
        if self.playlist[5]:
            playlist = json.loads(self.playlist[-1])
            song = self.mainWindow.sqlHandler.songs.retrieveById(playlist[0])
            self.mainWindow.songQueue.addAndSetCurrentSong(song[3])
            self.mainWindow.songQueue.playingPlaylist = [self.playlist, 0]

    def exportPlaylist(self) -> None:
        """
        Exports the playlist to a .csv file
        """
        playlistData = {
            'name': self.playlist[1],
            'creator': self.playlist[2],
            'description': self.playlist[3],
            'length': len(json.loads(self.playlist[5])),
            'songs': {

            }
        }
        for i, song in enumerate(json.loads(self.playlist[5])):
            songData = self.mainWindow.sqlHandler.songs.retrieveById(song)
            playlistData['songs'][i] = {
                'title': songData[1],
                'artist': songData[2],
                'filepath': songData[3],
                'sha256hash': songData[4],
                'source': songData[5],
                'release_date': songData[6],
                'deleted': songData[7]
            }
        
        options = QFileDialog.Option.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None, "Save Playlist", "", "Playlist Files (*.json);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                json.dump(playlistData, f, indent=4)

    def showPlaylistActionPopover(self, *, action: str) -> None:
        """
        Shows the delete playlist popover.

        Args:
            action (str): The action to perform. Can be 'delete' or 'rename'.
        """
        if action == 'delete':
            popover = GenericTextInputPopover(self.mainWindow, popoverType='deletePlaylist', playlist=self.playlist)
            buttonPos = self.mainWindow.playlistDisplay.deleteBtn.mapToGlobal(QPoint(0, 0))
        elif action == 'rename':
            popover = GenericTextInputPopover(self.mainWindow, popoverType='renamePlaylist', playlist=self.playlist)
            buttonPos = self.mainWindow.playlistDisplay.renameBtn.mapToGlobal(QPoint(0, 0))
        
        # Calculate the position of the popover
        popoverPosX = buttonPos.x() + self.mainWindow.playlistDisplay.deleteBtn.width()/2
        popoverPosY = buttonPos.y() + self.mainWindow.playlistDisplay.deleteBtn.height()/2
        
        # Set the position and size of the popover
        popover.setGeometry(int(popoverPosX), int(popoverPosY), 300, 100)
        popover.show()

    def displaySongsInPlaylist(self) -> None:
        """
        Displays the songs in the playlist in the playlist display widget.

        This function retrieves the container widget for the playlist display and checks if it has a layout. If not, a new QVBoxLayout is set.
        Existing content in the layout is cleared.
        Then, custom widgets are dynamically added to the layout for each song in the playlist.
        """
        container = self.mainWindow.playlistDisplay.playlistSongs

        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())):
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                layoutItem.widget().deleteLater()

        # Dynamically add custom widgets for each playlist
        if not self.playlist[5] is None:
            for songIndex, song in enumerate(json.loads(self.playlist[5])):
                playlistWidget = SongEntryWidget(song, songIndex, self.mainWindow, self)
                layout.addWidget(playlistWidget)
