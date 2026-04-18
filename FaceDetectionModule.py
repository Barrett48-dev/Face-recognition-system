import cv2
import mediapipe as mp
import time

class Face_Module():
    def __init__(self, minDetectionCon = 0.5):
    
        self.minDetectionCon = minDetectionCon
    
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(results)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih),\
                        int(bboxC.width * iw), int(bboxC.height * ih)
                        
                bboxs.append([bbox, detection.score])
                
                cv2.rectangle(img, bbox,(168, 25, 150), 2)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                
        return img, bboxs

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    Detector = Face_Module()
    while True:
        success, img = cap.read()
        img, bboxs = Detector.findFaces(img)
        print(bboxs)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.imshow("image", img)
        cv2.waitKey(1) #/ change value > 10 to slow feed or set value < 10 to speed feed up
        #// This is a simple loop to display webcam feed with FPS. FPS is calculated by taking the inverse of the time difference between frames. The text is drawn on the image using OpenCV's putText function.


if __name__ == "__main__":
    main()