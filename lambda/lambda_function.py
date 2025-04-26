import time
import os
import logging
import boto3
import base64
import numpy as np
import cv2
from ultralytics import YOLO
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ---- Cold start timing ----
cold_start_begin = time.time()

MODEL_BUCKET = os.getenv("MODEL_BUCKET")
MODEL_KEY = os.getenv("MODEL_KEY")
LOCAL_MODEL_PATH = f"/tmp/{MODEL_KEY}.pt"

def download_model():
    if not os.path.exists(LOCAL_MODEL_PATH):
        logger.info("Downloading model from S3...")
        s3 = boto3.client('s3')
        s3.download_file(MODEL_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
        logger.info("Model downloaded.")

download_model()
model = YOLO(LOCAL_MODEL_PATH)
logger.info("Model loaded.")

# ---- Cold start done ----
cold_start_end = time.time()
cold_start_latency = round(cold_start_end - cold_start_begin, 4)
logger.info(f"Cold start latency: {cold_start_latency}s")

# Lambda handler
def handler(event, context):
    try:
        start = time.time()

        body = json.loads(event['body'])
        if body.get("isBase64Encoded", False):
            image_bytes = base64.b64decode(body['body'])
        else:
            image_bytes = body['body'].encode()

        np_img = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Could not decode image.")

        results = model(image, conf=0.5, iou=0.3)
        detections = []

        for result in results:
            for box in result.boxes:
                x, y, w, h = box.xywh[0].tolist()
                conf = box.conf[0].item()
                detections.append({
                    "x": x, "y": y,
                    "width": w, "height": h,
                    "confidence": conf
                })

        return {
            "statusCode": 200,
            "body": {
                "detections": detections,
                "processing_time": round(time.time() - start, 4),
                "cold_start_latency": cold_start_latency
            }
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": {"error": str(e)}
        }
