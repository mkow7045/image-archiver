from common import *

class ExportOptions(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Options")
        self.setModal(True)

        layout = QVBoxLayout()
        
