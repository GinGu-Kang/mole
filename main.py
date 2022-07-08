import cv2
import time
import mediapipe as mp
import numpy as np

class pose(object):



    
    def __init__(self):
        self.mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
        self.mpPose = mp.solutions.pose
        self.pose=self.mpPose.Pose()
        self.numCount=0
        self.fCount=False                                         
        self.jCount=True
        self.moleSwitch=True
        #2번째 두더지
        self.numCount2=0
        self.fCount2=False                                         
        self.jCount2=True
        self.moleSwitch2=True
        #두더지 사이즈
        self.moleY=300
        self.moleX=300
        self.src2 = cv2.imread('mole3.jpg')
        self.src2 = cv2.resize(self.src2, dsize=(self.moleX, self.moleY), interpolation=cv2.INTER_CUBIC)



    #팔각도 목표 달성값 그래프
    def angleGage(self,angle,outWidth,frame):
            #왼쪽 팔각도 게이지 그래프 출력
            print(angle)

            #팔의 최대각도 160도 최소각도 60도  측정된 팔의 각도에서 최소각도를 양변에 빼주고 현재각도에서 최소각도를 뺀값과 최대각도에서 최소각도를 빼준값을 나누면 목표 각도의 퍼센테이지 측정 가능
            jointPercent=(angle-60)/100
            if jointPercent<0:
                jointPercent=0
            elif jointPercent>1:
                jointPercent=1

            #막대그래프의 최대값 * 목표 각도의 퍼센테이지 = 현재 목표각도 달성 정도
            startX=100+(500-round(500 * jointPercent))
            if startX<100:
                startX=100
            
            cv2.rectangle(frame, (outWidth-30, 100), (outWidth,600), (0,0,255), 3)
            cv2.rectangle(frame, (outWidth-30, startX), (outWidth,600), (0,0,255), -1)
            cv2.putText(frame,str(round(100*jointPercent)),(outWidth-45,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            return frame


    #3점 각도 계산
    def calculate_angle(self,a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
            
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            if angle >180.0:
                angle = 360-angle
                
            return angle

    #두더지 출력
    def moleOut(self,moleSwitch,moleShape,frameX,frameY,frame):
        if moleSwitch:
            rows, cols, channels = moleShape #로고파일 픽셀값 저장

            roi = frame[frameY:rows+frameY,frameX:cols+frameX] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
            
            gray = cv2.cvtColor(self.src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
            ret, mask = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
            mask_inv = cv2.bitwise_not(mask)

            src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
            src2_fg = cv2.bitwise_and(self.src2,self.src2, mask = mask_inv) #로고에서만 연산
            dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
            
            frame[frameY:rows+frameY,frameX:cols+frameX] = dst #src1에 dst값 합성
        return frame
    


    def get_frame(self,frame):
         #한개의 프레임 마다 읽어오기
        frame=cv2.resize(frame, (800,600)) 
        frameX=round(200)-round(self.moleY*0.5)
        frameY=round(600/2)-round(self.moleX*0.5)

        frame=cv2.flip(frame,1)
        
        
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #oepn cv : bgr /mediapipe : rgb    filp()= 좌우반전
        results=self.pose.process(rgb)   
        try:
            #각도계산
            landmark = results.pose_landmarks.landmark
            LEFT_HIP = [landmark[self.mpPose.PoseLandmark.RIGHT_WRIST].x,landmark[self.mpPose.PoseLandmark.RIGHT_WRIST].y]
            LEFT_KNEE = [landmark[self.mpPose.PoseLandmark.RIGHT_ELBOW].x,landmark[self.mpPose.PoseLandmark.RIGHT_ELBOW].y]
            LEFT_ANKLE = [landmark[self.mpPose.PoseLandmark.RIGHT_SHOULDER].x,landmark[self.mpPose.PoseLandmark.RIGHT_SHOULDER].y]
            angle=round(self.calculate_angle(LEFT_HIP,LEFT_KNEE,LEFT_ANKLE))
            
            #팔각도 측정으로 두더지 출력 미출력 판단
            if angle>=160:
                moleSwitch=False
                if self.jCount:
                    self.jCount=False
                    self.numCount+=1
            elif angle<60:
                moleSwitch=True
                if not self.jCount:
                    self.jCount=True

            #오른쪽 손

            LIGHT_HIP = [landmark[self.mpPose.PoseLandmark.LEFT_WRIST].x,landmark[self.mpPose.PoseLandmark.LEFT_WRIST].y]
            LIGHT_KNEE = [landmark[self.mpPose.PoseLandmark.LEFT_ELBOW].x,landmark[self.mpPose.PoseLandmark.LEFT_ELBOW].y]
            LIGHT_ANKLE = [landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER].x,landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER].y]
            angle2=round(self.calculate_angle(LIGHT_HIP,LIGHT_KNEE,LIGHT_ANKLE))
          
            
            #팔각도 측정으로 두더지 출력 미출력 판단
            if angle2>=160:
                moleSwitch2=False
                if self.jCount2:
                    self.jCount2=False
                    self.numCount2+=1
            elif angle2<60:
                moleSwitch2=True
                if not self.jCount2:
                    self.jCount2=True

            
            



            #self.mpDraw.draw_landmarks(frame,results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)


        





            cv2.putText(frame,str("Num_count"),(70,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(frame,str(int(self.numCount)),(150,150),cv2.FONT_HERSHEY_SIMPLEX,3,(255,102,0),3)

            cv2.putText(frame,str('Num_count2'),(500,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(frame,str(int(self.numCount2)),(500,150),cv2.FONT_HERSHEY_SIMPLEX,3,(255,102,0),3)
            #두더지 화면 출력
            self.moleOut(moleSwitch,self.src2.shape,frameX,frameY,frame)
            frameX=round(600)-round(self.moleY*0.5)
            self.moleOut(moleSwitch2,self.src2.shape,frameX,frameY,frame)
            




            self.angleGage(angle,80,frame)
            self.angleGage(angle2,720,frame)

        except Exception:
            pass
        return frame







if __name__ == "__main__":
    camera = cv2.VideoCapture(1)
    pose = pose()

    while camera.isOpened():
        ret, frame = camera.read()
        frame  = pose.get_frame(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1)  == ord('q'):
            break
    cv2.release()
    cv2.destroyAllWindows()















