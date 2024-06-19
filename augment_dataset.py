import os
from include.augment_video import random_resize_video

# Define the path to your dataset
dataset_path = "data/recordings"

# Define the path to save the augmented dataset
augmented_dataset_path = "data/augmented_recordings"

# Define the augmentation parameters
inter = None
width_range = (0.7, 1.3)
height_range = (0.7, 1.3)
num_augmentations = 4

# Iterate over each word directory in the dataset
for word_dir in os.listdir(dataset_path):
    word_path = os.path.join(dataset_path, word_dir)
    
    # Create the corresponding word directory in the augmented dataset
    augmented_word_path = os.path.join(augmented_dataset_path, word_dir)
    os.makedirs(augmented_word_path, exist_ok=True)
    
    # Iterate over each video file in the word directory
    for video_file in os.listdir(word_path):
        input_video_path = os.path.join(word_path, video_file)
        
        # Create the augmented video files
        for i in range(num_augmentations):
            output_video_path = os.path.join(augmented_word_path, f"{os.path.splitext(video_file)[0]}_aug{i+1}.mp4")
            random_resize_video(input_video_path, output_video_path, inter, width_range, height_range)