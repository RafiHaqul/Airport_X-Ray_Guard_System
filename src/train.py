from ultralytics import YOLO

"""
Dokumntasi untuk parameter yolo
https://docs.ultralytics.com/modes/train#musgd-optimizer
"""

def main():
    # Load model (bisa nano, medium, large)
    model = YOLO("yolov8n.pt") 

    # Jalankan training
    results = model.train(
        data    = "../configs/yolo11n.yaml", 
        epochs  = 5, 
        imgsz   = 640,
        batch   = 8,
        device  = 0,
        amp = True,
        project = "../outputs/models/",  
        name    = "ldxray_yolo11n", 
        patience= 5,
        save    = True,
        val     = True,
        workers = 0,
        cache   = "False"
    )

if __name__ == "__main__":
    main()