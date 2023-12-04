import cv2
from ultralytics import YOLO
from win32com.client import Dispatch
model = YOLO("yolov8n.pt")
speak = Dispatch("SAPI.SpVoice")
cap = cv2.VideoCapture("http://192.168.1.7:81/stream") 
"""
đây là cái đường link(thay thế tùy theo cái nó hiện ra trong serial monitor) mà chỉ có cam thôi
chứ link thường cv2 ko đọc đc cam
"""
cap.set(cv2.CAP_PROP_FPS, 30)
if not cap.isOpened():
    print("Lỗi cam 1")
    exit()
while True:
    ret, frame = cap.read()
    cv2.imshow('Frame', frame)
    results = model.predict(show=True, source=frame)
    item_detect = []
    for r in results:
        for obj in r.boxes:
            class_id = int(obj.cls.item())
            item_name = model.names[class_id]
            item_detect.append(item_name)
            print(item_name)
            score = obj.conf.item()
            if score >= 0.85:
                speak.Speak(item_name)# nó sẽ đọc ra tên vật thể nếu như độ tin cậy của vật thể lớn hơn 85% 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
