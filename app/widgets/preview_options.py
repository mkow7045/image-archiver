from common import *

class PreviewOptions(QWidget):
    back_to_archiver = pyqtSignal()
    set_local_color = pyqtSignal(QColor)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.archiver = QPushButton("Back to archiver page")
        self.set_color = QPushButton("Set bbox color")

        self.archiver.clicked.connect(self.back_to_archiver.emit)
        self.set_color.clicked.connect(self.get_color)

        layout.addWidget(self.archiver)
        layout.addWidget(self.set_color)

        self.setLayout(layout)

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_local_color.emit(color)
        