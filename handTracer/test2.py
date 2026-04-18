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
        # Use model_complexity=0 for speed
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=0,  # 0 = faster, 1 = more accurate
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mpDraw = mp.solutions.drawing_utils
        
        # For frame skipping
        self.frame_count = 0
        self.skip_frames = 2  # Process 1 out of every 3 frames

    def findHands(self, img, draw=True):
        self.frame_count += 1
        
        # Skip frames for speed
        if self.frame_count % self.skip_frames != 0:
            return img
            
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
    
    # Optional: Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = detector.findHands(img)
        
        # fps calculation
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, f"FPS: {int(fps)}", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)
        cv2.imshow("image", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()