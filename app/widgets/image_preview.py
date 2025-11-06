from common import *

class ImagePreview(QWidget):
    def __init__(self,state_manager):
        super().__init__()
        self.state_manager = state_manager
        self.label = QLabel()
        self.pixmap = QPixmap()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.label.setPixmap(self.pixmap)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.state_manager.image_path_changed.connect(self.set_image)

        

    def resizeEvent(self,event):
        if self.label.pixmap():
            modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            self.label.setPixmap(modified_pixmap)
        super().resizeEvent(event)

    def set_image(self,path):
        self.pixmap = QPixmap(path)
        modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        self.label.setPixmap(modified_pixmap)

    def draw_bounding_boxes(self,results):
        boxes,scores,classes = results
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(2)
        for i in range(len(boxes)):
            x1,y1,x2,y2 = boxes[i]
            cls = classes[i]
            score = scores[i]
            rect = QRect(int(x1),int(y1),int(x2),int(y2))
            painter.drawRect(rect)
            painter.drawText(int(x1),int(y1)+20, f"{self.state_manager.class_names[int(cls)]}: {score}")
        modified_pixmap = self.pixmap.scaled(
                    self.label.width(),
                    self.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
        self.label.setPixmap(modified_pixmap)


        
    


    




