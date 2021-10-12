import cv2
import time
import mediapipe as mp

#cap=cv2.VideoCapture(0) # 비디오 불러오기

mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
mpPose = mp.solutions.pose
pose=mpPose.Pose()

width=400
heith=300
prevTime=0
fCount=False                                         
jCount=True
numCount=0
firstFoot=0
firstKnee=0
footPoint=0
frame = cv2.imread('V.png')
print(frame)
src2 = cv2.imread('mole.png')
src2 = cv2.resize(src2, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)



keypoints=[]

frame=cv2.resize(frame, (800,600)) 
frame=cv2.flip(frame,1)


rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #oepn cv : bgr /mediapipe : rgb    filp()= 좌우반전
results=pose.process(rgb)   

if results.pose_landmarks:
    landmark = results.pose_landmarks.landmark

    if (landmark[mpPose.PoseLandmark.NOSE].y>landmark[mpPose.PoseLandmark.LEFT_THUMB].y):
        fCount=True



    if (fCount):
        firstFoot=landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].y
        firstKnee=landmark[mpPose.PoseLandmark.RIGHT_KNEE].y
        
        fCount=False
    mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)

    footPoint=landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX].y
    print(landmark[mpPose.PoseLandmark.RIGHT_WRIST])
    # print(landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y)
    # print(landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y)
    try:
        jump=firstFoot/firstKnee-footPoint/firstKnee 
        if (jump>0.02):
            if(jCount):
                numCount+=1
                print(numCount)
                jCount=False
        elif(jump<0.02):
            jCount=True
    except Exception:
        pass

    currTime=time.time()
    fps =1/(currTime-prevTime)
    prevTime=currTime
    

    cv2.putText(frame,str('Num_count'),(70,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(frame,str(int(numCount)),(70,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)
    #추가
    
    rows, cols, channels = src2.shape #로고파일 픽셀값 저장
    roi = frame[width:rows+width,heith:cols+heith] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
    cv2.imshow("output", frame)
    
    gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
    ret, mask = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
    mask_inv = cv2.bitwise_not(mask)
    src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
    src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #로고에서만 연산
    dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
    
    frame[width:rows+width,heith:cols+heith] = dst #src1에 dst값 합성
    #끝
    cv2.imshow("output", frame)

    key=cv2.waitKey(0)



#cap.release()
cv2.destroyAllWindows()