from popovers.queuePopover.queuePopover import QueuePopover

from bars.bottomBar.controlBtns.volumeSlider import VolumeSlider
from bars.bottomBar.controlBtns.timeSlider import TimeSlider
from bars.bottomBar.controlBtns.playButton import PlayButton
from bars.bottomBar.controlBtns.nextButton import NextButton
from bars.bottomBar.controlBtns.lastButton import LastButton

from PyQt6.QtCore import QPoint

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiBottomBar, BaseClass = uic.loadUiType('bars/bottomBar/bottomBar.ui')

class BottomBarWidget(BaseClass, UiBottomBar):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        # Add buttons for playback control
        layout = self.controlBtnFrame.layout()
        self.lastBtn = LastButton(self.mainWindow)
        self.playBtn = PlayButton(self.mainWindow)
        self.nextBtn = NextButton(self.mainWindow)
        layout.addWidget(self.lastBtn)
        layout.addWidget(self.playBtn)
        layout.addWidget(self.nextBtn)

        layout = self.controlSliderFrame.layout()
        self.timeSlider = TimeSlider(self.mainWindow)
        layout.addWidget(self.timeSlider)

        layout = self.rightSideFrame.layout()
        self.volumeSider = VolumeSlider(self.mainWindow)
        layout.addWidget(self.volumeSider)

        self.showQueueBtn.clicked.connect(self.showQueuePopover)

    def showQueuePopover(self) -> None:
        """
        #Shows the queue popover.
        """
        popover = QueuePopover(self.mainWindow)

        buttonPos = self.showQueueBtn.mapToGlobal(QPoint(0, 0)) # Get the position of the button
        
        # Calculate the size of the popover
        popoverSizeX = self.mainWindow.width() * 0.4
        popoverSizeY = self.mainWindow.height() * 0.8
        # Calculate the position of the popover
        popoverPosX = buttonPos.x() + self.showQueueBtn.width()/2 - popoverSizeX
        popoverPosY = buttonPos.y() + self.showQueueBtn.height()/2 - popoverSizeY
        
        # Set the position and size of the popover
        popover.setGeometry(int(popoverPosX), int(popoverPosY), int(popoverSizeX), int(popoverSizeY))
        popover.show()
