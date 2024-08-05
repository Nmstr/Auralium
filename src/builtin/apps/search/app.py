from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QFile
import os

class SearchApp(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        loader = QUiLoader()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        ui_file = QFile(f"{current_dir}/app.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
