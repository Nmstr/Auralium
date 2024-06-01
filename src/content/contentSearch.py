from content.search.searchEngine.searchEngine import SearchEngine

from content.search.songResult import SearchSongResultWidget
from content.search.topResult import SearchTopResultWidget

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentSearch, BaseClass = uic.loadUiType('content/contentSearch.ui')

class ContentSearchWidget(BaseClass, UiContentSearch):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler
        
        self.searchEngine = SearchEngine(self.sqlHandler)
        self.searchEngine.createIndex()
        self.searchEngine.addToIndex()

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

        similar = searchResults[:3]
        similarSongs = searchResults

        self.displaySearchResultsTop(similar)
        self.displaySearchResultsSongs(similarSongs)

    def switchSearchFilter(self, filter: bool) -> None:
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
        for song in similar:
            searchTopResultWidget = SearchTopResultWidget(self.mainWindow, song)
            layout.addWidget(searchTopResultWidget)

    def displaySearchResultsSongs(self, similarSongs: list) -> None:
        """
        Dynamically add custom widgets for each song in the search results.
        This adds to the general search results

        Parameters:
            similarSongs (list): The list of songs to display in the search results.
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
        for song in similarSongs:
            searchSongResultWidget = SearchSongResultWidget(self.mainWindow, song)
            layout.addWidget(searchSongResultWidget)
