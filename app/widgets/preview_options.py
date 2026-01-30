from common import *

class PreviewOptions(QWidget):
    back_to_archiver = pyqtSignal()
    set_local_color = pyqtSignal(QColor)
    delete_selected_image = pyqtSignal()
    conf_val_changed = pyqtSignal(float)

    def __init__(self,state_manager):
        super().__init__()
        layout = QVBoxLayout()

        self.state_manager = state_manager

        self.archiver = QPushButton("Back to archiver page")
        self.set_color = QPushButton("Choose bounding box color for this image")
        self.delete_image = QPushButton("Delete this image")

        self.archiver.clicked.connect(self.back_to_archiver.emit)
        self.set_color.clicked.connect(self.get_color)
        self.delete_image.clicked.connect(self.delete_image_popup)

        self.conf_label = QLabel(f"Confidence: 0% - Won't draw boxes below score")
        self.conf_slider = QSlider(Qt.Orientation.Horizontal)
        self.conf_slider.setMinimum(0)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(0)
        self.conf_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.conf_slider.setTickInterval(10)
        self.conf_slider.valueChanged.connect(self.update_conf)
        

        self.delete_image.setStyleSheet("""
            QPushButton {
                background-color: #eb1c2a;
                color: white;
                                        }
                                        
            QPushButton:hover {
                background-color: #f03737;
                                        }
                
                                        """)
        
        layout.addStretch()
        layout.addWidget(self.archiver)
        layout.addStretch()
        layout.addWidget(self.set_color)
        layout.addStretch()
        layout.addWidget(self.delete_image)
        layout.addStretch()
        layout.addWidget(self.conf_label)
        layout.addWidget(self.conf_slider)
        layout.addStretch()

        

        self.setLayout(layout)

    def update_conf(self, value):
        self.state_manager.conf_bboxes = value / 100.0
        self.conf_label.setText(f"Confidence: {value}% - Won't draw boxes below score")




    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_local_color.emit(color)

    def delete_image_popup(self):
        popup = QMessageBox.question(self, "Delete this image?", "Deleting is permanent!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if popup == QMessageBox.StandardButton.Yes:
            self.delete_selected_image.emit()



        

        