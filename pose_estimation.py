import cv2
import mediapipe as mp
import numpy as np
import time
#from camera import VideoCamera

class PoseEstimation():
    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        # Curl counter variables
        self.count = 0
        self.check_num = 0
        

        self.RIGHT_ELBOW_angle_check_num = 0
        self.RIGHT_ELBOW_angle_count = 0
        

        self.LEFT_KNEE_angle_check_num = 0
        self.LEFT_KNEE_angle_count = 0

        self.RIGHT_KNEE_angle_check_num = 0
        self.RIGHT_KNEE_angle_count = 0

        #left_elbow, right_elbow, left_knee, right_knee 카운드 여부
        self.is_exercise_list = [False,False,False,False] 
        self.vt_time = 0 
        self.star_time = 0
        self.time_resutl = 0

        self.pose_landmarks = None
        
    def calculate_angle(self,a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle
    


    def get_frame(self,frame):
        image = None
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #image = cv2.flip(image, 1) #좌우반전
            image.flags.writeable = False  
            
            # Make detection
            results = pose.process(image)
            self.pose_landmarks = results.pose_landmarks
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            
            # Extract landmarks
            try:
                
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates #좌우반전 되어 ex)왼쪽 팔 좌표를 찾아 오른쪽 팔로 출력
                RIGHT_SHOULDER = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                RIGHT_ELBOW = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                RIGHT_WRIST = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                LEFT_SHOULDER = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                LEFT_ELBOW = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                LEFT_WRIST = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                LEFT_HIP = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                LEFT_KNEE = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                LEFT_ANKLE = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                RIGHT_HIP = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                RIGHT_KNEE = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                RIGHT_ANKLE = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                # Calculate angle
                RIGHT_ELBOW_angle = self.calculate_angle(RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)  
                LEFT_ELBOW_angle = self.calculate_angle(LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)    
                RIGHT_KNEE_angle = self.calculate_angle(RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE)   
                LEFT_KNEE_angle = self.calculate_angle(LEFT_HIP, LEFT_KNEE, LEFT_ANKLE)  

                print("RIGHT_ELBOW_ANGLE: ",RIGHT_ELBOW_angle)

                #left_elbow, right_elbow, left_knee, right_knee 카운드 여부
                self.is_exercise_list = [False,False,False,False] 
                if LEFT_ELBOW_angle <= 60 :
                    self.check_num = 1

                if LEFT_ELBOW_angle >= 120 and self.check_num == 1:
                    self.count += 1
                    self.check_num = 0
                    #left_elbow 카운트됨
                    self.is_exercise_list[0] = True


                if RIGHT_ELBOW_angle <= 60 :
                    self.RIGHT_ELBOW_angle_check_num = 1

                if RIGHT_ELBOW_angle >= 120 and self.RIGHT_ELBOW_angle_check_num == 1:
                    self.RIGHT_ELBOW_angle_count += 1
                    self.RIGHT_ELBOW_angle_check_num = 0
                    #right_elbow 카운트됨
                    self.is_exercise_list[1] = True 

                if LEFT_KNEE_angle <= 90 :
                    self.LEFT_KNEE_angle_check_num = 1

                if LEFT_KNEE_angle >= 130 and self.LEFT_KNEE_angle_check_num == 1:
                    self.LEFT_KNEE_angle_count += 1
                    self.LEFT_KNEE_angle_check_num = 0
                    #left_knee 카운트됨
                    self.is_exercise_list[2] = True

                if RIGHT_KNEE_angle  <= 90 :
                    self.RIGHT_KNEE_angle_check_num = 1

                if RIGHT_KNEE_angle  >= 130 and self.RIGHT_KNEE_angle_check_num == 1:
                    self.RIGHT_KNEE_angle_count += 1
                    self.RIGHT_KNEE_angle_check_num = 0
                    #left_knee 카운트됨
                    self.is_exercise_list[2] = True
                    
                if self.count == 1 and self.vt_time == 0:
                    self.star_time = time.time()
                    self.vt_time += 1

                if self.count >= 1:
                    self.time_resutl = int(time.time() - self.star_time)


                # Visualize angle
                
            except Exception as e:
                pass
        
            # Render detections
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
        return image

if __name__ == "__main__":
    camera = cv2.VideoCapture(1)

    pose = PoseEstimation()

    while True:
        frame  = camera.get_frame()
        frame  = pose.get_frame(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1)  == ord('q'):
            break
    
    cv2.destroyAllWindows()
