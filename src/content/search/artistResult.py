from popovers.contextPopover.contextPopover import ContextPopover

from PyQt6.QtCore import Qt, QPoint

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSearchArtistResult, BaseClass = uic.loadUiType('content/search/artistResult.ui')

class SearchArtistResultWidget(BaseClass, UiSearchArtistResult):
    def __init__(self, mainWindow, artist):
        self.mainWindow = mainWindow
        self.artist = artist

        super().__init__()
        self.setupUi(self)

        # Set artist info
        self.nameLabel.setText(self.artist['data'][1])
        self.mainWindow.songDataHandler.setSongImage(self.artist['data'][1], self.coverImg, [150, 150])

        # Grey out if disabled
        if self.artist['data'][3] == 1:
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
 