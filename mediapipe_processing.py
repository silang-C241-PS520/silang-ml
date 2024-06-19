import os
import cv2
from include.mediapipe_preprocessing import mediapipe_detection, holistic, pose, hands

def process_videos(recordings_path, output_path):
    for word_folder in os.listdir(recordings_path):
        word_path = os.path.join(recordings_path, word_folder)
        if os.path.isdir(word_path):
            output_word_path = os.path.join(output_path, word_folder)
            os.makedirs(output_word_path, exist_ok=True)

            for video_file in os.listdir(word_path):
                if video_file.endswith(".mp4") or video_file.endswith(".avi"):
                    video_path = os.path.join(word_path, video_file)
                    output_file = os.path.splitext(video_file)[0] + ".txt"
                    output_file_path = os.path.join(output_word_path, output_file)

                    video_cap = cv2.VideoCapture(video_path)
                    with open(output_file_path, "w") as f:
                        frame_count = 0
                        while video_cap.isOpened() and frame_count < 30:
                            ret, frame = video_cap.read()
                            if not ret:
                                break

                            image, holistic_results = mediapipe_detection(frame, holistic)
                            # image, pose_results = mediapipe_detection(frame, pose)
                            # image, hands_results = mediapipe_detection(frame, hands)

                            pose_landmarks = holistic_results.pose_landmarks
                            left_hand_landmarks = holistic_results.left_hand_landmarks
                            right_hand_landmarks = holistic_results.right_hand_landmarks

                            landmark_data = []
                            if pose_landmarks:
                                base_x = pose_landmarks.landmark[0].x
                                base_y = pose_landmarks.landmark[0].y
                                base_z = pose_landmarks.landmark[0].z

                                for landmark in pose_landmarks.landmark:
                                    landmark_data.extend([landmark.x - base_x, landmark.y - base_y, landmark.z - base_z, landmark.visibility])
                            else:
                                landmark_data.extend([0] * (33 * 4))

                            if left_hand_landmarks:
                                base_x = left_hand_landmarks.landmark[0].x
                                base_y = left_hand_landmarks.landmark[0].y
                                base_z = left_hand_landmarks.landmark[0].z

                                for landmark in left_hand_landmarks.landmark:
                                    landmark_data.extend([landmark.x - base_x, landmark.y - base_y, landmark.z - base_z])
                            else:
                                landmark_data.extend([0] * (21 * 3))

                            if right_hand_landmarks:
                                base_x = right_hand_landmarks.landmark[0].x
                                base_y = right_hand_landmarks.landmark[0].y
                                base_z = right_hand_landmarks.landmark[0].z

                                for landmark in right_hand_landmarks.landmark:
                                    landmark_data.extend([landmark.x - base_x, landmark.y - base_y, landmark.z - base_z])
                            else:
                                landmark_data.extend([0] * (21 * 3))

                            landmark_data_str = ",".join(map(str, landmark_data))
                            f.write(landmark_data_str + "\n")

                            frame_count += 1

                    video_cap.release()

# Example usage
recordings_path = "data/augmented_recordings"
output_path = "data/text_data"
process_videos(recordings_path, output_path)