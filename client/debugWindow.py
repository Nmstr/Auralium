from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('debug.ui', self)

        self.ui.debugIndexSongs.clicked.connect(self.indexSongs)

        self.show()
    
    def indexSongs(self):
        print('Test')
