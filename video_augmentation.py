from vidaug import augmentors as va

def augment_frames(frames):
    augmented_frames = []
    seq = va.Sequential([ 
        va.RandomShear(0.2, 0.2),
    ])
    for i in range(7):
        augmented_frames.append(seq(frames))
    return augmented_frames

def downsample(frames):
    len_frames = float(len(frames))
    seq = va.Sequential([ 
        va.Downsample(0.8),
    ])
    return seq(frames)

def upsample(frames):
    len_frames = float(len(frames))
    seq = va.Sequential([ 
        va.Upsample(1.2),
    ])
    return seq(frames)
    
