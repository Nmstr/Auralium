from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt, QTimer

class TimeSlider(QSlider):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.positionEstimate = 0
        self.timerTickingRate = 100
        self.pressed = False

        super().__init__(Qt.Orientation.Horizontal)

        self.setRange(0, 1000)

        # Create a QTimer to update the time slider automatically every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimeSlider)
        self.timer.start(self.timerTickingRate)

    def updateTimeSlider(self) -> None:
        """
        Update the time slider position.

        This function is called every second to update the time slider position.

        Returns:
            None
        """
        self.positionEstimate += self.timerTickingRate
        try:
            if not self.pressed:
                self.setSliderPosition(int(self.positionEstimate / self.mainWindow.songQueue.getDuration()))

            if int(self.positionEstimate / self.mainWindow.songQueue.getDuration()) >= 1000:
                self.positionEstimate = 0
                self.setSliderPosition(0)
                self.mainWindow.songQueue.goToNextSong()
        except ZeroDivisionError:
            pass

    def mousePressEvent(self, event) -> None:
        """
        Handle the mouse press event.

        This function is called when a mouse button is pressed. It checks if the left mouse button was pressed and if so, executes the function.

        Parameters:
            event (QMouseEvent): The mouse event that triggered the function.

        Returns:
            None
        """
        self.pressed = True
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """
        Handle the mouse release event.

        This function is called when a mouse button is released. It checks if the left mouse button was released and if so, executes the function.

        Parameters:
            event (QMouseEvent): The mouse event that triggered the function.

        Returns:
            None
        """
        eventPositon = event.pos().x()
        self.setSliderPosition(int(eventPositon / self.width() * 1000))
        newTime = int(eventPositon / self.width() * self.mainWindow.songQueue.getDuration())
        self.mainWindow.songQueue.setTime(newTime)
        self.positionEstimate = newTime * 1000
        self.pressed = False
        return super().mouseReleaseEvent(event)
