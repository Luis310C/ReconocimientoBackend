import os
import time

from matplotlib import pyplot as plt

from models import UserModel, DpiModel
import cv2
import imutils as imutils
import numpy as np
from typing import List, Tuple, Final
from io import BytesIO


class ServiceRecognize:
    face_cascade: cv2.CascadeClassifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces: List[str] = []
    identifiers_faces: List[int] = []
    mrz_front_dpi: Final = 11
    mrz_back_dpi: Final = 5
    labels = []
    recognizer: cv2.face.LBPHFaceRecognizer_create = cv2.face.LBPHFaceRecognizer_create()

    # def __init__(self):
    #     face_cascade =
    #     recognizer =

    @staticmethod
    def __identify_all_faces(current_face, faces):
        faces.append(current_face)
        from matplotlib import pyplot as plt
        plt.imshow(current_face)
        plt.show()
        return False

    def __save_model(self, model_name: str):
        self.recognizer.save(model_name)
        self.recognizer.clear()

    def train_faces(self, temp_path: str, trainer_model_name: str):
        self.identifiers_faces = []
        self.labels = []
        video_capture = cv2.VideoCapture(temp_path)
        for i in range(40):
            _, frame = video_capture.read()
            if frame is None:
                break
            gray = self.preprocess_image(frame)
            self.__get_faces(gray, lambda face, array_images: self.__identify_all_faces(face, array_images),
                             self.identifiers_faces)
        self.recognizer.train(self.identifiers_faces, np.array(self.labels))
        self.__save_model(trainer_model_name)
        return trainer_model_name

    def __dpi_has_two_images(self, img):
        gray_image = self.preprocess_image(img)
        self.labels = []
        self.__get_faces(gray_image)
        success = len(self.labels) == 2
        return success

    def __validate_front(self, img) -> bool:
        success: bool = self.__dpi_has_two_images(img)
        copy_image = img.copy()
        quantity = self.__get_mrz(copy_image)
        success = success and quantity == self.mrz_front_dpi
        return success

    def __validate_back(self, img) -> bool:
        return self.__get_mrz(img) == self.mrz_back_dpi

    @staticmethod
    def __get_mrz(image) -> int:
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        image = imutils.resize(image, height=600)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
        thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
        thresh = cv2.erode(thresh, None, iterations=4)

        p = int(image.shape[1] * 0.05)
        thresh[:, 0:p] = 0
        thresh[:, image.shape[1] - p:] = 0
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # plt.imshow(thresh)
        # plt.show()
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        size = len(cnts)
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            crWidth = w / float(gray.shape[1])
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.03)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))
            roi = image[y:y + h, x:x + w].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return size

    def validate_dpi(self, front_dpi: bytes, back_dpi: bytes) -> bool:
        front_image = self.__bytes_to_img(front_dpi)
        success = self.__validate_front(front_image)
        back_image = self.__bytes_to_img(back_dpi)
        success = success and self.__validate_back(back_image)
        return success

    def find_match(self, name_target: str, bytes_image: bytes):
        success: bool = False
        local_recognizer: cv2.face.LBPHFaceRecognizer_create = cv2.face.LBPHFaceRecognizer_create()
        local_recognizer.read(name_target)
        img = self.__bytes_to_img(bytes_image)
        gray_image = self.preprocess_image(img)
        success = self.__get_faces(gray_image,
                                   lambda image, model: model.predict(image)[1] < 84, local_recognizer)
        return success

    @staticmethod
    def __bytes_to_img(bytes_image: bytes):
        numpy_arr = np.frombuffer(bytes_image, np.uint8)
        return cv2.imdecode(numpy_arr, cv2.IMREAD_COLOR)

    def record_video(self, max_frames: int):
        images_bytes: List[bytes] = []
        cap = cv2.VideoCapture(0)
        output_directory = "output_frames"
        os.makedirs(output_directory, exist_ok=True)
        frame_count = 0
        while frame_count < max_frames:
            ret, frame = cap.read()
            _, image_bytes = cv2.imencode(".jpg", frame)
            images_bytes.append(image_bytes.tobytes())
            frame_count += 1
        cap.release()
        self.train(images_bytes, 0, "recognizer")

    @staticmethod
    def preprocess_image(frame):
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray

    def __get_faces(self, gray_image, opt_function=lambda x, y: False, local_contex=None) -> bool:
        # labels = []
        opt_match: bool = False
        aux_frame = gray_image.copy()
        faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=12)
        for (x, y, w, h) in faces:
            select_face = aux_frame[y:y + h, x:x + w]
            select_face = cv2.resize(select_face, (150, 150), interpolation=cv2.INTER_CUBIC)
            opt_match = opt_function(select_face, local_contex)
            self.labels.append(0)
            if opt_match:
                break
        return opt_match

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
