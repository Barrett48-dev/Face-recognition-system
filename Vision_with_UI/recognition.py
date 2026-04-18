import cv2
import face_recognition
import FaceDetectionModule as fdm # face detection file name
import mysql.connector
import numpy as np
import register_module as rm

# -------------------------
# Load Known Face (REGISTERED USER)
# -------------------------
known_image = face_recognition.load_image_file("benny.jpg")  
known_encoding = face_recognition.face_encodings(known_image)[0]

# -------------------------
# Initialize Detection
# -------------------------
detector = fdm.Face_Module(minDetectionCon=0.7)
cap = cv2.VideoCapture(0)

#Connect to MySQL Database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="face_recognition_db"
)
cursor = connection.cursor()

# fetch user data from database
cursor.execute("SELECT name, Encoding FROM users")
rows = cursor.fetchall()

known_names = []
known_encodings = []

for row in rows:
    name = row[0]
    encoding_string = row[1]
    
    #convert string back to numpy array
    encoding = np.array(eval(encoding_string))
    
    known_names.append(name)
    known_encodings.append(encoding)
    
print("Loaded users from database:", known_names)

def load_users():
    cursor.execute("SELECT name, Encoding FROM users")
    rows = cursor.fetchall()
    
    known_names = []
    known_encodings= []
    
    for row in rows:
        name = row[0]
        encoding_string = row[1]
        
        encoding = np.array(eval(encoding_string))
        
        known_names.append(name)
        known_encodings.append(encoding)
        
    print("Loaded users from database: ", known_names)
    return known_names, known_encodings


while True:
    success, img = cap.read()
    if not success:
        break

    # Step 1: Detect Faces
    img, bboxs = detector.findFaces(img)

    # Step 2: Loop Through Detected Faces
    for bbox, score in bboxs:
        x, y, w, h = bbox

        # Crop face
        face_crop = img[y:y+h, x:x+w]

        # Convert to RGB (VERY IMPORTANT)
        face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        # Step 3: Generate Encoding
        encodings = face_recognition.face_encodings(face_crop_rgb)

        if encodings:
            encoding = encodings[0]

            # Step 4: Compare With Known Encoding
            matches = face_recognition.compare_faces([known_encoding], encoding)
            face_distance = face_recognition.face_distance([known_encoding], encoding)

            if matches[0]:
                name = "Barrett"
                color = (0, 255, 0)
            else:
                name = "Unknown"
                color = (0, 0, 255)

            # Draw Name
            cv2.putText(img, name, (x, y-2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Recognition System", img)

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'):
        name = ("Enter new user name here: ")
        rm.register_user(name, img)
        known_names, known_encodings = load_users()
        
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()