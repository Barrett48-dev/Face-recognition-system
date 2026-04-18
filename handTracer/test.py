import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, max_num_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_num_hands
        self.detection_con = detection_con
        self.track_con = track_con
        
        self.mpHands = mp.solutions.hands
        # FIXED: Use named parameters to avoid order issues, and add model_complexity
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=1,  # This was missing! Use 0 for faster but less accurate, 1 for more accurate
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mpDraw = mp.solutions.drawing_utils 

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
                
                
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()  # Now this will work!
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break
            
        img = detector.findHands(img)
        
        # fps calculation
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)
        
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    cap.release()
    cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()