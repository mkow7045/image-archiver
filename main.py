from ultralytics import YOLO
from detectors import *
from app import MainWindow
import sys
from PyQt6.QtWidgets import QApplication
from state_manager import StateManager
from database_manager import DatabaseManager
import qdarkstyle


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    screen = QApplication.primaryScreen().availableGeometry()

    state_manager = StateManager()
    database_manager = DatabaseManager(state_manager)

    state_manager.theme_changed.connect(lambda theme: change_theme(app,theme))

    window = MainWindow(screen.width(),screen.height(),state_manager, database_manager)
    window.show()
    app.exec()


def change_theme(app,theme):
    if theme == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    if theme == "light":
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=qdarkstyle.LightPalette))


    
        
    

if __name__ == "__main__":
    main()