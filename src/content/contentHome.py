from sqlHandler import sqlHandler

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentHome, BaseClass = uic.loadUiType('content/contentHome.ui')

class ContentHomeWidget(BaseClass, UiContentHome):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Connect playlist buttons
        self.playlistsRetrieveBtn.clicked.connect(lambda: print(sqlHandler.playlists.retrieve(1)))
        self.playlistsRetrieveAllBtn.clicked.connect(lambda: print(sqlHandler.playlists.retrieveAll()))
        self.playlistsAddSongBtn.clicked.connect(lambda: sqlHandler.playlists.addSong(1, 500, 999999))
        self.playlistsRemoveSongBtn.clicked.connect(lambda: sqlHandler.playlists.removeSong(1, 3))
        self.playlistsMoveSongBtn.clicked.connect(lambda: sqlHandler.playlists.moveSong(1, 3, 1))
        self.settingsBtn.clicked.connect(lambda: self.mainWindow.setMainContentDisplay('settings'))
