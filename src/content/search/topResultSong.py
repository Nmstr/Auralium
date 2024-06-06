from popovers.contextPopover.contextPopover import ContextPopover

from PyQt6.QtCore import Qt, QPoint

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSearchTopResultSong, BaseClass = uic.loadUiType('content/search/topResultSong.ui')

class SearchTopResultSongWidget(BaseClass, UiSearchTopResultSong):
    def __init__(self, mainWindow, song):
        self.mainWindow = mainWindow
        self.song = song

        super().__init__()
        self.setupUi(self)

        # Set song info
        self.nameLabel.setText(self.song['data'][1])
        self.artistLabel.setText(self.song['data'][2])
        self.mainWindow.songDataHandler.setSongImage(self.song['data'][1], self.coverImg, [150, 150])

        # Connect control buttons
        self.playBtn.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(self.song['data'][3]))
        self.addToQueueBtn.clicked.connect(lambda: self.mainWindow.songQueue.addSong(self.song['data'][3]))

        # Grey out if disabled
        if self.song['data'][7] == 1:
            self.setEnabled(False)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            self.showContextPopover()
            return super().mousePressEvent(event)

    def enterEvent(self, event) -> None:
        self.setStyleSheet("background-color: #333;")
        return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.setStyleSheet("")
        return super().leaveEvent(event)
 
    def showContextPopover(self) -> None:
        """
        Show the context popover.
        """
        popover = ContextPopover(self.mainWindow, self.song)

        popoverPos = self.mapToGlobal(QPoint(0, 0))
        
        # Set the position and size of the popover
        popover.setGeometry(popoverPos.x(), popoverPos.y(), self.width(), self.height())
        popover.show()
