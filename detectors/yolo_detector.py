from .base_detector import BaseDetector
from ultralytics import YOLO
from common import *


class YOLODetector(BaseDetector):

    def __init__(self, model_name, conf,state_manager):
        super().__init__(model_name, conf)
        self.state_manager = state_manager
        self.model = YOLO(model_name)
        self.state_manager.class_names = self.model.names
        self.state_manager.model_name = model_name


        self.state_manager.model_name_changed.connect(self.set_model)
        

    def set_model(self, model_name, conf=0.25):
        self.model = YOLO(model_name)
        self.state_manager.model_name = model_name
        print("Model set!")



    def run_detection(self,image_path):
        if(image_path and self.state_manager.busy != True):
            self.state_manager.busy = True
            results = self.model.predict(image_path, save=False, imgsz=640, conf = self.conf, verbose = False)
            r = results[0]
            boxes = r.boxes.xyxy.cpu().numpy()
            score = r.boxes.conf.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()
            self.state_manager.results = (boxes,score,classes)
            self.state_manager.busy = False
        else:
            print("No image loaded!")


        
        