from common import *
from app.widgets import ImagePreview
from app.widgets import ImageOptions
from detectors import YOLODetector
from app.widgets import ArchiverOptions


class MainPage(QWidget):
    def __init__(self,state_manager):
        super().__init__()
        self.state_manager = state_manager
        conf = 0.25 # do zmiany
        self.detector = YOLODetector("yolov8n.pt",conf,state_manager)
        layout_preview_page = QHBoxLayout()
        self.preview = ImagePreview(state_manager)
        self.options = ImageOptions(state_manager)
        preview_page = QWidget()
        layout_preview_page.addWidget(self.preview, stretch=7)
        layout_preview_page.addWidget(self.options, stretch=3)
        preview_page.setLayout(layout_preview_page)

        self.archiver_options = ArchiverOptions(state_manager,self.detector)

        self.stack = QStackedWidget()
        self.stack.addWidget(preview_page)
        self.stack.addWidget(self.archiver_options)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)


        
        self.archiver_options.preview_clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.options.archiver_clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.options.detect_clicked.connect(self.send_image_path_to_detector)
        self.state_manager.results_changed.connect(self.send_results_to_detector)


    def send_image_path_to_detector(self):
        self.detector.run_detection(self.state_manager.image_path)

    def save_image_path(self,image_path):
        self.state_manager.image_path = image_path
        self.preview.set_image(image_path)

    def send_results_to_detector(self, results):
        if self.state_manager.processing_running == False:
            self.preview.draw_bounding_boxes(results)
