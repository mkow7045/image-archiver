from ultralytics import YOLO
from detectors import *
from app import MainWindow
import sys
from PyQt6.QtWidgets import QApplication
from state_manager import StateManager


def main():
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen().availableGeometry()

    state_manager = StateManager()

    window = MainWindow(screen.width(),screen.height(),state_manager)
    window.show()
    app.exec()


    
         

    

if __name__ == "__main__":
    main()