from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentPlaylist, BaseClass = uic.loadUiType('content/contentPlaylist.ui')

class contentPlaylistWidget(BaseClass, UiContentPlaylist):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)
