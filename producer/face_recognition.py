import cv2
import dlib

detector = dlib.get_frontal_face_detector()
# cap = cv2.VideoCapture(0)  # webcam
cap = cv2.VideoCapture('./sample.mp4')  # video

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

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        except Exception:
            pass

    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
