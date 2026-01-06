from common import *
from math import ceil

class GalleryThumb(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self,image_id):
        super().__init__()
        self.image_id = image_id

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.image_id)
        else:
            ev.ignore()

class Gallery(QWidget):
    thumb_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.thumb_size = 150
        

        self.image_cache = {}
    

        self.thumbnails = QWidget()
        self.thumbnails_layout = QGridLayout()
        self.thumbnails.setLayout(self.thumbnails_layout)

        self.scroll_area.setWidget(self.thumbnails)

        self.layout.addWidget(self.scroll_area)
        self.image_list = []

        self.setLayout(self.layout)

    def update_images(self,image_list):
        self.image_list = image_list
        while self.thumbnails_layout.count():
            item = self.thumbnails_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        row = 0
        col = 0
        max_col = 3
        for image in image_list:
            thumb = GalleryThumb(image)
            if image not in self.image_cache:
                self.image_cache[image] = QPixmap(image)
            pixmap = self.image_cache[image]
            thumb.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            thumb.setFixedSize(self.thumb_size, self.thumb_size)
            thumb.setPixmap(pixmap)
            thumb.clicked.connect(self.thumb_clicked)
            thumb_size = self.thumb_size
            scaled_pixmap = pixmap.scaled(
                    thumb_size,
                    thumb_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            thumb.setPixmap(scaled_pixmap)
            self.thumbnails_layout.addWidget(thumb,row,col)
            col += 1
            if(col >= max_col):
                row += 1
                col = 0
            rows = ceil(len(self.image_list) / max_col)
            spacing = self.thumbnails_layout.verticalSpacing()
            total_height = rows * (self.thumb_size + spacing)

            self.thumbnails.setMinimumHeight(total_height)

            

    def resizeEvent(self, event):
        self.thumb_size = max(150, int(self.width() / 4))

        for i in range(self.thumbnails_layout.count()):
            item = self.thumbnails_layout.itemAt(i)
            thumb = item.widget()
            if thumb:
                thumb.setFixedSize(self.thumb_size, self.thumb_size)
                pixmap = self.image_cache[thumb.image_id].scaled(
                    self.thumb_size,
                    self.thumb_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                thumb.setPixmap(pixmap)

        max_col = 3
        rows = ceil(len(self.image_list) / max_col)
        spacing = self.thumbnails_layout.verticalSpacing()
        total_height = rows * (self.thumb_size + spacing)

        self.thumbnails.setMinimumHeight(total_height)

        super().resizeEvent(event)
