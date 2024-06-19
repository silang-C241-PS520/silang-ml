import cv2
import mediapipe as mp

mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

holistic = mp_holistic.Holistic(model_complexity=2, 
                                min_detection_confidence=0.5, 
                                min_tracking_confidence=0.5)

pose = mp_pose.Pose(model_complexity=2, 
                    min_detection_confidence=0.5, 
                    min_tracking_confidence=0.5)

hands = mp_hands.Hands(model_complexity=1,
                      min_detection_confidence=0.5, 
                      min_tracking_confidence=0.5)

def mediapipe_detection(image, model):
    results = model.process(image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return image, results