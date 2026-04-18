# Import libraries for video capture, face encoding generation, and database operations
import cv2
import face_recognition
import mysql.connector

# Function to register a new user by capturing their face and storing encoding in database
def register_user(name, cap):
    # Connect to MySQL database
    connection = mysql.connector.connect (
        host="localhost",
        user="root",
        password="",
        database="face_recognition_db"
    )
    
    cursor = connection.cursor()
    
    # Prompt user to capture registration image
    print(f"Registering user: {name}....")
    print(f"Press 's' to capture the image for {name} registration.")

    # Loop to capture registration image
    while True:
        # Read frame from webcam
        success, img = cap.read()
        if not success:
            continue
        
        # Display live video feed
        cv2.imshow("Register User", img)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        # 's' = save and register user
        if key == ord('s'):
            # Convert BGR to RGB format (required for face_recognition)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Generate 128-dimensional face encoding
            encodings = face_recognition.face_encodings(rgb)
            
            # If face detected and encoding generated
            if encodings:
                encoding = encodings[0]
                # Convert numpy array to string for database storage
                encoding_string = str(encoding.tolist())
            
                # Insert user name and encoding into database
                cursor.execute(
                    "INSERT INTO users (name, Encoding) VALUES (%s, %s)",
                    (name, encoding_string)
                )
                connection.commit()
            
                print(f"User {name} registered successfully!")
            else:
                print("No face detected. Please try again.")
            break
        
        # 'q' = cancel registration
        if key == ord('q'):
            print("Registration cancelled.")
            break
    
    # Close registration window
    cv2.destroyWindow("Register User")  
    