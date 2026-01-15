from common import *

class PreviewOptions(QWidget):
    back_to_archiver = pyqtSignal()
    set_local_color = pyqtSignal(QColor)
    delete_selected_image = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.archiver = QPushButton("Back to archiver page")
        self.set_color = QPushButton("Set bbox color")
        self.delete_image = QPushButton("Delete this image")

        self.archiver.clicked.connect(self.back_to_archiver.emit)
        self.set_color.clicked.connect(self.get_color)
        self.delete_image.clicked.connect(self.delete_image_popup)

        self.delete_image.setStyleSheet("""
            QPushButton {
                background-color: #eb1c2a;
                color: white;
                                        }
                                        
            QPushButton:hover {
                background-color: #f03737;
                                        }
                
                                        """)

        layout.addWidget(self.archiver)
        layout.addWidget(self.set_color)
        layout.addWidget(self.delete_image)

        

        self.setLayout(layout)

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_local_color.emit(color)

    def delete_image_popup(self):
        popup = QMessageBox.question(self, "Delete this image?", "Deleting is permanent!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if popup == QMessageBox.StandardButton.Yes:
            self.delete_selected_image.emit()



        

        