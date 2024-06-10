from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

class LastButton(QGraphicsView):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()

        # Set properties
        self.setFixedSize(48, 48)
        self.setStyleSheet("background: transparent;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
        self.setIcon(icon='media-skip-backward')

    def setIcon(self, *, icon) -> None:
        """
        Set the icon of the button.
        """
        # Set the img
        graphicsScene = QGraphicsScene()
        icon = QIcon.fromTheme(icon)
        pixmap = icon.pixmap(QSize(48, 48))
        graphicsScene.addPixmap(pixmap)
        self.setScene(graphicsScene)

    def mousePressEvent(self, event) -> None:
        """
        Handle the mouse press event.

        This function is called when a mouse button is pressed. It checks if the left mouse button was pressed and if so, executes the function.

        Parameters:
            event (QMouseEvent): The mouse event that triggered the function.

        Returns:
            None
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.mainWindow.songQueue.goToPreviousSong()
            self.mainWindow.bottomBar.timeSlider.positionEstimate = 0
        return super().mousePressEvent(event)
