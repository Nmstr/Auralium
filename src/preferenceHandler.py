from PyQt6.QtGui import QFont
import configparser
import shutil
import os

configPath = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/auralium/config.ini'

class PreferenceHandler():
    def __init__(self, QApplication, app) -> None:
        self.QApplication = QApplication
        self.app = app
        self.createAllPreferences()

        self.config = self.readConfig()
        self.loadStyleSheet()
        self.loadFont()

    def createAllPreferences(self) -> None:
        """
        Creates a template config file if none exists and a default stylesheet if none exists.
        """
        # Copy template config if none exists
        if not os.path.exists(configPath):
            os.makedirs(os.path.dirname(configPath), exist_ok=True)
            shutil.copy('assets/templateConfig.ini', configPath)

        # Create stylesheet if none exists
        stylesheetPath = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/auralium/style.qss'
        if not os.path.exists(stylesheetPath):
            shutil.copy('assets/style.qss', stylesheetPath)

    def readConfig(self) -> configparser.ConfigParser:
        """
        Reads the configuration file and returns a ConfigParser object.

        This function ensures that the configuration file exists by copying a template file if it does not. It then reads the configuration file specified by `configPath` using the `configparser.ConfigParser` module and returns the resulting `ConfigParser` object.

        Returns:
            configparser.ConfigParser: A ConfigParser object representing the configuration file.
        """
        # Read the config file
        config = configparser.ConfigParser()
        config.read(configPath)
        return config
    
    def writeConfig(self, *, section: str, option: str, value: str, reload: bool = True) -> None:
        """
        Write a value to the configuration file.

        Args:
            section (str): The section of the configuration file.
            option (str): The option within the section.
            value (str): The value to be written.
        """
        # Write the value
        self.config.set(section, option, value)
        with open(configPath, 'w') as configfile:
            self.config.write(configfile)
        
        if reload: # Reload the config
            self.readConfig()

    def loadStyleSheet(self) -> None:
        """
        Loads the style sheet from the specified file path and sets it as the style sheet for the application.

        This function reads the style sheet file located at the path specified by the environment variable `XDG_CONFIG_HOME` if it exists, otherwise it uses the default path `~/.config/auralium/style.qss`. It then opens the file and reads its contents, and finally sets the read contents as the style sheet for the application using the `setStyleSheet` method.
        """
        stylesheetPath = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/auralium/style.qss'
        with open(stylesheetPath, 'r') as f:
            self.app.setStyleSheet(f.read())

    def loadFont(self) -> None:
        """
        Sets the font for the QApplication based on the value specified in the configuration file.

        This function reads the value of the 'font' key from the 'APPEARANCE' section of the configuration file. If the value is not 'default', it creates a QFont object with the specified font and sets it as the font for the QApplication object.
        
        Parameters:
            QApplication (QApplication): The QApplication object to set the font for.
        """
        # Set the font
        setFont = self.config.get('APPEARANCE', 'font', fallback='default')
        if setFont != 'default':
            font = QFont(setFont)
            self.QApplication.setFont(font)
