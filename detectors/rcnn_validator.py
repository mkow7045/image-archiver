"""
R-CNN Validator z użyciem TorchMetrics
Wymaga: pip install torchmetrics
"""
import torch
import xml.etree.ElementTree as ET
import time  # <--- Dodano do mierzenia czasu
from pathlib import Path
from PIL import Image
from torchvision import transforms
from torchmetrics.detection.mean_ap import MeanAveragePrecision

def parse_voc_xml(xml_path, class_mapping):
    root = ET.parse(xml_path).getroot()
    boxes, labels = [], []
    
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name in class_mapping:
            bnd = obj.find('bndbox')
            boxes.append([
                float(bnd.find('xmin').text), float(bnd.find('ymin').text),
                float(bnd.find('xmax').text), float(bnd.find('ymax').text)
            ])
            labels.append(class_mapping[name])
            
    return {
        'boxes': torch.tensor(boxes, dtype=torch.float32),
        'labels': torch.tensor(labels, dtype=torch.int64)
    }

def validate_rcnn(model, images_dir, annotations_dir, class_names, device=None):
    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()
    
    metric = MeanAveragePrecision(iou_type="bbox", class_metrics=True)
    
    name_to_id = {v: k for k, v in class_names.items()}
    transform = transforms.Compose([transforms.ToTensor()])
    
    xml_files = list(Path(annotations_dir).glob('*.xml'))
    print(f"Walidacja na {len(xml_files)} obrazach...")

    preds = []
    targets = []
    inference_times = [] 

    for xml_file in xml_files:
        img_path = next((p for p in Path(images_dir).glob(f"{xml_file.stem}.*") 
                         if p.suffix.lower() in ['.jpg', '.png', '.jpeg']), None)
        
        if not img_path: continue

        img = transform(Image.open(img_path).convert("RGB")).to(device)
        
        if device.type == 'cuda': torch.cuda.synchronize()
        start_time = time.time()
        
        with torch.no_grad():
            output = model([img])[0]
            
        if device.type == 'cuda': torch.cuda.synchronize()
        inference_times.append(time.time() - start_time)
        # --------------------

        preds.append({
            'boxes': output['boxes'].cpu(),
            'scores': output['scores'].cpu(),
            'labels': output['labels'].cpu()
        })
        
        gt = parse_voc_xml(xml_file, name_to_id)
        if len(gt['boxes']) > 0:
            targets.append(gt)

    print("Obliczam metryki...")
    metric.update(preds, targets)
    result = metric.compute()
    
    avg_time_ms = (sum(inference_times) / len(inference_times)) * 1000 if inference_times else 0

    print("=" * 40)
    print(f"mAP (0.5:0.95):   {result['map'].item():.4f}")
    print(f"mAP@0.5:          {result['map_50'].item():.4f}")
    print(f"mAP@0.75:         {result['map_75'].item():.4f}")
    print("-" * 40)
    print(f"Recall (mAR@100): {result['mar_100'].item():.4f}")
    print("-" * 40)
    print(f"Średni czas:      {avg_time_ms:.2f} ms")
    print("=" * 40)
    

    return {
        'mAP': result['map'].item(),
        'mAP@0.5': result['map_50'].item(),
        'mAP@0.75': result['map_75'].item(),
        'Recall': result['mar_100'].item(),
        'Time_ms': avg_time_ms
    }