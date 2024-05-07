from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiNowPlayingQueue, BaseClass = uic.loadUiType('queuePopover/queueEntry.ui')

class QueueEntryWidget(BaseClass, UiNowPlayingQueue):
    def __init__(self, song):
        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(song[1])
