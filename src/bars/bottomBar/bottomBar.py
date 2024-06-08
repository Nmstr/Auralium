from popovers.queuePopover.queuePopover import QueuePopover

import songDataHandler

from PyQt6.QtCore import QTimer, QPoint
from PyQt6 import uic

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiBottomBar, BaseClass = uic.loadUiType('bars/bottomBar/bottomBar.ui')

class BottomBarWidget(BaseClass, UiBottomBar):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Connect buttons for music controls
        self.musicControlsNext.clicked.connect(self.mainWindow.songQueue.goToNextSong)
        self.musicControlsLast.clicked.connect(self.mainWindow.songQueue.goToPreviousSong)
        self.musicControlsPlay.clicked.connect(self.playMusic)
        self.musicControlsVolume.valueChanged.connect(self.mainWindow.songQueue.setVolume)
        self.musicControlsVolume.sliderReleased.connect(lambda: self.mainWindow.preferenceHandler.writeConfig(section = 'SETTINGS', option = 'volume', value = str(self.musicControlsVolume.value())))
        self.musicControlsTime.sliderReleased.connect(self.updateSliderPositionManual)
        self.showQueueBtn.clicked.connect(self.showQueuePopover)

        # Create a QTimer to update the time slider automatically every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimeSliderAuto)
        self.timer.start(1000)

        # Create value for song duration
        self.oldDuration = 0

        self.musicControlsVolume.setValue(int(self.mainWindow.preferenceHandler.config.get('SETTINGS', 'volume', fallback=10)))

    def playMusic(self) -> None:
        """
        Plays the current song in the queue.
        """
        if self.mainWindow.songQueue.playing:
            self.mainWindow.songQueue.pause()
        else:
            self.mainWindow.songQueue.play()

    def updateSliderPositionManual(self) -> None:
        """
        Updates the slider position manually based on the value of musicControlsTime.
        Changes the position in the song.
        """
        timeInSeconds = self.musicControlsTime.value()
        self.mainWindow.songQueue.setTime(timeInSeconds)

    def updateTimeSliderAuto(self) -> None:
        """
        Updates the time slider automatically based on the current song's duration.
        Adjusts the slider value and triggers actions based on song progress.
        """
        newValue = self.musicControlsTime.value()
        if self.mainWindow.songQueue.playing:
            newValue += 1
            self.musicControlsTime.setValue(newValue)

        try:
            newDuration = self.mainWindow.songDataHandler.getTag(self.mainWindow.songQueue.getCurrentSong()).duration
            if self.oldDuration != newDuration:
                self.musicControlsTime.setValue(0)
                self.musicControlsTime.setRange(0, int(newDuration))
            self.oldDuration = newDuration

            if newValue >= int(newDuration):
                self.musicControlsTime.setValue(0)
                self.mainWindow.songQueue.goToNextSong()
        except Exception:
            pass #print('No song loaded')

    def showQueuePopover(self) -> None:
        """
        Shows the queue popover.
        """
        popover = QueuePopover(self.mainWindow)

        buttonPos = self.showQueueBtn.mapToGlobal(QPoint(0, 0)) # Get the position of the butto
        
        # Calculate the size of the popover
        popoverSizeX = self.mainWindow.width() * 0.4
        popoverSizeY = self.mainWindow.height() * 0.8
        # Calculate the position of the popover
        popoverPosX = buttonPos.x() + self.showQueueBtn.width()/2 - popoverSizeX
        popoverPosY = buttonPos.y() + self.showQueueBtn.height()/2 - popoverSizeY
        
        # Set the position and size of the popover
        popover.setGeometry(int(popoverPosX), int(popoverPosY), int(popoverSizeX), int(popoverSizeY))
        popover.show()
