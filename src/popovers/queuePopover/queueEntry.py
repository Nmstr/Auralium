from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiNowPlayingQueue, BaseClass = uic.loadUiType('popovers/queuePopover/queueEntry.ui')

class QueueEntryWidget(BaseClass, UiNowPlayingQueue):
    def __init__(self, song, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(song[1])

        self.mainWindow.songDataHandler.setSongImage(song[1], self.coverImg, [100, 100])