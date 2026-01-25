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
    model_options_clicked = pyqtSignal()
    detection_start = pyqtSignal(str)


    def __init__(self, state_manager,detector, database_manager):
        super().__init__()
        layout = QVBoxLayout()

        self.state_manager = state_manager
        self.database_manager = database_manager

        processing_group = QGroupBox("Processing configuration")
        processing_group_layout = QVBoxLayout()
        processing_group.setLayout(processing_group_layout)
        visual_group = QGroupBox("Visual options")
        visual_group_layout = QVBoxLayout()
        visual_group.setLayout(visual_group_layout)
        db_group = QGroupBox("Database opeartions")
        db_group_layout = QVBoxLayout()
        db_group.setLayout(db_group_layout)
        self.load_button = QToolButton()
        self.load_button.setText("Load")
        self.load_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.draw_selected_only = QCheckBox("Draw only selected classes")

        self.load_menu = QMenu(self)
        load_file = QAction("Load file", self)
        load_folder = QAction("Load folder", self)
        

        load_file.triggered.connect(self.select_file)
        load_folder.triggered.connect(self.select_folder)

        self.load_menu.addAction(load_file)
        self.load_menu.addAction(load_folder)

        self.load_button.setMenu(self.load_menu)

        self.dark = QRadioButton("Dark mode")
        self.light = QRadioButton("Light mode")
        self.dark.setChecked(True)

        self.conf_label = QLabel(f"Confidence: 25%")
        self.conf_slider = QSlider(Qt.Orientation.Horizontal)
        self.conf_slider.setMinimum(0)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(25)
        self.conf_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.conf_slider.setTickInterval(10)
        self.conf_slider.valueChanged.connect(self.update_conf)
        

        self.selection_group = QButtonGroup()
        self.selection_group.addButton(self.dark,1)
        self.selection_group.addButton(self.light,2)

        self.colors = QWidget()
        self.colors_layout = QHBoxLayout()

        self.colors_layout.addWidget(self.dark)
        self.colors_layout.addWidget(self.light)

        self.colors.setLayout(self.colors_layout)
        


        self.color_picker = QPushButton("Choose bounding box color for all images")
        self.export_options = QPushButton("Export options")
        self.delete_from_db = QPushButton("Delete selection from database")
        self.model_options = QPushButton("Model options")

        self.model_label = QLabel(f"Model loaded: {self.state_manager.model_name}")

        
        processing_group_layout.addWidget(self.load_button)
        processing_group_layout.addWidget(self.model_label)
        processing_group_layout.addWidget(self.model_options)
        processing_group_layout.addWidget(self.conf_label)
        processing_group_layout.addWidget(self.conf_slider)
        visual_group_layout.addWidget(self.color_picker)
        visual_group_layout.addWidget(self.colors)
        visual_group_layout.addWidget(self.draw_selected_only)
        db_group_layout.addWidget(self.export_options)
        db_group_layout.addWidget(self.delete_from_db)

        layout.addWidget(processing_group)
        layout.addWidget(visual_group)
        layout.addWidget(db_group)

        self.setLayout(layout)

        self.load_button.clicked.connect(self.show_load_menu)
        self.color_picker.clicked.connect(self.get_color)
        self.export_options.clicked.connect(lambda: self.export_clicked.emit())
        self.delete_from_db.clicked.connect(lambda: self.db_delete_clicked.emit())
        self.model_options.clicked.connect(lambda: self.model_options_clicked.emit())
        self.selection_group.buttonClicked.connect(self.change_theme)
        self.draw_selected_only.stateChanged.connect(self.send_draw_selected_only)

    
    def send_draw_selected_only(self, state):
        self.state_manager.draw_only_selected = (state == Qt.CheckState.Checked.value)
        

    def update_conf(self, value):
        self.state_manager.conf = value / 100.0
        self.conf_label.setText(f"Confidence: {value}%")

    def update_conf_after_model(self):
        self.conf_slider.setValue(int(self.state_manager.conf * 100))
        self.conf_label.setText(f"Confidence: {int(self.state_manager.conf * 100)}%")

    
    def change_theme(self):
        selected_entry = self.selection_group.checkedId()
        if selected_entry == 1:
            self.state_manager.theme = "dark"
        if selected_entry == 2:
            self.state_manager.theme = "light"

    def show_load_menu(self):
        self.load_menu.setMinimumWidth(self.load_button.width())
        button_pos = self.load_button.mapToGlobal(self.load_button.rect().bottomLeft())
        self.load_menu.exec(button_pos)

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
        progress.setWindowTitle("Processing files")
        progress.show()

        progress_bar_num=1
        
        for file in files:
            name = os.path.basename(file)
            self.database_manager.delete_single(name)
            progress.setLabelText(f"Processing file: {name}")
            progress.setMinimumDuration(0)
            progress.setValue(progress_bar_num)
            progress_bar_num += 1
            QApplication.processEvents()
            QApplication.processEvents()
            self.detection_start.emit(file)
            results = self.state_manager.results
            boxes,scores,classes = results
            
            if len(boxes) == 0:
                if os.path.exists(file):
                    os.remove(file)
            else:
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
        progress = QProgressDialog("Starting processing",None, 0,0, self)
        progress.setWindowTitle("Processing files")
        progress.show()
        QApplication.processEvents()
        QApplication.processEvents()
        file = file[0]
        copied = self.copy_folder([file])
        if not copied:
            progress.close()
            self.state_manager.processing_running = False
            return
        name = os.path.basename(copied[0])
        self.database_manager.delete_single(name)
        self.detection_start.emit(copied[0])
        results = self.state_manager.results
        boxes,scores,classes = results
        if len(boxes) == 0:
            if os.path.exists(copied[0]):
                os.remove(copied[0])
        else:
            for i in range(len(boxes)):
                    x1,y1,x2,y2 = boxes[i]
                    score = scores[i]
                    cls = classes[i]
                    self.database_manager.add_image_to_table(name,self.state_manager.model_name,self.state_manager.class_names[int(cls)],float(score), float(x1),float(y1),float(x2),float(y2))
        progress.close()
        self.refresh_page.emit()
        self.state_manager.processing_running = False

    
    def set_model_label(self):
        self.model_label.setText(f"Model loaded: {os.path.basename(self.state_manager.model_name)}")



