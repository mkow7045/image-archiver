from common import *
import os
import shutil
import hashlib

class ArchiverOptions(QWidget):
    image_selected = pyqtSignal(str) 
    model_selected = pyqtSignal(str)
    preview_clicked = pyqtSignal()
    refresh_page = pyqtSignal()
    export_clicked = pyqtSignal()
    db_delete_clicked = pyqtSignal()


    def __init__(self, state_manager, detector, database_manager):
        super().__init__()
        layout = QVBoxLayout()

        self.state_manager = state_manager
        self.database_manager = database_manager
        self.detector = detector

        detector_group = QGroupBox("Detector configuration")
        detector_group_layout = QVBoxLayout()
        detector_group.setLayout(detector_group_layout)
        processing_group = QGroupBox("Processing configuration")
        processing_group_layout = QVBoxLayout()
        processing_group.setLayout(processing_group_layout)
        visual_group = QGroupBox("Visual options")
        visual_group_layout = QVBoxLayout()
        visual_group.setLayout(visual_group_layout)
        db_group = QGroupBox("Database opeartions")
        db_group_layout = QVBoxLayout()
        db_group.setLayout(db_group_layout)
        self.load_file = QPushButton("Load file")
        self.load_folder = QPushButton("Load folder")
        self.load_model = QPushButton("Load model")
        self.color_picker = QPushButton("Choose bbox color")
        self.export_options = QPushButton("Export options")
        self.delete_from_db = QPushButton("Delete selection from database")


        self.conf_label = QLabel(f"Confidence: 25%")
        self.conf_slider = QSlider(Qt.Orientation.Horizontal)
        self.conf_slider.setMinimum(0)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(25)
        self.conf_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.conf_slider.setTickInterval(10)
        self.conf_slider.valueChanged.connect(self.update_conf)
    

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


        
        processing_group_layout.addWidget(self.load_file)
        processing_group_layout.addWidget(self.load_folder)
        detector_group_layout.addWidget(self.combo_model)
        detector_group_layout.addWidget(self.combo_model_size)
        detector_group_layout.addWidget(self.load_model)
        processing_group_layout.addWidget(self.conf_label)
        processing_group_layout.addWidget(self.conf_slider)
        visual_group_layout.addWidget(self.color_picker)
        db_group_layout.addWidget(self.export_options)
        db_group_layout.addWidget(self.delete_from_db)

        layout.addWidget(processing_group)
        layout.addWidget(detector_group)
        layout.addWidget(visual_group)
        layout.addWidget(db_group)

        self.setLayout(layout)

        self.load_file.clicked.connect(self.select_file)
        self.load_folder.clicked.connect(self.select_folder)
        self.load_model.clicked.connect(self.emit_model_path)
        self.color_picker.clicked.connect(self.get_color)
        self.export_options.clicked.connect(lambda: self.export_clicked.emit())
        self.delete_from_db.clicked.connect(lambda: self.db_delete_clicked.emit())

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.state_manager.color = color

    def update_conf(self, value):
        self.state_manager.conf = value / 100.0
        self.conf_label.setText(f"Confidence: {value}%")


    def emit_model_path(self):
        base_name = self.combo_model.currentData()
        size = self.combo_model_size.currentData()
        task = "normal"
        model_path = base_name + size


        self.state_manager.model_name = model_path + ".pt"
            

    
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
    

    def select_file(self):
        file = QFileDialog.getOpenFileName(self,"Select image")
        if file == ('', ''):
            return
        self.process_file(file)

    def select_folder(self):
        current_folder = QFileDialog.getExistingDirectory(self, "Select image folder")
        if(current_folder == ""):
            return
        self.process_folder(current_folder)

    def open_folder(self,folder_path):
        files = []
        folder = folder_path
        
        for file in os.listdir(folder):
            if file.lower().endswith((".jpg",".jpeg",".png")):
                files.append(os.path.join(folder,file))
        return files
        

    def process_folder(self, current_folder):
        self.state_manager.processing_running = True
        og_files = self.open_folder(current_folder)
        files = self.copy_folder(og_files)

        progress = QProgressDialog("Starting processing",None, 0,len(files), self)
        progress.show()

        progress_bar_num=1
        
        for file in files:
            name = os.path.basename(file)
            progress.setLabelText(f"Processing file: {name}")
            progress_bar_num += 1
            progress.setValue(progress_bar_num)
            QApplication.processEvents()
            self.detector.run_detection(file)
            results = self.state_manager.results
            boxes,scores,classes = results
            for i in range(len(boxes)):
                x1,y1,x2,y2 = boxes[i]
                score = scores[i]
                cls = classes[i]
                self.database_manager.add_image_to_table(name,self.state_manager.model_name,self.state_manager.class_names[int(cls)],float(score), float(x1),float(y1),float(x2),float(y2))
            self.refresh_page.emit()
        
        progress.close()
        self.state_manager.processing_running = False

    def process_file(self, file):
        self.state_manager.processing_running = True
        file = file[0]
        copied = self.copy_folder([file])
        name = os.path.basename(copied[0])
        print(name)
        self.detector.run_detection(copied[0])
        results = self.state_manager.results
        boxes,scores,classes = results
        for i in range(len(boxes)):
                x1,y1,x2,y2 = boxes[i]
                score = scores[i]
                cls = classes[i]
                self.database_manager.add_image_to_table(name,self.state_manager.model_name,self.state_manager.class_names[int(cls)],float(score), float(x1),float(y1),float(x2),float(y2))
        self.refresh_page.emit()
        self.state_manager.processing_running = False



