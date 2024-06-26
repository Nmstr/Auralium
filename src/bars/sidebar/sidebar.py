from popovers.createPlaylistPopover.createPlaylistPopover import CreatePlaylistPopover

from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QCursor

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSidebar, BaseClass = uic.loadUiType('bars/sidebar/sidebar.ui')

class SidebarWidget(BaseClass, UiSidebar):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.resizeBar = False

        super().__init__()
        self.setupUi(self)

        self.playlistsCreateBtn.clicked.connect(lambda: self.showCreatePlaylistPopover())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setCursorShape)
        self.timer.start(10)

    def showCreatePlaylistPopover(self) -> None:
        """
        Shows the create playlist popover.
        """
        popover = CreatePlaylistPopover(self.mainWindow)

        buttonPos = self.playlistsCreateBtn.mapToGlobal(QPoint(0, 0))
        
        # Calculate the position of the popover
        popoverPosX = buttonPos.x() + self.playlistsCreateBtn.width()/2
        popoverPosY = buttonPos.y() + self.playlistsCreateBtn.height()/2
        
        # Set the position and size of the popover
        popover.setGeometry(int(popoverPosX), int(popoverPosY), 300, 100)
        popover.show()

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
        if self.resizeBar:
            newPos = event.pos().x() + 20
            if newPos > 150 and newPos < self.mainWindow.width() * 0.6:
                self.mainWindow.ui.sidebarContainer.setFixedWidth(event.pos().x() + 20)
        return super().mouseMoveEvent(event)
