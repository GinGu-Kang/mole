import cv2
import time
import mediapipe as mp
import numpy as np





def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle







cap=cv2.VideoCapture(1) # 비디오 불러오기

mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
mpPose = mp.solutions.pose
pose=mpPose.Pose()


prevTime=0

numCount=0
firstFoot=0
firstKnee=0
footPoint=0
moleY=300
moleX=300
src2 = cv2.imread('mole.png')
src2 = cv2.resize(src2, dsize=(moleX, moleY), interpolation=cv2.INTER_CUBIC)
moleSwitch=True





while cap.isOpened(): #한개의 프레임 마다 읽어오기
    ret, frame = cap.read()
    keypoints=[]
    
    frame=cv2.resize(frame, (800,600)) 
    frameX=round(800/2)-round(moleY*0.5)
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

        if angle>=160:
            moleSwitch=False
            if jCount:
                jCount=False
                numCount+=1
        elif angle<60:
            moleSwitch=True
            if not jCount:
                jCount=True



        mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)


    except Exception:
        pass

    currTime=time.time()
    fps =1/(currTime-prevTime)
    prevTime=currTime
    

    cv2.putText(frame,str('Num_count'),(70,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,str(int(numCount)),(70,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)
    #두더지 화면 출력
    if moleSwitch:
        rows, cols, channels = src2.shape #로고파일 픽셀값 저장

        roi = frame[frameY:rows+frameY,frameX:cols+frameX] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
        cv2.imshow("output", frame)
        
        gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
        ret, mask = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
        mask_inv = cv2.bitwise_not(mask)

        src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
        src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #로고에서만 연산
        dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
        
        frame[frameY:rows+frameY,frameX:cols+frameX] = dst #src1에 dst값 합성
        #끝
    cv2.imshow("output", frame)


    key=cv2.waitKey(1)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()