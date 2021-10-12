import cv2
import time
import mediapipe as mp
import numpy as np


#팔각도 목표 달성값 그래프
def angleGage(angle,outWidth):
            #왼쪽 팔각도 게이지 그래프 출력

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


#3점 각도 계산
def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle

#두더지 출력
def moleOut(moleSwitch,moleShape,frameX,frameY,frame):
    if moleSwitch:
        rows, cols, channels = moleShape #로고파일 픽셀값 저장

        roi = frame[frameY:rows+frameY,frameX:cols+frameX] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
        cv2.imshow("output", frame)
        
        gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
        ret, mask = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
        mask_inv = cv2.bitwise_not(mask)

        src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
        src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #로고에서만 연산
        dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
        
        frame[frameY:rows+frameY,frameX:cols+frameX] = dst #src1에 dst값 합성
    return frame







cap=cv2.VideoCapture(1) # 비디오 불러오기

mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
mpPose = mp.solutions.pose
pose=mpPose.Pose()



numCount=0
fCount=False                                         
jCount=True
moleSwitch=True
#2번째 두더지
numCount2=0
fCount2=False                                         
jCount2=True
moleSwitch2=True
#두더지 사이즈
moleY=300
moleX=300
src2 = cv2.imread('mole3.jpg')
src2 = cv2.resize(src2, dsize=(moleX, moleY), interpolation=cv2.INTER_CUBIC)

cc=0






while cap.isOpened(): #한개의 프레임 마다 읽어오기
    ret, frame = cap.read()
    keypoints=[]
    
    frame=cv2.resize(frame, (800,600)) 
    frameX=round(200)-round(moleY*0.5)
    frameY=round(600/2)-round(moleX*0.5)

    frame=cv2.flip(frame,1)
    
    
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #oepn cv : bgr /mediapipe : rgb    filp()= 좌우반전
    results=pose.process(rgb)   
    try:
        #각도계산
        landmark = results.pose_landmarks.landmark
        LEFT_HIP = [landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,landmark[mpPose.PoseLandmark.RIGHT_WRIST].y]
        LEFT_KNEE = [landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y]
        LEFT_ANKLE = [landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y]
        angle=round(calculate_angle(LEFT_HIP,LEFT_KNEE,LEFT_ANKLE))
        
        #팔각도 측정으로 두더지 출력 미출력 판단
        if angle>=160:
            moleSwitch=False
            if jCount:
                jCount=False
                numCount+=1
        elif angle<60:
            moleSwitch=True
            if not jCount:
                jCount=True

        #오른쪽 손

        LIGHT_HIP = [landmark[mpPose.PoseLandmark.LEFT_WRIST].x,landmark[mpPose.PoseLandmark.LEFT_WRIST].y]
        LIGHT_KNEE = [landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,landmark[mpPose.PoseLandmark.LEFT_ELBOW].y]
        LIGHT_ANKLE = [landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y]
        angle2=round(calculate_angle(LIGHT_HIP,LIGHT_KNEE,LIGHT_ANKLE))
        
        #팔각도 측정으로 두더지 출력 미출력 판단
        if angle2>=160:
            moleSwitch2=False
            if jCount2:
                jCount2=False
                numCount2+=1
        elif angle2<60:
            moleSwitch2=True
            if not jCount2:
                jCount2=True

        
        



        mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)


    





        cv2.putText(frame,str("Num_count"),(70,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(frame,str(int(numCount)),(150,150),cv2.FONT_HERSHEY_SIMPLEX,3,(255,102,0),3)

        cv2.putText(frame,str('Num_count2'),(500,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(frame,str(int(numCount2)),(500,150),cv2.FONT_HERSHEY_SIMPLEX,3,(255,102,0),3)
        #두더지 화면 출력
        moleOut(moleSwitch,src2.shape,frameX,frameY,frame)
        frameX=round(600)-round(moleY*0.5)
        moleOut(moleSwitch2,src2.shape,frameX,frameY,frame)
        




        angleGage(angle,80)
        angleGage(angle2,720)

    except Exception:
        pass
    cv2.imshow("output", frame)

    key=cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break


cap.release()
cv2.destroyAllWindows()