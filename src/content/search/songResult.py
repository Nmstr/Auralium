from contextPopover.contextPopover import ContextPopover

from PyQt6.QtCore import Qt, QPoint

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSearchSongResult, BaseClass = uic.loadUiType('content/search/songResult.ui')

class SearchSongResultWidget(BaseClass, UiSearchSongResult):
    def __init__(self, mainWindow, song):
        self.mainWindow = mainWindow
        self.song = song

        super().__init__()
        self.setupUi(self)

        # Set song info
        self.nameLabel.setText(self.song[1])
        self.artistLabel.setText(self.song[2])
        self.mainWindow.setSongImage(self.song[1], self.coverImg, [150, 150])

        # Connect control buttons
        self.playBtn.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(self.song[3]))
        self.addToQueueBtn.clicked.connect(lambda: self.mainWindow.songQueue.addSong(self.song[3]))

        # Grey out if disabled
        if self.song[7] == 1:
            self.setEnabled(False)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            self.showContextPopover()

    def enterEvent(self, event) -> None:
        self.setStyleSheet("background-color: #333;")

    def leaveEvent(self, event) -> None:
        self.setStyleSheet("")
 
    def showContextPopover(self) -> None:
        """
        Show the context popover.
        """
        popover = ContextPopover(self.mainWindow, self.song, self.mainWindow.sqlHandler)

        buttonPos = self.mapToGlobal(QPoint(0, 0)) # Get the position of the butto
        
        # Set the position and size of the popover
        popover.setGeometry(buttonPos.x(), buttonPos.y(), self.width(), self.height())
        popover.show()
