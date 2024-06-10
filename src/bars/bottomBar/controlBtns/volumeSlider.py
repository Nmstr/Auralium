from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt, QTimer

class VolumeSlider(QSlider):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__(Qt.Orientation.Horizontal)

        self.setRange(0, 100)

        config = self.mainWindow.preferenceHandler.readConfig()
        self.setValue(config.getint('SETTINGS', 'volume'))
        self.mainWindow.songQueue.setVolume(config.getint('SETTINGS', 'volume'))

    def mousePressEvent(self, event) -> None:
        """
        Handle the mouse release event.

        This function is called when a mouse button is released. It checks if the left mouse button was released and if so, executes the function.

        Parameters:
            event (QMouseEvent): The mouse event that triggered the function.

        Returns:
            None
        """
        newVolume = int(event.pos().x() / self.width() * 100)
        self.setSliderPosition(int(newVolume))
        self.mainWindow.songQueue.setVolume(int(newVolume))
        self.mainWindow.preferenceHandler.writeConfig(section = 'SETTINGS', option = 'volume', value = str(self.value()))
        return super().mousePressEvent(event)
