import cv2


def get_video_frames(path: str) -> list:
    video = cv2.VideoCapture(path)
    success, image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    seconds = 5
    multiplier = int(fps * seconds)
    frames = []
    while success:
        frame_id = int(round(video.get(1)))
        success, image = video.read()
        if frame_id % multiplier == 0 and image is not None:
            frames.append(image)
    return frames
