import itertools

import cv2
from confluent_kafka import Producer

# cap = cv2.VideoCapture(0)  # webcam
cap = cv2.VideoCapture('./sample.mp4')  # video

p = Producer({'bootstrap.servers': 'localhost:9092'})

producing_count: int = 1

producing_iterator = itertools.count()
if producing_count:
    producing_iterator = range(producing_count)

for i in producing_iterator:
    ret, img = cap.read()  # img.shape is (360, 640, 3)

    if not ret:
        break

    try:
        p.produce('mytopic', key='hello', value=img.tobytes())
        p.flush(30)  # 하나씩 전송함을 보장

    except Exception as e:
        print(e)
        pass

    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
