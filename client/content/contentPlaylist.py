from PyQt6 import uic

# Load the .ui file and get the base class and form class
Ui_PlaylistItem, BaseClass = uic.loadUiType('content/contentPlaylist.ui')

class contentPlaylistWidget(BaseClass, Ui_PlaylistItem):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Enable mouse tracking
        self.setMouseTracking(True)
