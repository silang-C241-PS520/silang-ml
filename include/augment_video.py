import cv2
import numpy as np
import random

def flip_video(input_video_path, output_video_path, flip_code):
    """
    Flip a video horizontally or vertically using the warpAffine method.

    Args:
        input_video_path (str): Path to the input video file.
        output_video_path (str): Path to save the resized 
        flip_code (int): Flip code (0 for vertical flip, 1 for horizontal flip, -1 for both horizontal and vertical flip).

    Returns:
        list: List of flipped frames.
    """
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print('* Capture width:', width)
    print('* Capture height:', height)
    print('* Capture FPS:', fps)
    print('* Capture fourcc:', fourcc) 

    # Create a video writer for the output video
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame
        flipped_frame = flip_image(frame, flip_code)

        # Write the resized frame to the output video
        out.write(flipped_frame)


    # Release resources
    cap.release()
    out.release()

    return

def flip_image(image, flip_code):
    """
    Flip an image horizontally, vertically, or both using the warpAffine method.

    Args:
        image (numpy.ndarray): Input image.
        flip_code (int): Flip code (0 for vertical flip, 1 for horizontal flip, -1 for both horizontal and vertical flip).

    Returns:
        numpy.ndarray: Flipped image.
    """
    flip_x = flip_y = 1

    if flip_code == 0:
        flip_y = -1
    elif flip_code == 1:
        flip_x = -1
    elif flip_code == -1:
        flip_x = -1
        flip_y = -1
    else:
        raise ValueError("Invalid flip code. Use 0 for vertical flip, 1 for horizontal flip, or -1 for both horizontal and vertical flip.")

    translate_x = translate_y = 0

    if flip_x == -1:
        translate_x = image.shape[1]
    if flip_y == -1:
        translate_y = image.shape[0]

    M = np.float32([[flip_x, 0, translate_x], [0, flip_y, translate_y]])
    flipped_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return flipped_image

def image_resize(image, inter, width=1, height=1):
    """
    Resize an image to the specified width and height using the warpAffine method.

    Args:
        image (numpy.ndarray): Input image.
        inter (int, optional): Interpolation method for resizing.
        width (int, optional): Desired width of the resized image. If not provided, the aspect ratio is maintained.
        height (int, optional): Desired height of the resized image. If not provided, the aspect ratio is maintained.

    Returns:
        numpy.ndarray: Resized image.
    """

    assert image is not None, "file could not be read, check with os.path.exists()"

    if inter is None:
        if width <= 1 and height <= 1:
            inter = cv2.INTER_AREA
        elif width >= 1 and height >= 1:
            inter = cv2.INTER_CUBIC
        else:
            inter = cv2.INTER_LINEAR

    resized_image = cv2.resize(image,(width, height), interpolation = inter)

    return resized_image

def random_resize_video(input_video_path, output_video_path, inter, width_range=(0.5, 2.0), height_range=(0.5, 2.0)):
    """
    Resize a video randomly within the specified width and height ranges while maintaining the aspect ratio
    and adding black padding to the outside of the image.

    Args:
        input_video_path (str): Path to the input video file.
        output_video_path (str): Path to save the resized 
        inter (int): Interpolation method for resizing.
        width_range (tuple): Range for scaling the width (min, max).
        height_range (tuple): Range for scaling the height (min, max).

    Returns:
        list: List of resized frames with black padding.
    """
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Randomly select the resize dimensions within the specified ranges
    new_width = int(random.uniform(width_range[0], min(width_range[1], 1)) * width)
    new_height = int(random.uniform(height_range[0], min(height_range[1], 1)) * height)

    # Calculate the aspect ratio of the input video
    aspect_ratio = width / height
    new_aspect_ratio = new_width / new_height

    # Calculate the new dimensions while maintaining the aspect ratio
    if  aspect_ratio > new_aspect_ratio :
        new_width = int(new_height * new_aspect_ratio)
        new_height = height
    else:
        new_height = int(new_width / new_aspect_ratio)
        new_width = width

    # Create a video writer for the output video
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame while maintaining the aspect ratio
        resized_frame = image_resize(frame, inter, new_width, new_height)

        # Create a black background image with the original video size
        padded_frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate the top-left corner coordinates to center the resized frame
        y_offset = (height - new_height) // 2
        x_offset = (width - new_width) // 2

        # Copy the resized frame onto the black background image
        padded_frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_frame

        # Write the resized frame to the output video
        out.write(padded_frame)


    # Release resources
    cap.release()
    out.release()

    return
