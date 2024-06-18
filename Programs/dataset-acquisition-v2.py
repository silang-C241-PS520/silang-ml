import numpy as np
import cv2
import datetime
import queue
from threading import Thread
import time

# global variables
stop_thread = False             # controls thread execution


def start_capture_thread(cap, queue):
    global stop_thread

    # continuously read fames from the camera
    while True:
        _, img = cap.read()
        queue.put(img)

        if (stop_thread):
            break


def capture_videos(cap, frames_queue):
    global stop_thread

    video_count = 1
    while not stop_thread:
        # 3-second countdown
        for i in range(3, 0, -1):
            print(f"Recording video {video_count} in {i} seconds...")
            time.sleep(1)

        # Initialize video writer
        out = cv2.VideoWriter(f'output_{video_count}.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (640, 480))

        # Record 1-second video
        start_time = time.time()
        while time.time() - start_time < 1:
            if frames_queue.empty():
                continue

            img = frames_queue.get()
            if img is not None:
                out.write(img)

        out.release()
        print(f"Video {video_count} captured.")
        video_count += 1


def main():
    global stop_thread

    # create display window
    cv2.namedWindow("webcam", cv2.WINDOW_NORMAL)

    # initialize webcam capture object
    cap = cv2.VideoCapture(1)
    #cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    # retrieve properties of the capture object
    cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps = cap.get(cv2.CAP_PROP_FPS)
    print('* Capture width:', cap_width)
    print('* Capture height:', cap_height)
    print('* Capture FPS:', cap_fps)

    # create a queue
    frames_queue = queue.Queue(maxsize=0)

    # start the capture thread: reads frames from the camera (non-stop) and stores the result in img
    thread = Thread(target=start_capture_thread, args=(cap, frames_queue,), daemon=True) # a deamon thread is killed when the application exits
    thread.start()

    # start the video capture thread
    capture_thread = Thread(target=capture_videos, args=(cap, frames_queue,), daemon=True)
    capture_thread.start()

    # initialize time and frame count variables
    last_time = datetime.datetime.now()
    frames = 0
    cur_fps = 0

    while (True):
        if (frames_queue.empty()):
            continue

        # blocks until the entire frame is read
        frames += 1

        # measure runtime: current_time - last_time
        delta_time = datetime.datetime.now() - last_time
        elapsed_time = delta_time.total_seconds()

        # compute fps but avoid division by zero
        if (elapsed_time != 0):
            cur_fps = np.around(frames / elapsed_time, 1)

        # retrieve an image from the queue
        img = frames_queue.get()

        # TODO: process the image here if needed

        # draw FPS text and display image
        if (img is not None):
            cv2.putText(img, 'FPS: ' + str(cur_fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("webcam", img)

        # wait 1ms for ESC to be pressed
        key = cv2.waitKey(1)
        if (key == 27):
            stop_thread = True
            break

    # release resources
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()