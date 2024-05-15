from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSearchSongResult, BaseClass = uic.loadUiType('content/search/songResult.ui')

class SearchSongResultWidget(BaseClass, UiSearchSongResult):
    def __init__(self, mainWindow, song):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Set song info
        self.nameLabel.setText(song[1])
        self.artistLabel.setText(song[2])
        self.mainWindow.setSongImage(song[1], self.coverImg, [150, 150])

        # Connect control buttons
        self.playBtn.clicked.connect(lambda: self.mainWindow.songQueue.addAndSetCurrentSong(song[3]))
        self.addToQueueBtn.clicked.connect(lambda: self.mainWindow.songQueue.addSong(song[3]))
