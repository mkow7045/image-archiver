from common import *
from app.widgets import ImagePreview
from detectors import YOLODetector
from app.widgets import ArchiverOptions
from .archiver_page import Archiver
from app.widgets import PreviewOptions



class MainPage(QWidget):
    def __init__(self,state_manager,database_manager):
        super().__init__()
        self.state_manager = state_manager
        self.database_manager = database_manager
        self.detector = YOLODetector("yolov8n.pt",self.state_manager.conf,state_manager)
        layout_single_detection_page = QHBoxLayout()
        layout_archiver_page = QHBoxLayout()
        self.preview = ImagePreview(state_manager)


        

        self.archiver_options = ArchiverOptions(state_manager,self.detector,database_manager)
        self.archiver_main = Archiver(state_manager, database_manager)
        archiver_page = QWidget()
        layout_archiver_page.addWidget(self.archiver_main, stretch=7)
        layout_archiver_page.addWidget(self.archiver_options, stretch=3)
        archiver_page.setLayout(layout_archiver_page)


        layout_preview_page = QHBoxLayout()
        preview_page = QWidget()
        self.preview_options = PreviewOptions()
        layout_preview_page.addWidget(self.preview, stretch=7)
        layout_preview_page.addWidget(self.preview_options, stretch=3)
        preview_page.setLayout(layout_preview_page)
        


        self.stack = QStackedWidget()
        self.stack.addWidget(archiver_page)
        self.stack.addWidget(preview_page)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)


        
        self.archiver_options.preview_clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.archiver_options.refresh_page.connect(lambda: self.archiver_main.get_images_from_db())
        self.state_manager.results_changed.connect(self.send_results_to_detector)
        self.archiver_main.gallery.thumb_clicked.connect(self.send_preview_image)
        self.preview_options.back_to_archiver.connect(lambda: self.stack.setCurrentIndex(0))


    def send_image_path_to_detector(self):
        self.detector.run_detection(self.state_manager.image_path)

    def save_image_path(self,image_path):
        self.state_manager.image_path = image_path
        self.preview.set_image(image_path)

    def send_results_to_detector(self, results):
        if self.state_manager.processing_running == False:
            self.preview.draw_bounding_boxes(results)

    def send_preview_image(self, image):
        self.state_manager.image_path = image
        self.stack.setCurrentIndex(1)
        self.preview.draw_bounding_boxes(self.database_manager.get_results_from_db(image))
        
        


        
