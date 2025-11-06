from common import *

class ImageOptions(QWidget):
    model_selected = pyqtSignal(str)
    detect_clicked = pyqtSignal()
    archiver_clicked = pyqtSignal()


    def __init__(self, state_manager):
        super().__init__()
        layout = QVBoxLayout()

        self.state_manager = state_manager
        
        self.load_image = QPushButton("Load image")
        self.load_model = QPushButton("Load model")
        self.detect = QPushButton("Detect")
        self.archiver = QPushButton("Archiver")
    

        self.combo_model = QComboBox()
        self.combo_model.addItem("YOLOv8", "yolov8")
        self.combo_model.addItem("YOLOv11", "yolo11")
        self.combo_model.addItem("YOLOv12", "yolo12")
        self.combo_model.setCurrentIndex(0)

        self.combo_model_size = QComboBox()
        self.combo_model_size.addItem("Nano", "n")
        self.combo_model_size.addItem("Small", "s")
        self.combo_model_size.addItem("Medium", "m")
        self.combo_model_size.addItem("Large", "l")
        self.combo_model_size.addItem("Extra large", "x")
        self.combo_model_size.setCurrentIndex(0)

        self.combo_model_task = QComboBox()
        self.combo_model_task.addItem("Detection", "normal")
        self.combo_model_task.addItem("Classification", "cls")
        self.combo_model_task.addItem("Instance segmentation", "seg")
        self.combo_model_task.addItem("Oriented Detection", "obb")
        self.combo_model_task.addItem("Pose/Keypoints", "pose")
        self.combo_model_task.setCurrentIndex(0)


        

        layout.addWidget(self.load_image)
        layout.addWidget(self.combo_model)
        layout.addWidget(self.combo_model_size)
        layout.addWidget(self.combo_model_task)
        layout.addWidget(self.load_model)
        layout.addWidget(self.detect)
        layout.addWidget(self.archiver)

        self.setLayout(layout)
        
        self.load_image.clicked.connect(self.open_image)
        self.detect.clicked.connect(self.detect_clicked.emit)
        self.load_model.clicked.connect(self.emit_model_path)
        self.archiver.clicked.connect(self.archiver_clicked.emit)

    def emit_model_path(self):
        base_name = self.combo_model.currentData()
        size = self.combo_model_size.currentData()
        task = self.combo_model_task.currentData()
        model_path = base_name + size

        if(task == "normal"):
            self.state_manager.model_name = model_path + ".pt"
            
        else:
            model_path = model_path + "-" + task + ".pt"
            self.state_manager.model_name = model_path
            


    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image")
        if file_name:
            self.state_manager.image_path = file_name



