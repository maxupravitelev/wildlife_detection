import cv2
from functions.imgToGif import imgToGif


from imutils.video import VideoStream
from functions.create_avi import Avi_writer
from functions.create_gif import Gif_writer

import os
import time

import argparse

import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 

args = vars(parser.parse_args())

mode = args["mode"]

background_image=None

# frame_width = 1296
# frame_height = 730

frame_width = 1280
frame_height = 720

camera = PiCamera()
camera.resolution = (frame_width, frame_height)
camera.framerate = 30
camera.awb_mode = 'fluorescent'
camera.awb_gains = 4
camera.exposure_mode = 'off'
cap = PiRGBArray(camera, size=(frame_width, frame_height))

# frame_width = 640
# frame_height = 480

#cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()

#ap=cv2.VideoCapture(0)

# cap = VideoStream(src=0).start()
# cap = VideoStream(src=0, resolution=(1296,730)).start()

# cap.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
# cap.set(17, 5000 ) 

time.sleep(2.0)

#ret, frame = cap.read()

#print("Frame resolution: " + str(frame.shape))

if mode == "avi":
    avi_writer = Avi_writer(frame)
else: 
# if mode == "gif":
    gif_writer = Gif_writer()

# capture frames from the camera
for image in camera.capture_continuous(cap, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    frame = image.array
    # show the frame
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(7,7),0)

    if gif_writer.background_image is None:
        gif_writer.background_image=gray_frame

    # print(movement_detected)

    delta=cv2.absdiff(gif_writer.background_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours == []: 
        movement_detected = False
    else:
        movement_detected = True

    if mode == "gif":

        # handle creating gifs from frames
        gif_writer.create_gif(movement_detected, frame)

    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    cap.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# while True:
#     last_frame = frame.copy()
#     ret, frame = cap.read()
#     #frame = cap.read()

#     if np.array_equal(last_frame,frame):
#         continue

#     gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     gray_frame=cv2.GaussianBlur(gray_frame,(7,7),0)

#     if gif_writer.background_image is None:
#         gif_writer.background_image=gray_frame

#     # print(movement_detected)

#     delta=cv2.absdiff(gif_writer.background_image,gray_frame)
#     threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
#     #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
#     (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if contours == []: 
#         movement_detected = False
#     else:
#         movement_detected = True

#     # if contours == []: 
#     #     movement_detected = False

#     # if contours is not None:
#     #     for contour in contours:
#     #         # print(cv2.contourArea(contour))
#     #         if cv2.contourArea(contour) >= 0:
#     #             movement_detected = True
#     #             # (x, y, w, h)=cv2.boundingRect(contour)
#     #             # cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
#     #             continue
#     #         else: 
#     #             movement_detected = False       
   
#     # print(movement_detected)

#     if mode == "avi":

#         avi_writer.create_avi(movement_detected, frame)
#         if contours != None:
#         # if movement_detected is True:
#             #print(background_image)
#             background_image = None
       

#     if mode == "gif":

#         # handle creating gifs from frames
#         gif_writer.create_gif(movement_detected, frame)

            
#     if mode == "debug":

#         # draw rectangle around movement area
#         for contour in contours:
#             if cv2.contourArea(contour) < 8000:
#                 continue
#             (x, y, w, h)=cv2.boundingRect(contour)
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)

#         # view color frame
#         cv2.imshow("video feed", frame)

#         # view gray_frame
#         cv2.imshow("gray_frame", gray_frame)

#         # view delta between background and gray_frame

#         cv2.imshow("delta", delta)
        
#         # view threshold of delta frame
#         cv2.imshow("threshold", threshold)
        


#     key=cv2.waitKey(1)

#     if key==ord('x'):
#         break

if mode == "avi":
    writer.release()

#cap.release()
cap.stop()
cv2.destroyAllWindows
