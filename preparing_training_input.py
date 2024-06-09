import cv2
import math
import numpy as np
import tensorflow as tf

def get_training_input():
    """Generate training input
        Output: word_frames_dict (dictionary). key = words, value = list of frames
    """
    VIDEO_URLS_PATH = "assets/new_common_words.txt"
    f = open(VIDEO_URLS_PATH, 'r')
    word_url_dict = dict()
    for line in f:
        word, url = line.split()
        word = word.strip(':')
        word_url_dict[word] = url
    f.close()

    word_frames_dict = dict()
    counter = 1
    for word, url in word_url_dict.items():
        print(f"{counter}. {word}")
        vcap = cv2.VideoCapture(url)
        frames = []
        while(True):
            ret, frame = vcap.read()
            if frame is not None:
                frames.append(frame)
            else:
                vcap.release()
                cv2.destroyAllWindows()
                break

        new_frames = []
        if len(frames) < 30:
            new_frames = frames
        else:
            frame_counter = 0
            for i in range(0, len(frames), math.floor(len(frames)/30)):
                if frame_counter >= 30:
                    break
                new_frames.append(frames[i])
                frame_counter += 1
        if len(new_frames) != 30:
            new_frames.append(frames[-1])
        print(f"Num of frames: {len(new_frames)}")
        word_frames_dict[word] = new_frames
        counter += 1
    return word_frames_dict

if __name__ == "__main__":
    word_frames = get_training_input()

    for word, frames in word_frames.items():
        writer = cv2.VideoWriter(f'assets/videos/{word}.avi', cv2.VideoWriter_fourcc(*"MJPG"), 30, (1280, 720))
        for frame in frames:
            frame = cv2.resize(frame, (1280, 720), interpolation = cv2.INTER_LINEAR)
            writer.write(frame)
        writer.release()
        cv2.destroyAllWindows()
    

    
