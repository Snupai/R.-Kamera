import cv2
import numpy as np
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", help="camera index to use")
ap.add_argument("-i", "--image", help="path to the image")
ap.add_argument_group("Get cameras", "get list of available cameras")
ap.add_argument("--get-cameras", help="get list of available cameras", nargs="?", const=True)
args = vars(ap.parse_args())

# if there is not at least one argument supplied, print help and exit
if not any(args.values()):
    ap.print_help()
    exit()

def get_cameras():
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        print(f"Camera {index}: {cap.getBackendName()}")
        cap.release()
        index += 1
    


def get_yellowest_pixel(frame):
    # detect the yellowest pixel in the image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # get the coordinates of the yellowest pixel
    coordinates = np.argwhere(mask > 0)
    y, x = coordinates.mean(0)
    return (x, y)


def open_camera(camera_index):
    # open camera stream
    cap = cv2.VideoCapture(camera_index)
    return cap


def take_frame(cap):
    # take current frame from camera stream
    ret, frame = cap.read()
    # crop frame to 100x3 pixels
    frame = frame[0:100, 0:100]

    return frame





