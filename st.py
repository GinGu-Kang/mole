import cv2
import threading
key=cv2.waitKey(1)
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)
        
        (self.grabbed, self.frame) = self.video.read()
        print(self.frame)
        threading.Thread(target=self.update, args=()).start()
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if key == ord('q') or key == ord('Q'):
                break


def gen(camera):
    while True:
        frame = camera.get_frame()
        cv2.imshow("output",frame)
        
        if key == ord('q') or key == ord('Q'):
            break

cap = VideoCamera()
gen(VideoCamera)

