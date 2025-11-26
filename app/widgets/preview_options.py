from common import *

class PreviewOptions(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.archiver  = QPushButton("Back to archiver page")

        layout.addWidget(self.archiver)

        self.setLayout(layout)

        