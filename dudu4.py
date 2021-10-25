from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

stop=1

class VideoCamera(object):
    def __init__(self):
        global stop
        self.video = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        print("외않되")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        
        print("오긴오냐")

        return jpeg.tobytes()

    def update(self):
        while True:
            if stop==0:
                print("종료")
                break
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        cv2.imshow("output", frame)
    


        key=cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            break
            global stop

            try:
                yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except:  # This is bad! replace it with proper handling
                print("에러입니다...")
            pass

camera = VideoCamera()

gen(camera.get_frame)