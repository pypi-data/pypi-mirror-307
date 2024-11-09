import os
from importlib import resources
from typing import Optional


# Modify the model path handling in process_video function
def process_video(
    input_path: str,
    model_path: str = None,  # Changed default to None
    output_path: Optional[str] = None,
    output_format: str = 'mjpeg',
    debug: bool = False
) -> None:
    if model_path is None:
        # Use the default model from the package
        model_path = "yolo11n-pose.pt"
        if not os.path.exists(model_path):
            print("Downloading YOLO model...")
            from ultralytics import YOLO
            YOLO(model_path)  # This will download the model if it doesn't exist
    
    # Rest of the function remains the same... 