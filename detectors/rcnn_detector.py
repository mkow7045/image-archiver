from .base_detector import BaseDetector
from common import *
import torch
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights, fasterrcnn_mobilenet_v3_large_fpn, FasterRCNN_MobileNet_V3_Large_FPN_Weights, retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights
from PIL import Image

class RCNNDetector(BaseDetector):
    def __init__(self,model_name,state_manager):
        super().__init__(model_name)
        self.state_manager = state_manager
        self.model_name = model_name

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        
        self.model = self.load_model()
        self.model.to(self.device)
        self.model.eval()

        

        self.state_manager.model_name = model_name
        self.state_manager.class_names = {i: name for i, name in enumerate(self.weights.meta["categories"])}

        self.transform = transforms.Compose([transforms.ToTensor()])

        self.state_manager.model_name_changed.connect(self.set_model)


    def load_model(self):
        if self.model_name == "fasterrcnn_resnet50":
            self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            return fasterrcnn_resnet50_fpn_v2(weights=self.weights)

        elif self.model_name == "fasterrcnn_mobilenet":
            self.weights = FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT
            return fasterrcnn_mobilenet_v3_large_fpn(weights=self.weights)

        elif self.model_name == "retinanet_resnet50":
            self.weights = RetinaNet_ResNet50_FPN_Weights.DEFAULT
            return retinanet_resnet50_fpn(weights=self.weights)

    def set_model(self, model_name):
        self.state_manager.model_name = model_name
        self.model = self.load_model()
        self.model.to(self.device)
        self.model.eval()

        
        self.state_manager.class_names = {i: name for i, name in enumerate(self.weights.meta["categories"])}

    def run_detection(self,image_path):
        if image_path and not self.state_manager.busy:
            self.state_manager.busy = True

            image = Image.open(image_path).convert("RGB")
            image_tensor = self.transform(image).to(self.device)

            with torch.no_grad():
                outputs = self.model([image_tensor])[0]

                boxes = outputs["boxes"].cpu().numpy()
                scores = outputs["scores"].cpu().numpy()
                classes = outputs["labels"].cpu().numpy()
                print(f"Raw classes from model: {classes[:5]}")  # First 5
                print(f"Class names dict keys: {list(self.state_manager.class_names.keys())[:20]}")

                filter = ((classes > 0) & (scores > self.state_manager.conf))

                boxes = boxes[filter]
                scores = scores[filter]
                classes = classes[filter]
                print(f"After filter, before shift: {classes[:5]}")
                classes = classes - 1
                print(f"After shift: {classes[:5]}")
                print(f"Mapped names: {[self.state_manager.class_names.get(int(c), 'UNKNOWN') for c in classes[:5]]}")
            
                self.state_manager.results = (boxes,scores,classes)

                self.state_manager.busy = False
        else:
            print("No image")