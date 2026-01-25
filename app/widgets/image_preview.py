from common import *
from PIL import Image
from PIL.ExifTags import TAGS

class ImagePreview(QWidget):
    def __init__(self,state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.label = QLabel()
        self.pixmap = QPixmap()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.label.setPixmap(self.pixmap)
        self.color = self.state_manager.color
        self.current_results = []
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.state_manager.image_path_changed.connect(self.set_image)
        self.state_manager.conf_bboxes_changed.connect(self.conf_bboxes_changed)

    def load_image_exif(self,image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return pixmap

        pil_image = Image.open(image_path)
        if pil_image is None:
            return pixmap
        
        if not hasattr(pil_image, 'getexif'):
            return pixmap
        
        exif = pil_image.getexif()
        if exif is None:
            return pixmap
        
        orientation_value = exif.get(274, None)
        if orientation_value is None:
            return pixmap
        

        if orientation_value == 3:
            pil_image = pil_image.rotate(180, expand=True)
        elif orientation_value == 6:
            pil_image = pil_image.rotate(270, expand=True)
        elif orientation_value == 8:
            pil_image = pil_image.rotate(90, expand=True)
        else:
            return pixmap
        
        pil_image = pil_image.convert("RGB")
        data = pil_image.tobytes("raw", "RGB")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def conf_bboxes_changed(self):
        if self.current_results:
            self.draw_bounding_boxes(self.current_results)
        

    def resizeEvent(self,event):
        if self.label.pixmap():
            modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            self.label.setPixmap(modified_pixmap)
            self.draw_bounding_boxes(self.current_results)
        super().resizeEvent(event)

    def set_image(self,path):
        self.color = self.state_manager.color
        self.pixmap = self.load_image_exif(path)
        modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        self.label.setPixmap(modified_pixmap)

    def draw_bounding_boxes(self,results):
        self.current_results = results
        
        modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        
        scale_x = modified_pixmap.width() / self.pixmap.width()
        scale_y = modified_pixmap.height() / self.pixmap.height()

        painter = QPainter(modified_pixmap)
        pen = QPen(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        for result in results:
            if self.state_manager.draw_only_selected == False:
                boxes,scores,classes = result
                for i in range(len(boxes)):
                    if scores[i] < self.state_manager.conf_bboxes:
                        continue
                    x1,y1,x2,y2 = boxes[i]
                    cls = classes[i]
                    score = scores[i]
                    x1 *= scale_x
                    x2 *= scale_x
                    y1 *= scale_y
                    y2 *= scale_y
                    rect = QRect(int(x1),int(y1),int(x2),int(y2))
                    painter.drawRect(rect)
                    painter.drawText(int(x1),int(y1)+20, f"{cls}: {score}")

            if self.state_manager.draw_only_selected == True:
                boxes,scores,classes = result
                for i in range(len(boxes)):
                    if scores[i] < self.state_manager.conf_bboxes:
                        continue
                    x1,y1,x2,y2 = boxes[i]
                    cls = classes[i]
                    score = scores[i]
                    x1 *= scale_x
                    x2 *= scale_x
                    y1 *= scale_y
                    y2 *= scale_y
                    if cls in self.state_manager.filter_yes:
                        rect = QRect(int(x1),int(y1),int(x2),int(y2))
                        painter.drawRect(rect)
                        painter.drawText(int(x1),int(y1)+20, f"{cls}: {score}")


        painter.end()
        self.label.setPixmap(modified_pixmap)

    


        
    


    




