from common import *

class ClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self,image_id):
        super().__init__()
        self.image_id = image_id

    def mousePressEvent(self, ev):
        self.clicked.emit(self.image_id)
        return super().mousePressEvent(ev)

class Gallery(QWidget):
    thumb_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
    

        self.thumbnails = QWidget()
        self.thumbnails_layout = QGridLayout()
        self.thumbnails.setLayout(self.thumbnails_layout)

        self.scroll_area.setWidget(self.thumbnails)

        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

    def update_images(self,image_list):
        while self.thumbnails_layout.count():
            item = self.thumbnails_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        row = 0
        col = 0
        max_col = 4
        for image in image_list:
            label = ClickableLabel(image)
            pixmap = QPixmap(image)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            label.setPixmap(pixmap)
            label.clicked.connect(self.thumb_clicked)
            thumb_size = 150
            scaled_pixmap = pixmap.scaled(
                    thumb_size,
                    thumb_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            label.setPixmap(scaled_pixmap)
            if(col >= max_col):
                row += 1
                col = 0
            self.thumbnails_layout.addWidget(label,row,col)
            col += 1
