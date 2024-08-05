from PySide6.QtWidgets import QHBoxLayout
from menu.menu_item import MenuItem
import importlib
import json
import os

def load_apps(parent) -> None:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    apps = os.listdir(f"{current_dir}/builtin/apps")
    
    layout = QHBoxLayout(parent.ui.menu)
    layout.setContentsMargins(5, 5, 5, 5)

    for app in apps:
        try:
            with open(f"{current_dir}/builtin/apps/{app}/manifest.json") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            print(f"Failed to load app {app}")
            print(e)
        
        # Create the page
        module = importlib.import_module(data["module_name"])
        app_class = getattr(module, data["app_class_name"])
        widget = app_class(parent)

        # Add the page to the page widget stack
        parent.ui.page.addWidget(widget)

        # Create the menu item
        menu_item = MenuItem(parent, app_data=data, widget=widget)
        layout.addWidget(menu_item)
