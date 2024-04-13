from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import uic
import sys

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)

        self.ui.homeBtn.clicked.connect(self.goHome)
        self.ui.searchBtn.clicked.connect(self.goSearch)

        self.show()
    
    def goHome(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.home)

    def goSearch(self):
        self.ui.mainContentStack.setCurrentWidget(self.ui.search)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec())