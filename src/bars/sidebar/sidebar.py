from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSidebar, BaseClass = uic.loadUiType('bars/sidebar/sidebar.ui')

class SidebarWidget(BaseClass, UiSidebar):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler

        super().__init__()
        self.setupUi(self)

        self.playlistsCreateBtn.clicked.connect(lambda: self.sqlHandler.playlists.create('dadwdaddawkuuhku', None, None, None))
        self.playlistsCreateBtn.clicked.connect(lambda: self.mainWindow.displayPlaylists())