from common import *

class PreviewOptions(QWidget):
    back_to_archiver = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.archiver = QPushButton("Back to archiver page")

        self.archiver.clicked.connect(self.back_to_archiver.emit)

        layout.addWidget(self.archiver)

        self.setLayout(layout)

        