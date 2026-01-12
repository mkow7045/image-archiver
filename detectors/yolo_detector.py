from ultralytics import YOLO
from common import *


class YOLODetector():

    def __init__(self, model_name, conf,state_manager):
        self.model_name = model_name
        self.conf = conf
        self.state_manager = state_manager
        self.model = YOLO(model_name)
        self.state_manager.class_names = self.model.names
        self.state_manager.model_name = model_name
        self.fallback_model = "yolov8n.pt"
        

    def set_model(self, model_name):
        try:
            self.model = YOLO(model_name)
            if self.model.task != "detect":
                raise ValueError()
            
            if not isinstance(self.model.names, dict) or len(self.model.names) == 0:
                raise ValueError()
        except Exception as e:
            self.model = YOLO(self.fallback_model)
            model_name = self.fallback_model
            QMessageBox.critical(self, "Error", "Not compatible model, switching to fallback.")
        
        self.state_manager.class_names = self.model.names
        self.state_manager.model_name = model_name



    def run_detection(self,image_path):
        if(image_path and self.state_manager.busy != True):
            self.state_manager.busy = True
            results = self.model.predict(image_path, save=False, imgsz=640, conf = self.state_manager.conf, verbose = False)
            r = results[0]
            boxes = r.boxes.xyxy.cpu().numpy()
            score = r.boxes.conf.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()
            self.state_manager.results = (boxes,score,classes)
            self.state_manager.busy = False
        else:
            print("No image loaded!")


        
        