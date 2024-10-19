import time
import os
import cv2
import requests
import json
from ultralytics import YOLO
from multiprocessing import Process

delay = float(os.environ.get('DELAY', 0))
tg_token = os.environ.get('TG_TOKEN')
tg_chat_id = os.environ.get('TG_CHAT_ID')

model = YOLO('yolov10n.pt', verbose=False)
conf_tresh = float(os.environ.get('CONF_TRESH', 0.5))
classes = [0]


def get_rtsp_frame(address):
    vcap = cv2.VideoCapture(address)
    ret, frame = vcap.read()
    vcap.release()
    return frame


def detect_objects(frame, filename):
    results = model.predict(source=frame, save=False, conf=conf_tresh, classes=classes)
    if len(results[0].boxes) > 0:
        print(f"[INFO] Found {len(results[0].boxes)} detections.")
        results[0].plot(save=True, filename=filename)
        return True
    else:
        print("[INFO] No detections.")
        return False


def send_notification(camera, filename):
    data = {
        'chat_id': tg_chat_id,
        'caption': f'Object detected on {camera}!',
    }
    url = f'https://api.telegram.org/bot{tg_token}/sendPhoto'
    with open(filename, 'rb') as image_file:
        requests.post(url, data=data, files={"photo": image_file})


def camera_loop(rtsp, name):
    while True:
        if detect_objects(get_rtsp_frame(rtsp), f"{name}.jpg"):
            print(f"[INFO] Object detected on {name}!")
            send_notification(name, f"{name}.jpg")
        time.sleep(delay)


def main():
    # Load cameras from config
    with open('config.json') as f:
        config = json.load(f)
    cameras = [(camera['url'], camera['name']) for camera in config['cameras']]

    # Start processes for each camera
    processes = []
    for camera in cameras:
        print("[INFO] Starting process for", camera[1])
        processes.append(Process(target=camera_loop, args=(camera[0], camera[1])))
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
