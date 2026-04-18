import cv2
import mediapipe as mp
import time


class handDetector():
    """Helper class wrapping MediaPipe Hands for hand detection and landmark extraction.

    Usage:
    detector = handDetector()
    img = detector.findHands(img)         # draws landmarks on the image
    lm_list = detector.findPosition(img)   # returns list of landmark coordinates
    """

    def __init__(self, mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize MediaPipe Hands with the provided parameters.

        Args:
            mode (bool): If True, treats input images as static (slower, but more accurate for single images).
            max_num_hands (int): Maximum number of hands to detect.
            min_detection_confidence (float): Minimum confidence for the detection to be considered successful.
            min_tracking_confidence (float): Minimum confidence for the landmark-tracking to be considered successful.
        """
        self.mode = mode
        self.maxHands = max_num_hands
        self.detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # MediaPipe hands solution reference; used for drawing and hand processing
        self.mpHands = mp.solutions.hands

        # Create the Hands object with the chosen parameters. model_complexity can be 0 or 1.
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=1,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        # Utility for drawing the detected landmarks and connections on images
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """Detect hands in an image and optionally draw landmarks.

        Args:
            img: BGR image (as provided by OpenCV).
            draw (bool): If True, draw landmarks and connections onto `img`.

        Returns:
            The same `img` with optional drawings applied.
        """
        # MediaPipe requires RGB images
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image to detect hands and landmarks
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw landmarks and connections (if requested)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw landmarks and the skeleton connections on the original BGR image
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        """Return a list of landmark positions for a specific detected hand.

        Args:
            img: BGR image used to convert normalized landmark coords to pixel coords.
            handNo (int): Index of the hand to read from `self.results.multi_hand_landmarks`.
                Note: if multiple hands are detected, 0 is the first detected hand.
            draw (bool): If True, draw a small circle at each landmark position on `img`.

        Returns:
            List of [id, x, y] for each landmark on the requested hand. Empty list if no hands detected.
        """

        Lmlist = []

        # Ensure we have detection results before attempting to index them
        if self.results.multi_hand_landmarks:
            # Guard: if handNo is out of range, this will raise an IndexError.
            myHand = self.results.multi_hand_landmarks[handNo]

            # Each landmark is normalized to [0.0, 1.0] for x and y; convert to pixel coords
            for id, ln in enumerate(myHand.landmark):
                # Debug: printing the raw landmark object can be noisy; keep commented unless needed
                # print(id, ln)
                h, w, c = img.shape
                cx, cy = int(ln.x * w), int(ln.y * h)
                Lmlist.append([id, cx, cy])
                if draw:
                    # Draw a filled circle at each landmark position for visualization
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return Lmlist
                
                
                
def main():
    """Simple demo loop: open webcam, detect hands, and display FPS.

    This function is intended as a quick smoke test to verify the detector works.
    """
    pTime = 0
    cTime = 0

    # Open default camera (0). Change index for other cameras.
    cap = cv2.VideoCapture(0)

    # Instantiate the hand detector with default settings
    detector = handDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        # Detect hands and draw landmarks
        img = detector.findHands(img)

        # Get landmark list for the first detected hand (if any)
        Lmlist = detector.findPosition(img)
        if len(Lmlist) != 0:
            # Example: print landmark with id 4 (usually the tip of the index finger)
            print(Lmlist[8])

        # Basic FPS calculation for display
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()