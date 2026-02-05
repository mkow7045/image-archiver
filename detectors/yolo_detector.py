from ultralytics import YOLO
from common import *
#import time


class YOLODetector():

    def __init__(self, model_name,state_manager,parent=None):
        self.model_name = model_name
        self.state_manager = state_manager
        self.model = YOLO(model_name)
        self.state_manager.class_names = self.model.names
        self.state_manager.model_name = model_name
        self.fallback_model = "yolov8n.pt"
        self.parent = parent
        

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
            QMessageBox.critical(self.parent, "Error", "Not compatible model, switching to fallback.")
        
        self.state_manager.class_names = self.model.names
        self.state_manager.model_name = model_name

        metrics = self.model.val(data=r'C:\Users\desu\Desktop\git\image-archiver\detectors\test_data.yaml')  
        avg_inference_time = metrics.speed['inference']
        print(f"\n{'='*50}")
        print(f"Model: {model_name}")
        print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
        print(f"mAP@0.5: {metrics.box.map50:.4f}")
        print(f"mAP@0.75: {metrics.box.map75:.4f}")
        print(f"Precision: {metrics.box.mp:.4f}")
        print(f"Recall: {metrics.box.mr:.4f}")
        print(f"Time (inf):   {avg_inference_time:.2f} ms")
        print(f"{'='*50}\n")


    def run_detection(self,image_path):
        if(image_path and self.state_manager.busy != True):
            self.state_manager.busy = True

            #start_time = time.time()
            results = self.model.predict(image_path, save=False, imgsz=640, conf = self.state_manager.conf, verbose = False)
            #elapsed_time = time.time() - start_time
            #self.state_manager.avg_time += elapsed_time
            r = results[0]
            boxes = r.boxes.xyxy.cpu().numpy()
            score = r.boxes.conf.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()
            self.state_manager.results = (boxes,score,classes)
            self.state_manager.busy = False



        
        