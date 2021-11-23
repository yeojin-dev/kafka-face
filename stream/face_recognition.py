import dlib
import faust
import numpy as np

app = faust.App(
    'hello-world',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

greetings_topic = app.topic('mytopic')
detector = dlib.get_frontal_face_detector()


@app.agent(greetings_topic)
async def greet(greetings):
    async for raw_img in greetings:
        raw_img = np.frombuffer(raw_img, dtype=np.uint8).reshape(360, 640, 3)  # 샘플 비디오의 차원

        dets = detector(raw_img)
        for det in dets:
            try:
                x1 = det.left()
                y1 = det.top()
                x2 = det.right()
                y2 = det.bottom()

                # TODO: 새로운 토픽에 이미지 저장
                print(x1, x2, y1, y2)

            except Exception as e:
                print(e)
                pass
