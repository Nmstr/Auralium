from PyQt6 import uic

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor


# Load the .ui file and get the base class and form class
UiSidebar, BaseClass = uic.loadUiType('bars/sidebar/sidebar.ui')

class SidebarWidget(BaseClass, UiSidebar):
    def __init__(self, mainWindow, sqlHandler):
        self.mainWindow = mainWindow
        self.sqlHandler = sqlHandler
        self.resizeBar = False

        super().__init__()
        self.setupUi(self)

        self.playlistsCreateBtn.clicked.connect(lambda: self.sqlHandler.playlists.create('dadwdaddawkuuhku', None, None, None))
        self.playlistsCreateBtn.clicked.connect(lambda: self.mainWindow.displayPlaylists())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setCursorShape)
        self.timer.start(10)

    def setCursorShape(self) -> None:
        """
        Sets the cursor shape based on the position of the mouse.
        """
        global_pos = QCursor.pos()
        local_pos = self.mapFromGlobal(global_pos)
        if abs(local_pos.x() - self.width()) <= 25:
            self.resizeBar = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            self.resizeBar = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
    def mouseMoveEvent(self, event) -> None:
        """
        Handles the mouse move event.

        Resizes the sidebar, if self.resizeBar is True.
        """
        super().mouseMoveEvent(event)
        if self.resizeBar:
            self.mainWindow.ui.sidebarContainer.setFixedWidth(event.pos().x() + 20)
