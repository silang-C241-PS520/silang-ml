import cv2
import math

def get_training_input():
    """Generate training input
        Output: word_frames_dict (dictionary). key = words, value = list of frames
    """
    VIDEO_URLS_PATH = "assets/Filtering_word_with_link_video.txt"
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
        for i in range(0, len(frames), math.ceil(len(frames)/30)):
            new_frames.append(frames[i])
        if len(new_frames) != 30:
            new_frames.append(frames[-1])
            
        word_frames_dict[word] = new_frames
        counter += 1
    return word_frames_dict

if __name__ == "__main__":
    word_frames = get_training_input()
    counter = 0
    for frame in word_frames['A']:
        cv2.imshow('frame', frame)
        print(counter)
        counter += 1
        key = cv2.waitKey(0)
        while key not in [ord('q'), ord('k')]:
            key = cv2.waitKey(0)
    

    
