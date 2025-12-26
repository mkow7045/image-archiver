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
        self.delete_image.clicked.connect(lambda: self.delete_selected_image.emit())

        layout.addWidget(self.archiver)
        layout.addWidget(self.set_color)
        layout.addWidget(self.delete_image)

        self.setLayout(layout)

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_local_color.emit(color)

        