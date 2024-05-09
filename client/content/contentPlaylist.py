from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentPlaylist, BaseClass = uic.loadUiType('content/contentPlaylist.ui')

class ContentPlaylistWidget(BaseClass, UiContentPlaylist):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)
