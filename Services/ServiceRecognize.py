import os
import time

import cv2
import imutils as imutils
import numpy as np
from typing import List


class ServiceRecognize:
    face_cascade: cv2.CascadeClassifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces: List[str] = []
    identifiers_faces: List[int] = []
    recognizer: cv2.face.LBPHFaceRecognizer_create = cv2.face.LBPHFaceRecognizer_create()

    # def __init__(self):
    #     face_cascade =
    #     recognizer =

    def get_faces(self, content: bytes):
        video_capture = cv2.VideoCapture(content)
        for i in range(30):
            ret, frame = video_capture.read()
            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aux_frame = frame.copy()

            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                                       minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                current_face = aux_frame[y:y + h, x:x + w]
                current_face = cv2.resize(current_face, (150, 150), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite("face_{}.jpg".format(i), current_face)
                self.identifiers_faces.append(current_face)
        self.recognizer.train(self.identifiers_faces, np.array([0 for i in range(1)]))

    def find_match(self, name_target: str, frame):
        self.recognizerface_recognizer.read(f'{name_target}.yml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = gray.copy()
        faces = self.recognizer.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            select_face = aux_frame[y:y + h, x:x + w]
            select_face = cv2.resize(select_face, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = self.recognizer.predict(select_face)
            if result[1] < 70:
                print(" {} is: {}".format(name_target, result))

    def record_video(self, duration: int):
        images_bytes: List[bytes] = []
        cap = cv2.VideoCapture(0)

        output_directory = "output_frames"
        os.makedirs(output_directory, exist_ok=True)

        frame_count = 0

        while frame_count < 30:
            ret, frame = cap.read()
            _, image_bytes = cv2.imencode(".jpg", frame)
            images_bytes.append(image_bytes.tobytes())
            frame_count += 1
        cap.release()
        self.train(images_bytes)

    def train_image(self, data: bytes, faces: List[str]):
        numpy_arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(numpy_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_rects = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12, minSize=(30, 30))
        for (x, y, w, h) in face_rects:
            face = gray[y:y + h, x:x + w]
            faces.append(face)

    def train(self, data: List[bytes], i: int, name: str = "recognizer"):
        faces = []
        for i, img in enumerate(data):
            self.train_image(img, i, faces)
        self.recognizer.train(faces, np.array([i]))
        self.recognizer.save(f'{name}.yml')

        # cv2.imshow('img', gray)
        # cv2.waitKey(0)

        # faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # if len(faces) == 1:
        #     (x, y, w, h) = faces[0]
        #     face = gray[y:y + h, x:x + w]
        #     # self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        #     self.recognizer.train([face], labels=[1])
        #     self.recognizer.save('face_recognizer.yml')

        # cv2.destroyAllWindows()
