from content.search.searchEngine.searchEngine import SearchEngine

from content.search.topResultArtist import SearchTopResultArtistWidget
from content.search.topResultSong import SearchTopResultSongWidget
from content.search.artistResult import SearchArtistResultWidget
from content.search.songResult import SearchSongResultWidget

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentSearch, BaseClass = uic.loadUiType('content/contentSearch.ui')

class ContentSearchWidget(BaseClass, UiContentSearch):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.searchFilter = 'all'
        
        self.searchEngine = SearchEngine(self.mainWindow)
        self.searchEngine.createIndex()

        super().__init__()
        self.setupUi(self)

        # Connect buttons/text fields for search
        self.searchBarTextChange('') # Trigger searchBarTextChange once on startup
        self.searchBar.textChanged.connect(self.searchBarTextChange)
        self.searchFilterAllBtn.clicked.connect(self.switchSearchFilter)
        self.searchFilterSongsBtn.clicked.connect(self.switchSearchFilter)
        self.searchFilterArtistsBtn.clicked.connect(self.switchSearchFilter)

    def searchBarTextChange(self, text: str) -> None:
        """
        This function handles the search functionality based on the search bar text.
        It uses woosh to search for the text in the index and displays the results.
        
        Parameters:
            text (str): The text entered in the search bar.
        """
        searchResults = self.searchEngine.search(text)

        if self.searchFilter == 'all':
            similar = searchResults[:3]
        elif self.searchFilter == 'songs':
            similar = [item for item in searchResults if item['itemType'] == 'song'][:3]
        elif self.searchFilter == 'artists':
            similar = [item for item in searchResults if item['itemType'] == 'artist'][:3]
        self.displaySearchResultsTop(similar)
        self.displaySearchResultsSongs(searchResults)
        self.displaySearchResultsArtists(searchResults)

    def switchSearchFilter(self, filter: bool) -> None:
        """
        This function handles the switching of search filters based on the senderName and the filter value.
        """
        senderName = self.sender().objectName()

        if senderName == 'searchFilterAllBtn' and filter == True:
            self.searchFilterSongsBtn.setChecked(False)
            self.searchFilterArtistsBtn.setChecked(False)
            self.searchFilter = 'all'
        elif senderName == 'searchFilterSongsBtn' and filter == True:
            self.searchFilterAllBtn.setChecked(False)
            self.searchFilterArtistsBtn.setChecked(False)
            self.searchFilter = 'songs'
        elif senderName == 'searchFilterArtistsBtn' and filter == True:
            self.searchFilterAllBtn.setChecked(False)
            self.searchFilterSongsBtn.setChecked(False)
            self.searchFilter = 'artists'
        else:
            self.searchFilterAllBtn.setChecked(True)
            self.searchFilterSongsBtn.setChecked(False)
            self.searchFilterArtistsBtn.setChecked(False)
            self.searchFilter = 'all'

        self.searchBarTextChange(self.searchBar.text())

    def displaySearchResultsTop(self, similar: list) -> None:
        """
        Dynamically add custom widgets for each song in the search results.
        This adds to the top search results

        Parameters:
            similar (list): The list of songs to display in the search results.
        """
        container = self.searchTopResults
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
        for item in similar:
            if item['itemType'] == 'song':
                searchTopResultWidget = SearchTopResultSongWidget(self.mainWindow, song=item)
                layout.addWidget(searchTopResultWidget)
            elif item['itemType'] == 'artist':
                searchTopResultWidget = SearchTopResultArtistWidget(self.mainWindow, artist=item)
                layout.addWidget(searchTopResultWidget)

    def displaySearchResultsSongs(self, similarResults: list) -> None:
        """
        Dynamically add custom widgets for each song in the search results.
        This adds to the general search results

        Parameters:
            similarResults (list): The list of results to display in the search results.
        """
        container = self.searchSongsArea
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
        for item in similarResults:
            if item['itemType'] == 'song':
                searchSongResultWidget = SearchSongResultWidget(self.mainWindow, item)
                layout.addWidget(searchSongResultWidget)

    def displaySearchResultsArtists(self, similarResults: list) -> None:
        """
        Dynamically add custom widgets for each song in the search results.
        This adds to the general search results

        Parameters:
            similarResults (list): The list of results to display in the search results.
        """
        container = self.searchArtistsArea
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
        for item in similarResults:
            if item['itemType'] == 'artist':
                searchSongResultWidget = SearchArtistResultWidget(self.mainWindow, item)
                layout.addWidget(searchSongResultWidget)
