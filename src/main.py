from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from audio_player import AudioPlayer
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auralium")

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/main.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setGeometry(self.ui.geometry())

        from loadutils import load_apps
        load_apps(self)

        # Create the player
        self.player = AudioPlayer("mysound.wav")
        self.player.volume = 0.05

        # Connect buttons
        self.ui.play_btn.clicked.connect(self.play)
        self.ui.stop_btn.clicked.connect(self.stop)
    
    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
