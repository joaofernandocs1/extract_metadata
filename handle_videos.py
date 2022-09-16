from datetime import datetime
import cv2


def get_metadata(videoFile, videoPath=None):

    if videoPath is None:
        videoPath = ""

    nomePdv = videoFile.split("-", 1)[0]
    #print("nomePdv: ", nomePdv)

    data = videoFile.split("-", 3)[3].rstrip(".mp4")
    data_datetime = datetime.strptime(data, "%Y-%m-%d-%H-%M-%S")
    data_datetime = data_datetime.strftime('%Y-%m-%d %H:%M:%S')
    #print("data_datetime: ", data_datetime)

    video = cv2.VideoCapture(videoFile)
    duration = int(video.get(cv2.CAP_PROP_FRAME_COUNT)*1000/video.get(cv2.CAP_PROP_FPS)) # video duration in milliseconds
    #print("duration: ", duration)

    return nomePdv, data_datetime, duration


if __name__ == '__main__':

    pass