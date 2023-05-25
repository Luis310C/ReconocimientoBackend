# # import numpy as np
# # import cv2
# # import Services.ServiceRecognize as sr
# #
# #
# #
# # recognizer = sr.ServiceRecognize()
# # recognizer.record_video(1)
# import asyncio
#
# # cpr = CryptographyService()
# # print(cpr.get_password_hash("mongodb://mongoadmin:arroyo3102003@5157er@localhost:80"))
# from Services.CyptographyService import CryptographyService
# from configparser import ConfigParser
# from Services.NotificationService import NotificationService, StandardMessage
#
#
# async def test():
#     std = StandardMessage()
#     std.number_phone = 31891752
#     std.body = "esto es una prueba con aiohttp"
#     await ns.start()
#     await ns.send_message(std)
#     await ns.stop()
#
#
# config = ConfigParser()
# config.read('config.ini')
# public_key = config["CONNECTIONS"]["public_key"]
# connection = config["CONNECTIONS"]["mongo_connection_string"]
#
# pws = CryptographyService(str(public_key))
# PWST = pws.symmetric_encrypt('dbncgmwkayvfbnho')
# print(PWST)
#
# email_config = config["EMAIL"]
# email_config["smtp_password"] = pws.symmetric_decrypt(email_config["smtp_password"])
#
# ns = NotificationService(email_config, config["WHATSAPP"])
# asyncio.get_event_loop().run_until_complete(test())
#
# # import smtplib
# # from email.mime.multipart import MIMEMultipart
# # from email.mime.text import MIMEText
# #
# # # Email configuration
# # smtp_host = 'smtp.office365.com'
# # smtp_port = 587
# # sender_email = 'luisacajabon310@outlook.com'
# # receiver_email = 'luisacajabon310@gmail.com'
# # password = 'dbncgmwkayvfbnho'
# #
# # # Create a multipart message
# # message = MIMEMultipart()
# # message['From'] = sender_email
# # message['To'] = receiver_email
# # message['Subject'] = 'Hello from Python'
# #
# # # Add the message body
# # message.attach(MIMEText('This is the body of the email.', 'plain'))
# #
# # # Create an SMTP session
# # session = smtplib.SMTP(smtp_host, smtp_port)
# #
# # # Start the session and encrypt the connection
# # session.starttls()
# #
# # # Login to your Gmail account
# # session.login(sender_email, password)
# #
# # # Send the email
# # session.sendmail(sender_email, receiver_email, message.as_string())
# #
# # # Terminate the session
# # session.quit()
#
#
# # #
# # # def read_image_from_file(file_path):
# # #     with open(file_path, 'rb') as f:
# # #         img_str = f.read()
# # #     return img_str
# # #
# # #
# # # # Load image as string from file/database
# # # img_str = read_image_from_file('0.jpg')
# # # sr.ServiceRecognize.train([img_str])
# # duration = 10
# # cap = cv2.VideoCapture(0)
# # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # output = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
# #
# # start_time = time.time()
# # end_time = start_time + duration
# #
# # while True:
# #     ret, frame = cap.read()  # Read a frame from the webcam
# #
# #     # Write the frame to the video file
# #     output.write(frame)
# #
# #     # Break the loop if the specified duration has elapsed
# #     if time.time() >= end_time:
# #         break
# #
# #     # Display the frame (optional)
# #     cv2.imshow('Video', frame)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
#
# # Release the resources
# # cap.release()
# # output.release()
# # cv2.destroyAllWindows()
#
#
# # def read_frame(video_path, frame_index):
# #     cap = cv2.VideoCapture(video_path)
# #
# #     # Set the frame index to the desired frame
# #     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
# #
# #     ret, frame = cap.read()  # Read the frame at the specified index
# #
# #     if ret:
# #         # Display or save the frame as an image
# #         cv2.imshow('Frame', frame)
# #         cv2.waitKey(0)
# #         cv2.destroyAllWindows()
# #     else:
# #         print(f"Frame {frame_index} not found.")
# #
# #     # Release the resources
# #     cap.release()
# #
# # video_path = 'output.avi'
# # frame_index = 100  # Index of the frame to read
# #
# # read_frame(video_path, frame_index)
import uvicorn


def start_local():
    uvicorn.run("App:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start_local()
