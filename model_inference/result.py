import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from ultralytics import YOLO

# Load three YOLOv8 variants
models = {
    "YOLOv8n": YOLO("models/yolov8n-fn.pt"),
    "YOLOv8s": YOLO("models/yolov8s-fn.pt"),
    "YOLOv8m": YOLO("models/yolov8m-fn.pt")
}

# Load six sample images from the CCPD dataset
image_paths = glob.glob("ccpd_samples/*.jpg")[:6]  # Adjust folder & ensure 6 images exist

# Define confidence threshold and IoU threshold
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.3

# Function to draw bounding boxes
def draw_boxes(image, results):
    output_image = image.copy()
    for result in results:
        for box in result.boxes:
            x, y, w, h = map(int, box.xywh[0].tolist())  # Convert to integer
            conf = box.conf[0].item()  # Confidence score
            
            # Draw bounding box
            cv2.rectangle(output_image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
            
            # Define label text
            label = f"Conf: {conf:.2f}"
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]  # Get text size
            
            # Calculate text position
            text_x = x - w // 2
            text_y = y - h // 2 - 10
            text_w, text_h = text_size
            
            # Draw black background rectangle for text
            cv2.rectangle(output_image, (text_x, text_y - text_h - 5), (text_x + text_w + 5, text_y), (0, 0, 0), cv2.FILLED)
            
            # Put white text on black background
            cv2.putText(output_image, label, (text_x, text_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return output_image

# Process each image
for row, image_path in enumerate(image_paths):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # Convert for Matplotlib

    # Run inference for each model
    for col, (model_name, model) in enumerate(models.items()):
        results = model(original_image, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD)
        output_image = draw_boxes(original_image, results)
        
        # Save results
        cv2.imwrite(f"results/{model_name}_image{row}.jpg", output_image)
