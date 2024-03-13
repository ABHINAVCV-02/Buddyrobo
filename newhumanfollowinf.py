import cv2
import mediapipe as mp
import time
import math
import serial
import numpy as np
#import pyfirmata

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#####arduino code#####

#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

senddata = ""


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def distancebetweenpoints(x1, y1, x2, y2):
    x3 = x2 - x1
    y3 = y2 - y1
    distanceofpoints = ((x3 ** 2) + (y3 ** 2)) ** (1 / 2)
    return distanceofpoints


cap = cv2.VideoCapture(0)

text = "Hello, OpenCV!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 255)  # White color in BGR
thickness = 2

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get the landmarks of interest
            landmark_points = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]]

            # Draw connections between specified landmarks
            connections = [(mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value),
                           (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_SHOULDER.value),
                           (mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_HIP.value),
                           (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.RIGHT_HIP.value)]
#drawing lines between the specified landmarks on the image to visualize the skeletal structure or pose estimation results
            for connection in connections:
                cv2.line(image,
                         (int(landmarks[connection[0]].x * image.shape[1]),
                          int(landmarks[connection[0]].y * image.shape[0])),
                         (int(landmarks[connection[1]].x * image.shape[1]),
                          int(landmarks[connection[1]].y * image.shape[0])),
                         (255, 0, 0), 2)
#These calculations convert the relative coordinates of the detected shoulder landmarks (normalized between 0 and 1) into absolute pixel coordinates based on the dimensions of the image.
            image_hight, image_width, _ = image.shape
            x_coodinate1 = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width)
            y_coodinate1 = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_hight)

            x_coodinate2 = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
            y_coodinate2 = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_hight)
#calculates the midpoint between the coordinates of the right and left shoulder landmarks
            x_coodinate = int((x_coodinate1 + x_coodinate2) / 2)

            y_coodinate = int((y_coodinate1 + y_coodinate2) / 2)

            pos = (x_coodinate, y_coodinate)

            # print("x:",x_coodinate," y:",y_coodinate)

            bodysize = int(distancebetweenpoints(x_coodinate1, y_coodinate1, x_coodinate2, y_coodinate2))
            if (70 < bodysize < 160):
                if (400 < x_coodinate < 640):
                    # print("right")
                    direction = "G"  # right tta

                elif (240 > x_coodinate > 0):
                    # print("left")
                    direction = "K"  # left tta

                else:
                    direction = "F"  # forward


            elif (bodysize > 300):
                if (400 < x_coodinate < 640):
                    # print("right")
                    direction = "M"  # right tta
                elif (240 > x_coodinate > 0):
                    # print("left")
                    direction = "N"  # left tta

                else:
                    direction = "B"  # backward tta

            else:
                if (240 > x_coodinate > 0):
                    # print("left")
                    direction = "L"  # left tta

                elif (400 < x_coodinate < 640):
                    # print("right")
                    direction = "R"  # right tta

                else:
                    # print("stop")
                    direction = "S"  # stop tta

            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

            # print(data)

            text_x = int((image_width - text_size[0]) / 2)
            text_y = int((image_hight + text_size[1]) / 2)

            cv2.circle(image, (pos), 10, (0, 255, 0), 2)

            # Draw specified landmarks
            for point in landmark_points:
                cv2.circle(image,
                           (int(point.x * image.shape[1]), int(point.y * image.shape[0])),
                           5, (0, 255, 0), -1)

            cv2.putText(image, str(direction), (20, 460), font, font_scale, font_color, thickness)

            write_read(direction)



        except:
            pass

        cv2.imshow('jyothide robot', image)  # raspberry pi use cheyyumbo display ill verathirikkan eeh line of code comment cheytholo (add #)....

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
