from common import *
import os
import shutil
import hashlib

class ArchiverOptions(QWidget):
    image_selected = pyqtSignal(str) 
    model_selected = pyqtSignal(str)
    preview_clicked = pyqtSignal()


    def __init__(self, state_manager, detector,database_manager):
        super().__init__()
        layout = QVBoxLayout()

        self.state_manager = state_manager
        self.database_manager = database_manager
        self.detector = detector
        self.current_folder = ""
        
        self.load_folder = QPushButton("Load folder")
        self.load_model = QPushButton("Load model")
        self.start_processing = QPushButton("Start processing")
        self.preview = QPushButton("Back to preview")
    

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


        

        layout.addWidget(self.load_folder)
        layout.addWidget(self.combo_model)
        layout.addWidget(self.combo_model_size)
        layout.addWidget(self.combo_model_task)
        layout.addWidget(self.load_model)
        layout.addWidget(self.start_processing)
        layout.addWidget(self.preview)

        self.setLayout(layout)
        
        self.load_folder.clicked.connect(self.select_folder)
        self.load_model.clicked.connect(self.emit_model_path)
        self.start_processing.clicked.connect(self.process_folder)
        self.preview.clicked.connect(self.preview_clicked.emit)

    def emit_model_path(self):
        base_name = self.combo_model.currentData()
        size = self.combo_model_size.currentData()
        task = self.combo_model_task.currentData()
        model_path = base_name + size

        if(task == "normal"):
            model_path = model_path + ".pt"
            self.model_selected.emit(model_path)
        else:
            model_path = model_path + "-" + task + ".pt"
            self.model_selected.emit(model_path)
    
    def copy_folder(self, files):
        os.makedirs("./images",exist_ok=True)
        copied_files = []
        
        for file in files:
            if file.lower().endswith((".jpg",".jpeg",".png")):
                hasher = hashlib.md5()
                name, ext = os.path.splitext(file)
                ext = ext.lower()
                with open(file, "rb") as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
                    hash = hasher.hexdigest()
                shutil.copy(file,os.path.join("images", f"{hash}{ext}"))
                copied_files.append(os.path.join("images", f"{hash}{ext}"))
        return copied_files


    def select_folder(self):
        self.current_folder = QFileDialog.getExistingDirectory(self, "Select image folder")

    def open_folder(self,folder_path):
        files = []
        folder = self.current_folder
        
        for file in os.listdir(folder):
            if file.lower().endswith((".jpg",".jpeg",".png")):
                files.append(os.path.join(folder,file))
        return files
        

    def process_folder(self):
        self.state_manager.processing_running = True
        og_files = self.open_folder(self.current_folder)
        files = self.copy_folder(og_files)
        
        for file in files:
            name = os.path.basename(file)
            self.detector.run_detection(file)
            results = self.state_manager.results
            boxes,scores,classes = results
            for i in range(len(boxes)):
                x1,y1,x2,y2 = boxes[i]
                score = scores[i]
                cls = classes[i]
                self.database_manager.add_image_to_table(name,self.state_manager.model_name,self.state_manager.class_names[int(cls)],int(score), float(x1),float(y1),float(x2),float(y2))
            
        self.state_manager.processing_running = False



