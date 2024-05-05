from sqlHandler import sqlHandler

from PyQt6 import uic

import difflib

# Load the .ui file and get the base class and form class
Ui_PlaylistItem, BaseClass = uic.loadUiType('contentSearch.ui')

class contentSearchWidget(BaseClass, Ui_PlaylistItem):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Connect buttons/text fields for search
        self.searchBarTextChange('') # Trigger searchBarTextChange once on startup
        self.searchBar.textChanged.connect(self.searchBarTextChange)
        self.searchFilterAllBtn.clicked.connect(self.switchSearchFilter)
        self.searchFilterSongsBtn.clicked.connect(self.switchSearchFilter)
        self.searchFilterArtistsBtn.clicked.connect(self.switchSearchFilter)

        # Connect play buttons on top results and set defalt text
        self.searchTopResults0Play.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(sqlHandler.songs.retrieveByTitle(self.searchTopResult0Name.text())[3]))
        self.searchTopResults1Play.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(sqlHandler.songs.retrieveByTitle(self.searchTopResult1Name.text())[3]))
        self.searchTopResults2Play.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(sqlHandler.songs.retrieveByTitle(self.searchTopResult2Name.text())[3]))

        # Enable mouse tracking
        self.setMouseTracking(True)

    def searchBarTextChange(self, text):
        """
        This function handles the search functionality based on the search bar text.
        
        Parameters:
            text (str): The text entered in the search bar.
        """
        try:
            allSongs = sqlHandler.songs.retrieveAll()
            # Create a list of concatenated title and artist for matching
            titlesArtists = [song[1] + " " + song[2] for song in allSongs]
            similarTitlesArtists = difflib.get_close_matches(text, titlesArtists, n=3, cutoff=0.05)
            
            # Map the similar strings back to the original song tuples
            similar = [song for song in allSongs if (song[1] + " " + song[2]) in similarTitlesArtists]

            similar = similar + [sqlHandler.songs.retrieveRandomSong() for _ in range(3 - len(similar))]
        except Exception as e:
            # If there's an error, fill in with random songs
            similar = [sqlHandler.songs.retrieveRandomSong() for _ in range(3)]
            print(e)

        # Update top results labels
        self.searchTopResult0Name.setText(similar[0][1])
        self.searchTopResult1Name.setText(similar[1][1])
        self.searchTopResult2Name.setText(similar[2][1])
        self.searchTopResult0Artist.setText(similar[0][2])
        self.searchTopResult1Artist.setText(similar[1][2])
        self.searchTopResult2Artist.setText(similar[2][2])
        
        # Update top results images
        self.mainWindow.setSongImage(similar[0][1], self.searchTopResults0Img)
        self.mainWindow.setSongImage(similar[1][1], self.searchTopResults1Img)
        self.mainWindow.setSongImage(similar[2][1], self.searchTopResults2Img)

    def switchSearchFilter(self, filter):
        """
        This function handles the switching of search filters based on the senderName and the filter value.
        """
        senderName = self.sender().objectName()

        if senderName == 'searchFilterAllBtn' and filter == True:
            self.ui.searchFilterSongsBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)
        elif senderName == 'searchFilterSongsBtn' and filter == True:
            self.ui.searchFilterAllBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)
        elif senderName == 'searchFilterArtistsBtn' and filter == True:
            self.ui.searchFilterAllBtn.setChecked(False)
            self.ui.searchFilterSongsBtn.setChecked(False)
        else:
            self.ui.searchFilterAllBtn.setChecked(True)
            self.ui.searchFilterSongsBtn.setChecked(False)
            self.ui.searchFilterArtistsBtn.setChecked(False)