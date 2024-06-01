from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentHome, BaseClass = uic.loadUiType('content/contentHome.ui')

class ContentHomeWidget(BaseClass, UiContentHome):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler

        super().__init__()
        self.setupUi(self)

        # Connect playlist buttons
        self.playlistsRetrieveBtn.clicked.connect(lambda: print(self.sqlHandler.playlists.retrieve(1)))
        self.playlistsRetrieveAllBtn.clicked.connect(lambda: print(self.sqlHandler.playlists.retrieveAll()))
        self.playlistsAddSongBtn.clicked.connect(lambda: self.sqlHandler.playlists.addSong(1, 500, 999999))
        self.playlistsRemoveSongBtn.clicked.connect(lambda: self.sqlHandler.playlists.removeSong(1, 3))
        self.playlistsMoveSongBtn.clicked.connect(lambda: self.sqlHandler.playlists.moveSong(1, 3, 1))
