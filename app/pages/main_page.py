from common import *
from app.widgets import ImagePreview
from detectors import YOLODetector
from app.widgets import ArchiverOptions
from .archiver_page import Archiver
from app.widgets import PreviewOptions
from app.widgets import ExportOptions
from app.widgets import DatabaseDelete
from app.widgets import QueryBuilder
from app.widgets import ModelOptions



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
        self.archiver_options.export_clicked.connect(self.start_export)
        self.archiver_options.db_delete_clicked.connect(self.start_db_delete)
        self.state_manager.results_changed.connect(self.send_results_to_detector)
        self.archiver_main.gallery.thumb_clicked.connect(self.send_preview_image)
        self.preview_options.back_to_archiver.connect(self.back_to_gallery)
        self.preview_options.set_local_color.connect(self.apply_local_color)
        self.preview_options.delete_selected_image.connect(self.delete_single_image)
        self.archiver_main.query_builder_clicked.connect(self.open_query_builder)
        self.archiver_options.model_options_clicked.connect(self.open_model_options)


    def delete_single_image(self):
        self.database_manager.delete_single(self.state_manager.image_path)
        self.archiver_main.get_images_from_db()
        self.back_to_gallery()

    def back_to_gallery(self):
        self.stack.setCurrentIndex(0)
        self.apply_local_color(self.state_manager.color)

    def apply_local_color(self,color):
        self.preview.color = color
        self.preview.draw_bounding_boxes(self.preview.current_results)

    def start_db_delete(self):
        db_delete = DatabaseDelete(self.database_manager)
        db_delete.exec()
        self.archiver_main.get_images_from_db()

    def start_export(self):
        export = ExportOptions(self.database_manager, self.state_manager)
        export.exec()

    def open_model_options(self):
        model_options = ModelOptions(self.database_manager, self.state_manager)
        model_options.exec()
    
    def open_query_builder(self):
        builder = QueryBuilder(self.state_manager,self.database_manager)
        builder.query_ready.connect(lambda text: self.archiver_main.tag_chooser.setText(text))
        builder.exec()
        self.archiver_main.get_images_from_db()
        

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
        
        


        
