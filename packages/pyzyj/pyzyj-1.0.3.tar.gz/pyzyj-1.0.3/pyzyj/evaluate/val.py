from ultralytics import YOLO

if __name__ == '__main__':
    yolo = YOLO('yolov8n.pt')
    data = 'data.yaml'
    data = 'temp.yaml'
    yolo.val(data=data, device=0, batch=5)