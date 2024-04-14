import musicPlayerSqlHandler as sqlHandler

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
import difflib
import sys
import os

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        self.ui.homeBtn.clicked.connect(self.goHome)
        self.ui.searchBtn.clicked.connect(self.goSearch)

        self.ui.searchBar.textChanged.connect(self.searchBarTextChange)
        self.ui.searchFilterAllBtn.clicked.connect(self.switchSearchFilter)
        self.ui.searchFilterSongsBtn.clicked.connect(self.switchSearchFilter)
        self.ui.searchFilterArtistsBtn.clicked.connect(self.switchSearchFilter)

        self.show()
    
    def searchBarTextChange(self, text):
        """
        This function handles the search functionality based on the search bar text.
        """
        print(text)
        allSongs = sqlHandler.retrieveAllSongTitles()
        print(allSongs)
        simmilar = difflib.get_close_matches(text, allSongs, n=3, cutoff=0.05)
        print(simmilar)
        if len(simmilar) < 3:
            simmilar.append('')
            simmilar.append('')
            simmilar.append('')

        self.ui.searchTopResult0Name.setText(simmilar[0])
        self.ui.searchTopResult1Name.setText(simmilar[1])
        self.ui.searchTopResult2Name.setText(simmilar[2])

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
    
    def goHome(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.home)

    def goSearch(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.search)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec())