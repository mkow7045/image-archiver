from common import *
import torch
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights, fasterrcnn_mobilenet_v3_large_fpn, FasterRCNN_MobileNet_V3_Large_FPN_Weights, retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights
from PIL import Image
from .rcnn_validator import validate_rcnn

class RCNNDetector():
    def __init__(self, model_name, state_manager):
        self.model_name = model_name
        self.state_manager = state_manager
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize model and weights
        self.model, self.weights = self.load_model(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        self.state_manager.model_name = model_name
        self.state_manager.class_names = {i: name for i, name in enumerate(self.weights.meta["categories"])}
        self.transform = transforms.Compose([transforms.ToTensor()])
        
    def load_model(self, model_name):
        if model_name == "fasterrcnn_resnet50":
            weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
            model = fasterrcnn_resnet50_fpn_v2(weights=weights)
        elif model_name == "fasterrcnn_mobilenet":
            weights = FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT
            model = fasterrcnn_mobilenet_v3_large_fpn(weights=weights)
        elif model_name == "retinanet_resnet50":
            weights = RetinaNet_ResNet50_FPN_Weights.DEFAULT
            model = retinanet_resnet50_fpn(weights=weights)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        return model, weights
    
    def set_model(self, model_name):
        self.model_name = model_name
        self.model, self.weights = self.load_model(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        # Update state manager with new class names
        self.state_manager.model_name = model_name
        self.state_manager.class_names = {i: name for i, name in enumerate(self.weights.meta["categories"])}

        
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

                filter = ((classes > 0) & (scores > self.state_manager.conf))

                boxes = boxes[filter]
                scores = scores[filter]
                classes = classes[filter]

            
                self.state_manager.results = (boxes,scores,classes)

                self.state_manager.busy = False

    def validate(self, images_dir, annotations_dir):
        return validate_rcnn(
            model=self.model,
            images_dir=images_dir,
            annotations_dir=annotations_dir,
            class_names=self.state_manager.class_names,
            device=self.device
        )