import cv2
import threading

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return self.image

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        cv2.imshow("output",frame)
        key=cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break


gen(VideoCamera)


