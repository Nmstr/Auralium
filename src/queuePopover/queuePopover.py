from queuePopover.queueEntry import QueueEntryWidget

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt

from PyQt6 import uic

import json

# Load the .ui file and get the base class and form class
UiQueuePopover, BaseClass = uic.loadUiType('queuePopover/queuePopover.ui')

class QueuePopover(BaseClass, UiQueuePopover):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler

        super().__init__(mainWindow, Qt.WindowType.Popup)
        self.setupUi(self)

        self.addNowPlayingQueueItem()
        self.addNextInQueueItem()
        self.addNextInPlaylistItem()

    def addNowPlayingQueueItem(self):
        # Get the current song
        currentSong = self.mainWindow.songQueue.getCurrentSong()

        container = self.playingItemsFrame
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Add custom Widgets for the song
        if currentSong is not None:
            self.nowPlayingQueue = QueueEntryWidget(self.sqlHandler.songs.retrieveByPath(currentSong), self.mainWindow)
            layout.addWidget(self.nowPlayingQueue)

    def addNextInQueueItem(self):
        # Get the next songs in the queue
        songsInQueue = self.mainWindow.songQueue.queue
        index = self.mainWindow.songQueue.currentSongIndex
        songsNextInQueue = songsInQueue[index+1:]

        container = self.queueItemsFrame
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Add custom Widgets for the next songs from queue
        for song in songsNextInQueue:
            self.nextInQueue = QueueEntryWidget(self.sqlHandler.songs.retrieveByPath(song), self.mainWindow)
            layout.addWidget(self.nextInQueue)

    def addNextInPlaylistItem(self):
        # Get the next songs in the playlist
        songsInPlaylist = self.mainWindow.songQueue.playingPlaylist
        if songsInPlaylist is None: # If there are no songs in the playlist return
            return
        songsInPlaylist = json.loads(songsInPlaylist[0][5])
        index = self.mainWindow.songQueue.playingPlaylist[1]
        songsNextInPlaylist = songsInPlaylist[index+1:]

        container = self.playlistItemsFrame
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Add custom Widgets for the next songs from playlist
        for song in songsNextInPlaylist:
            songData = self.sqlHandler.songs.retrieveById(song)
            if songData[7] == 0: # Only add enabled songs
                self.nextInPlaylist = QueueEntryWidget(songData, self.mainWindow)
                layout.addWidget(self.nextInPlaylist)

    def focusOutEvent(self, event):
        # Close the popover when it loses focus
        self.close()
        super().focusOutEvent(event)
