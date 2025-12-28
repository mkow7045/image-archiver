from common import *

class GalleryThumb(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self,image_id):
        super().__init__()
        self.image_id = image_id

    def mousePressEvent(self, ev):
        self.clicked.emit(self.image_id)

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
            thumb = GalleryThumb(image)
            pixmap = QPixmap(image)
            thumb.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            thumb.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            thumb.setPixmap(pixmap)
            thumb.clicked.connect(self.thumb_clicked)
            thumb_size = 150
            scaled_pixmap = pixmap.scaled(
                    thumb_size,
                    thumb_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            thumb.setPixmap(scaled_pixmap)
            if(col >= max_col):
                row += 1
                col = 0
            self.thumbnails_layout.addWidget(thumb,row,col)
            col += 1
