import base64

import cv2
import dlib
import numpy as np
from confluent_kafka import Producer

detector = dlib.get_frontal_face_detector()
# cap = cv2.VideoCapture(0)  # webcam
cap = cv2.VideoCapture('./sample.mp4')  # video

p = Producer({'bootstrap.servers': 'localhost:9092'})

while True:
    ret, img = cap.read()

    if not ret:
        break

    dets = detector(img)

    for det in dets:
        try:
            x1 = det.left()
            y1 = det.top()
            x2 = det.right()
            y2 = det.bottom()

            # draw a face area
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # TODO: 얼굴 탐지를 kafka streams 기능을 사용할 수 없는지
            face_crop_img: np.ndarray = img[y1:y2, x1:x2]

            # TODO: 이미지를 시리얼라이즈하는 방법을 찾아보기
            face_crop_str = base64.b64encode(face_crop_img.tobytes())

            # TODO: 코드 구조를 생각해보기
            p.produce('mytopic', key='hello', value=face_crop_img.tobytes())
            p.flush(30)  # 하나씩 전송함을 보장

        except Exception as e:
            print(e)
            pass

    cv2.imshow('result', face_crop_img)
    if cv2.waitKey(1) == ord('q'):
        break
