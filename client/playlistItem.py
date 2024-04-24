from sqlHandler import sqlHandler

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6 import uic

# Load the .ui file and get the base class and form class
Ui_PlaylistItem, BaseClass = uic.loadUiType('playlistsEntry.ui')

class PlaylistItemWidget(BaseClass, Ui_PlaylistItem):
    def __init__(self, playlist):
        self.playlist = playlist # Assign playlist to self.playlist to make it accessible in other functions

        super().__init__()
        self.setupUi(self)

        self.nameLabel.setText(playlist[1])
        self.creatorLabel.setText(playlist[2])

        # Enable mouse tracking
        self.setMouseTracking(True)
    
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
            print("Frame clicked!")
            print(self.playlist)
    
    def enterEvent(self, event):
        """
        Handle the mouse enter event.

        Parameters:
            event (QEnterEvent): The enter event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("background-color: #333;")

    def leaveEvent(self, event):
        """
        Handle the mouse leave event.

        Parameters:
            event (QEvent): The leave event that triggered the function.

        Returns:
            None
        """
        self.setStyleSheet("")



    def displayPlaylists(self) -> None:
        """
        Display the playlists in the UI.

        This function retrieves all playlists from the database and dynamically adds custom widgets for each playlist in the UI.

        Parameters:
        - self: The instance of the class.

        Return:
        - None
        """
        # Retrieve all playlists from the database
        playlists = sqlHandler.playlists.retrieveAll()

        # Get the container widget
        container = self.ui.playlistsScrollAreaWidgetContents
        # Check if the container has a layout, if not, set a new QVBoxLayout
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout()
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())): 
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                layoutItem.widget().deleteLater()

        # Dynamically add custom widgets for each playlist
        for playlist in playlists:
            playlistWidget = PlaylistItemWidget(playlist)
            layout.addWidget(playlistWidget)