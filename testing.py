import tensorflow as tf
import cv2
import mediapipe_preprocessing
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np


dirs = os.listdir('assets/60_videos')
enc = LabelEncoder()
labels = enc.fit_transform(dirs)
labels = tf.keras.utils.to_categorical(labels)

def preprocess(frames):
    frames = np.array(frames)
    mediapipe_preprocessed_data = []
    for frame in frames:
        image, results = mediapipe_preprocessing.mediapipe_detection(frame, mediapipe_preprocessing.holistic)
        landmarks = []
        if results.right_hand_landmarks != None:
            for landmark in results.right_hand_landmarks.landmark:
                landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
        else:
            landmarks = landmarks + [0, 0, 0] * 21

        if results.left_hand_landmarks != None:
            for landmark in results.left_hand_landmarks.landmark:
                landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
        else:
            landmarks = landmarks + [0, 0, 0] * 21

        if results.pose_landmarks != None:
            nose_landmark = results.pose_landmarks.landmark[0]
            nose_landmarks = [nose_landmark.x, nose_landmark.y, nose_landmark.z] * 59
            for i in range(0, 17):
                landmark = results.pose_landmarks.landmark[i]
                landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
        else:
            nose_landmarks = [0,0,0] * 59
            landmarks = landmarks + [0, 0, 0] * 17
        mediapipe_preprocessed_data.append(np.array(landmarks) - np.array(nose_landmarks))
    return mediapipe_preprocessed_data



model = tf.keras.models.load_model('test_video8.h5')

# cap = cv2.VideoCapture(f'capstone/assets/videos/Makan.avi')
cap = cv2.VideoCapture(0)
frames = []

while cap.isOpened():

    # Read feed
    ret, frame = cap.read()
    frames.append(frame)

    # Show to screen
    
    frames = frames[-14:]
    if len(frames) == 14:
        res = preprocess(frames)
        res = np.array(res)
        res = np.expand_dims(res, axis=0)
        result = model.predict(res)[0]
        print(result.shape)
        i = np.argmax(result)
        mx = result[i]
        if mx > 0.9:
            print(enc.inverse_transform([i]))
    # Break gracefully
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

