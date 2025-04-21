from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
import io
import time
import logging
import os

# Configure logging to write to file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="YOLOv8 Number Plate Detection API")

model_name = os.getenv("MODEL_NAME", "yolov8n-fn.pt")

models = ["yolov8n-fn.pt", "yolov8s-fn.pt", "yolov8m-fn.pt"]
if model_name not in models:
    logger.error(f"Invalid model name: {model_name}. Defaulting to yolov8n-fn.pt")
    model_name = "yolov8n-fn.pt"

model = YOLO(f"models/{model_name}")  # Load the YOLOv8 model
logger.info("YOLOv8-Nano model loaded successfully")

@app.get("/")
async def root():
    return {"message": "Welcome to the YOLOv8 Number Plate Detection API"}

@app.post("/detect")
async def detect_number_plate(file: UploadFile = File(...)):
    request_time = time.time()  # Start time
    try:
        image_bytes = await file.read()
        np_img = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Convert to OpenCV format

        if image is None:
            raise ValueError("Invalid image format. Could not decode.")

        results = model(image, conf=0.5, iou=0.3)

        detections = []
        for result in results:
            for box in result.boxes:
                x, y, w, h = box.xywh[0].tolist()  # Extract bounding box coordinates
                conf = box.conf[0].item()  # Confidence score
                detections.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "confidence": conf
                })

        response_time = time.time()  # End time
        elapsed_time = round(response_time - request_time, 4)  # Calculate processing time

        logger.info(f"Request received: {file.filename} at {request_time}")
        logger.info(f"Response sent at {response_time}, Processing Time: {elapsed_time}s")
        
        return {
            "detections": detections,
            "processing_time": elapsed_time
        }

    except Exception as e:
        logger.error(f"Error during detection: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
