from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8
stop=1
def home(request):
    context = {}

    return render(request, "home.html", context)

class VideoCamera(object):
    def __init__(self):
        global stop
        self.video = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
    
        

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
        global stop

        try:
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:  # This is bad! replace it with proper handling
            print("에러입니다...")
        pass
        
def stop(request):

    global stop
    stop =0


    return render(request, "home.html")

def start(request):

    global stop
    stop =1


    return render(request, "home.html")
        
        
        


@gzip.gzip_page
def detectme(request):
    try:
        if stop!=0:
            print("종료")
            cam = VideoCamera()

            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass
