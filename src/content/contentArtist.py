from content.search.topResultSong import SearchTopResultSongWidget

from PyQt6.QtWidgets import QHBoxLayout

from PyQt6 import uic

import random

# Load the .ui file and get the base class and form class
UiContentArtist, BaseClass = uic.loadUiType('content/contentArtist.ui')

class ContentArtistWidget(BaseClass, UiContentArtist):
    def __init__(self, mainWindow, artist):
        self.mainWindow = mainWindow
        self.artist = artist

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(artist['data'][1])

        self.homeBtn.clicked.connect(lambda: self.displaySongs('home'))
        self.songsBtn.clicked.connect(lambda: self.displaySongs('songs'))

        self.displaySongs('home')

    def displaySongs(self, area) -> None:
        """
        Dynamically add custom widgets for each song in the search results.
        This adds to the top search results

        Parameters:
            songs (list): The list of songs to display in the search results.
        """
        # Retrieve songs to display
        allSongs = self.mainWindow.sqlHandler.songs.retrieveByArtist(self.artist['data'][1])
        if area == 'home':                                                  #
            randomSongs = random.sample(allSongs, min(len(allSongs), 3))    #
            selectedSongs = []                                              #
            for song in randomSongs:                                        #
                selectedSongs.append({'itemType': 'song', 'data': song})    # Todo: Fix this shit once dedicated widget for songs in home is created
        elif area == 'songs':                                               #
            selectedSongs = []                                              #
            for song in allSongs:                                           #
                selectedSongs.append({'itemType': 'song', 'data': song})    #

        container = self.bottom
        # Check if the container has a layout, if not, set a new QHBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QHBoxLayout()
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())):
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                layoutItem.widget().deleteLater()

        # Dynamically add custom widgets for each song
        for item in selectedSongs:
            searchTopResultWidget = SearchTopResultSongWidget(self.mainWindow, song=item)
            layout.addWidget(searchTopResultWidget)
