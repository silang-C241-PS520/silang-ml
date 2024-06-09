from vidaug import augmentors as va

def augment_frames(frames):
    augmented_frames = []
    seq = va.Sequential([
        va.RandomTranslate(50, 50),
        va.RandomShear(0.2,0),
    ])
    for i in range(14):
        new_frames = seq(frames)
        augmented_frames.append(new_frames)
    return augmented_frames

