# Import libraries for video, face recognition, database, and math operations
import cv2
import face_recognition
import FaceDetectionModule as fdm
import mysql.connector
import numpy as np
import register_module as rm
import ui_module as ui

# Initialize face detector with 70% confidence threshold
detector = fdm.Face_Module(minDetectionCon=0.7)

# Start webcam capture
cap = cv2.VideoCapture(0)

# Connect to MySQL database and get cursor
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="face_recognition_db"
)
cursor = connection.cursor()

# Load all registered users and their face encodings from database
cursor.execute("SELECT name, Encoding FROM users")
rows = cursor.fetchall()

known_names = []
known_encodings = []

# Convert stored encodings (strings) back to numpy arrays
for row in rows:
    name = row[0]
    encoding_string = row[1]
    encoding = np.array(eval(encoding_string))
    
    known_names.append(name)
    known_encodings.append(encoding)
    
print("Loaded users from database:", known_names)

# Function to refresh user list from database (called after registering new user)
def load_users():
    # Fetch updated user data
    cursor.execute("SELECT name, Encoding FROM users")
    rows = cursor.fetchall()
    
    known_names = []
    known_encodings= []
    
    # Convert string encodings to numpy arrays
    for row in rows:
        name = row[0]
        encoding_string = row[1]
        encoding = np.array(eval(encoding_string))
        
        known_names.append(name)
        known_encodings.append(encoding)
        
    print("Loaded users from database: ", known_names)
    return known_names, known_encodings

# Main recognition loop
while True:
    # Capture frame from webcam
    success, img = cap.read()
    if not success:
        break

    # Detect all faces in current frame
    img, bboxs = detector.findFaces(img)

    # Process each detected face
    for bbox, score in bboxs:
        x, y, w, h = bbox

        # Default: unknown person (red text)
        name = "Unknown"
        color = (0, 0, 255)

        # Extract face region from image
        face_crop = img[y:y+h, x:x+w]

        # Convert BGR to RGB (required for face_recognition library)
        face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        # Generate 128-dimensional face encoding
        encodings = face_recognition.face_encodings(face_crop_rgb)

        # If encoding was successfully generated
        if encodings:
            encoding = encodings[0]

            # Compare against all known encodings
            if len(known_encodings) > 0:
                # Returns True if face matches known encoding
                matches = face_recognition.compare_faces(known_encodings, encoding)
                # Returns distance values (lower = better match)
                face_distances = face_recognition.face_distance(known_encodings, encoding)

                # Find best matching known face
                best_match_index = np.argmin(face_distances)
                
                # If best match exceeds threshold, identify person (green text)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    color = (0, 255, 0)

        # Display recognized/unknown name above face
        cv2.putText(img, name, (x, y-2),
            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Show live recognition video
    cv2.imshow("Recognition System", img)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF
    
    # 'r' = register new user
    if key == ord('r'):
        name = input("Enter new user name here: ")
        rm.register_user(name, cap)
        known_names, known_encodings = load_users()
    
    # 'q' = quit application    
    if key == ord('q'):
        break

# Cleanup: release camera and close windows
cap.release()
cv2.destroyAllWindows()