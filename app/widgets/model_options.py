from common import *

class ModelOptions(QDialog):

    def __init__(self, database_manager, state_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Model options")
        self.setModal(True)

        self.setMinimumSize(650,300)

        self.state_manager = state_manager

        self.class_names = self.state_manager.class_names

        layout = QVBoxLayout()

        self.database_manager = database_manager

        self.menus = QWidget()
        self.menus_layout = QHBoxLayout()
        self.menus.setLayout(self.menus_layout)

        self.yolo_menu = QRadioButton("YOLO models (Ultralytics COCO)")
        self.rcnn_menu = QRadioButton("Faster R-CNN (Resnet)")
        self.custom_menu = QRadioButton("Custom (Ultralytics)")
        self.yolo_menu.setChecked(True)

        self.accept_model_yolo = QPushButton("Load model")

        self.rcnn_label = QLabel("Faster R-CNN RESNET model will be loaded.")

        self.menus_layout.addWidget(self.yolo_menu)
        self.menus_layout.addWidget(self.rcnn_menu)
        self.menus_layout.addWidget(self.custom_menu)
        

        self.accept_custom_yolo = QPushButton("Choose .pt file and load model")
        

        self.menu_group = QButtonGroup()
        self.menu_group.addButton(self.yolo_menu,1)
        self.menu_group.addButton(self.rcnn_menu,2)
        self.menu_group.addButton(self.custom_menu,2)


        self.options_widget = QWidget()
        self.options_widget_layout = QVBoxLayout()
        self.options_widget.setLayout(self.options_widget_layout)

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


        self.options_widget_layout.addWidget(self.conf_label)
        self.options_widget_layout.addWidget(self.conf_slider)
        self.options_widget_layout.addWidget(self.combo_model)
        self.options_widget_layout.addWidget(self.combo_model_size)
        self.options_widget_layout.addWidget(self.accept_model_yolo)
        


        
        layout.addWidget(self.menus, stretch=2)
        layout.addWidget(self.options_widget, stretch=8)


        self.setLayout(layout)
        
        self.accept_model_yolo.clicked.connect(self.emit_yolo_model_path)
        self.menu_group.buttonToggled.connect(self.change_options)
        self.accept_custom_yolo.connect(self.load_custom_yolo)

    def update_conf(self, value):
        self.state_manager.conf = value / 100.0
        self.conf_label.setText(f"Confidence: {value}%")

    def emit_yolo_model_path(self):
        base_name = self.combo_model.currentData()
        size = self.combo_model_size.currentData()
        model_path = base_name + size


        self.state_manager.model_name = model_path + ".pt"
        self.close()

    def change_options(self):
        selected_option = self.menu_group.checkedId()
        while self.options_widget_layout.count():
            item = self.options_widget_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        

        if selected_option == 1:
            self.options_widget_layout.addWidget(self.conf_label)
            self.options_widget_layout.addWidget(self.conf_slider)
            self.options_widget_layout.addWidget(self.combo_model)
            self.options_widget_layout.addWidget(self.combo_model_size)
            self.options_widget_layout.addWidget(self.accept_model_yolo)

        if selected_option == 2:
            self.options_widget_layout.addWidget(self.rcnn_label)

        if selected_option == 3:
            self.options_widget_layout.addWidget(self.conf_label)
            self.options_widget_layout.addWidget(self.conf_slider)
            self.options_widget_layout.addWidget(self.accept_custom_yolo)

    def load_custom_yolo(self):
        model_path, _ = QFileDialog.getSaveFileName(self, "Choose place to save","","CSV files (*.csv)")
        self.state_manager.model_name = model_path + ".pt"