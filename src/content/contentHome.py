from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiContentHome, BaseClass = uic.loadUiType('content/contentHome.ui')

class ContentHomeWidget(BaseClass, UiContentHome):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)
