from sqlHandler import sqlHandler

from PyQt6 import uic

# Load the .ui file and get the base class and form class
UiSettings, BaseClass = uic.loadUiType('settings/settings.ui')

class SettingsWidget(BaseClass, UiSettings):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        super().__init__()
        self.setupUi(self)

        self.fontApplyBtn.clicked.connect(self.applyFont)
    
    def applyFont(self):
        newFont = self.fontInput.text()
        self.mainWindow.preferenceHandler.writeConfig(section = 'APPEARANCE', option = 'font', value = newFont)
        self.mainWindow.preferenceHandler.loadFont()