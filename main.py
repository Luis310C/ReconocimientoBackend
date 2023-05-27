# import uvicorn
# import cv2
# from matplotlib import pyplot as plt
#
# # Cargamos los clasificadores requeridos
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
# img = cv2.imread('3.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# aux = gray.copy()
#
# faces = face_cascade.detectMultiScale(gray, 1.1, 12)
# numCaras = 0
# for (x, y, w, h) in faces:
#     select_face = aux[y:y + h, x:x + w]
#     plt.imshow(select_face)
#     plt.show()
#     numCaras += 1
#
#     # cv2.rectangle(img, (x, y), (x + w, y + h), (125, 255, 0), 2)
#     # numCaras = numCaras + 1
#     # Mostramos la imagen
#
# print("Número de caras detectadas: {}".format(numCaras))
from datetime import time, datetime
import uvicorn
def start_local():
    uvicorn.run("App:app", host="127.0.0.1", port=8000)



if __name__ == "__main__":
    start_local()
from imutils import paths
import numpy as np
import argparse
import time
import math
import imutils
import cv2
import matplotlib.pyplot as plt


    # plt.imshow(image)
    # plt.show()
    # check to see if the aspect ratio and coverage width are within<font></font>

# if __name__ == "__main__":
#     start_local()

# for c in cnts:
#     (x, y, w, h) = cv2.boundingRect(c)
#     ar = w / float(h)
#     crWidth = w / float(gray.shape[1])
#     pX = int((x + w) * 0.03)
#     pY = int((y + h) * 0.03)
#     (x, y) = (x - pX, y - pY)
#     (w, h) = (w + (pX * 2), h + (pY * 2))
#     roi = image[y:y + h, x:x + w].copy()
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)