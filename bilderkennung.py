import time
import cv2
import numpy as np
import argparse
import sys
import os
from termcolor import cprint, colored
from colorama import just_fix_windows_console


# construct the argument parse and parse the arguments
def buildArgumentsParser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Bilderkennung - currently WIP", epilog="Created by: Yann-Luca Näher")
    ap.add_argument("-c", "--camera", help="camera index to use", type=int)
    ap.add_argument("--live-feed", help="display live feed from camera", action="store_true")
    ap.add_argument("-g", "--get-greenest-pixel", help="get greenest pixel from image", action="store_true")
    ap.add_argument("-y", "--get-yellowest-pixel", help="get yellowest pixel from image", action="store_true")
    ap.add_argument("-i", "--image", help="path to the image", default="", type=str)
    ap.add_argument("--get-cameras", help="get list of available cameras", action="store_true")
    return ap


def printHelp(ap: argparse.ArgumentParser):
    default_help = ap.format_help()
    custom_help = """\n\nExample usage: 
    Get list of available cameras:      python bilderkennung.py --get-cameras
    Get yellowest pixel from image:     python bilderkennung.py -i frame.jpg -y
    Get yellowest pixel from camera:    python bilderkennung.py -c 0 -y
    Get greenest pixel from image:      python bilderkennung.py -i frame.jpg -g
    Get greenest pixel from camera:     python bilderkennung.py -c 0 -g
    Display live feed from camera:      python bilderkennung.py -c 0 --live-feed
    
Advanced usage:
    Get live feed from camera and get yellowest pixel as fast as possible:  python bilderkennung.py -c 0 --live-feed -y
    Get live feed from camera and get greenest pixel as fast as possible:   python bilderkennung.py -c 0 --live-feed -g"""
    print(default_help + custom_help)


# Perform argument checks
def performChecks(ap: argparse.ArgumentParser, args: dict):
    # if there is not at least one argument supplied, print help and exit
    args_copy = args.copy()
    if not any(args.values()):
        printHelp(ap)
        raise Exception("No arguments supplied")
    elif args["get_cameras"]:
        args_copy.pop("get_cameras")
        if any(args_copy.values()):
            raise Exception("You can't use --get-cameras with other arguments")
    elif args["camera"] and args["image"]:
        raise Exception("You can't use -c and -i at the same time")
    elif args["camera"]:
        if args["get_yellowest_pixel"] and args["get_greenest_pixel"]:
            raise Exception("You can't use -g and -y at the same time")
        elif args["camera"] < 0:
            raise Exception("Invalid camera index")
    elif args["image"]:
        if args["get_yellowest_pixel"] and args["get_greenest_pixel"]:
            raise Exception("You can't use -g and -y at the same time")
        elif not os.path.isfile(args["image"]):
            raise Exception(f"File {args['image']} does not exist")
        elif args["image"] and not (args["get_yellowest_pixel"] or args["get_greenest_pixel"]):
            raise Exception("You can't use -i without -y or -g")


# Print critical error message and exit
def printCriticalError(message: str, exitCode: int = 1):
    printError(message)
    #raise Exception(message)
    sys.exit(exitCode)

# Print error message
def printError(message, start: str = ""):
    cprint(start + "ERROR: " + message, color="red", attrs=["bold"], file=sys.stderr)

# Print warning message
def printWarning(message, start: str = ""):
    cprint(start + "WARNING: " + message, color="yellow", attrs=["bold"])

# Print info message
def printInfo(message, start: str = ""):
    cprint(start + "INFO: " + message, color="cyan")

def millis():
    return int(round(time.time() * 1000))

old_time = millis()


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
    # detect the yellowest pixel in the image and return its y coordinate relative to the image y / 2
    y = 0
    # convert image to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define lower and upper bounds for the color yellow
    lower_yellow = np.array([22, 93, 0], dtype=np.uint8)
    upper_yellow = np.array([45, 255, 255], dtype=np.uint8)
    # create a mask for the color yellow
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # find the coordinates of the yellowest pixel
    y, x = np.unravel_index(mask.argmax(), mask.shape)
    # draw a circle around the yellowest pixel
    cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)
    return y


def get_greenest_pixel(frame):
    # detect the greenest pixel in the image and return its y coordinate relative to the image y / 2
    y = 0
    # convert image to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define lower and upper bounds for the color green
    lower_green = np.array([40, 40, 40], dtype=np.uint8)
    upper_green = np.array([70, 255, 255], dtype=np.uint8)
    # create a mask for the color green
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # find the coordinates of the greenest pixel
    y, x = np.unravel_index(mask.argmax(), mask.shape)
    # draw a circle around the greenest pixel
    cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)
    return y


def open_camera(camera_index):
    # open camera stream
    cap = cv2.VideoCapture(camera_index)
    return cap


def take_frame(cap):
    # take current frame from camera stream
    ret, frame = cap.read()
    # crop frame while using int x and int y as the middle coordinate to crop to 100px * 3px to have a narrow line to detect the yellowest pixel
    frame = crop_frame(frame)
    return frame

def crop_frame(frame):
    y = frame.shape[0] / 2
    frame = frame[int(y)-5:int(y)+5, 0:frame.shape[1]]
    return frame


def get_current_mouse_position(event, x, y, flags, param):
    # print current mouse position to console
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


def live_feed(cap):
    while True:
        _, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.setMouseCallback("frame", get_current_mouse_position)
        if cv2.waitKey(1) & 0xFF == ord("q") or cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1: # close window if q is pressed or window is closed
            break
    cap.release()
    cv2.destroyAllWindows()


def detect_blob(frame):
    x = 0
    y = 0
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # get edges of the image
    edges = cv2.Canny(gray_image, 100, 200)
    # get contours of the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # draw contours on the frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Edges", edges)
    cv2.imshow("Contours", frame)
    params = cv2.SimpleBlobDetector_Params() 

    params.filterByArea = True
    params.minArea = 500

    params.filterByCircularity = True 
    params.minCircularity = 0.5

    params.filterByConvexity = True
    params.minConvexity = 0.1

    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector_create(params) 

    keypoints = detector.detect(gray_image) 

    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        print(f"Blob center coordinates: {x}, {y}")
        cv2.putText(frame, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    blank = np.zeros((1, 1))  
    blobs = cv2.drawKeypoints(gray_image, keypoints, blank, (0, 0, 255), 
                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 

    cv2.imshow("Blobs", blobs)
    cv2.imshow("Image", frame)
    return x


def do_check(cap, get_pixel_function):
    cv2.imshow("frame", cap.read()[1])
    while True:
        old_time = millis()
        _, frame = cap.read()
        frame = take_frame(cap)
        frame = crop_frame(frame)
        get_pixel_function(frame)
        # open window to detect when user wants to close it
        if cv2.waitKey(1) & 0xFF == ord("q") or cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
            break
        print(f"Ellapsed time: {millis() - old_time}ms")
    cap.release()
    cv2.destroyAllWindows()


# main
def main() -> int:
    just_fix_windows_console()
    ap = buildArgumentsParser()
    args = buildArgumentsParser().parse_args()

    try:
        performChecks(ap, args.__dict__)
    except Exception as e:
        printCriticalError(str(e))

    if args.get_cameras:
        get_cameras()
        return 0
    elif args.camera >= 0:
        cap = open_camera(int(args.camera))
        if args.live_feed:
            if(args.get_yellowest_pixel):
                do_check(cap, get_yellowest_pixel)
            elif(args.get_greenest_pixel):
                do_check(cap, get_greenest_pixel)
            else:
                live_feed(cap)
        else:
            frame = take_frame(cap)
            cv2.imwrite("frame.jpg", frame)
            if args.get_yellowest_pixel:
                printInfo(get_yellowest_pixel(frame))
            else:
                printInfo(get_greenest_pixel(frame))
    elif args.image:
        frame = cv2.imread(args.image)
        frame = crop_frame(frame)
        cv2.imwrite("frame.jpg", frame)
        if(args.get_yellowest_pixel):
            printInfo("Yellowest pixel: " + get_yellowest_pixel(frame))
        elif(args.get_greenest_pixel):
            printInfo("Greenest pixel: " + get_greenest_pixel(frame))
        return 0
    else:
        printHelp(ap)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        printCriticalError("Interrupted by user.", 130)
