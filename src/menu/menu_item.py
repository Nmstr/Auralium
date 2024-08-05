from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QFile 

class MenuItem(QFrame):
    def __init__(self, parent=None, *, app_data: str, widget: QFrame) -> None:
        self._parent = parent
        self._widget = widget
        super().__init__(parent)
        loader = QUiLoader()
        ui_file = QFile("src/menu/menu_item.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the label
        self.ui.app_name_label.setText(app_data["name"])

    def mousePressEvent(self, event):  # noqa: N802
        self._parent.ui.page.setCurrentWidget(self._widget)
