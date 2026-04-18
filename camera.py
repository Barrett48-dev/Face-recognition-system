import cv2

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    cv2.imshow("Press s to save", img)
    
    key = cv2.waitKey(1)
    
    if key == ord('s'):
        cv2.imwrite("benny3.jpg", img)
        print("image Saved")
        break
    
    if key == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()