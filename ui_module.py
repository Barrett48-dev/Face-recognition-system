# Face Recognition UI built with customtkinter
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import face_recognition
import mysql.connector
import numpy as np
import FaceDetectionModule as fdm
import register_module as rm

# Set the GUI theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FaceRecognitionUI:
    def __init__(self):
        # Create main application window
        self.root = ctk.CTk()

        # Window title and size
        self.root.title("Face Recognition System")
        self.root.geometry("600x400")

        # Configure grid layout for left and right panels
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        # Left panel for controls and status
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        # Right panel for webcam preview or placeholder
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.grid(
            row=0,
            column=1,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        # App title label in left panel
        self.title_label = ctk.CTkLabel(
            self.left_frame,
            text="AI Face Recognition",
            font=("Arial", 26)
        )
        self.title_label.pack(pady=20)

        # Status label shows current app state
        self.status_label = ctk.CTkLabel(
            self.left_frame,
            text="System Ready",
            font=("Arial", 18),
            text_color="lightgreen"
        )
        self.status_label.pack(pady=10)

        # Button to simulate scanning a face
        self.test_button = ctk.CTkButton(
            self.left_frame,
            text="Scan Face",
            command=self.test_function
        )
        self.test_button.pack(pady=10)

        # Button to simulate user registration
        self.register_button = ctk.CTkButton(
            self.left_frame,
            text="Register User",
            command=self.register_user
        )
        self.register_button.pack(pady=10)

        # Exit button closes the app
        self.exit_button = ctk.CTkButton(
            self.left_frame,
            text="Exit",
            fg_color="red",
            hover_color="darkred",
            command=self.close_app
        )
        self.exit_button.pack(pady=20)

        # Placeholder text for right panel
        self.camera_label = ctk.CTkLabel(
            self.right_frame,
            text="Press 'Scan Face' to start",
            font=("Arial", 20)
        )
        self.camera_label.pack(expand=True)
        
        self.cap = cv2.VideoCapture(0)
        self.scanning = False # Flag to control scanning state

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_recognition_db"
        )
        self.cursor = self.connection.cursor()

        self.known_names = []
        self.known_encodings = []

        self.load_users()
        
    def test_function(self):
        if not self.scanning:
            self.scanning = True
            self.status_label.configure(
                text="Scanning for face...",
                text_color="yellow"
            )
            
            self.update_camera()  # Start updating camera feed
            print("Face Scanning Begins...")

    def register_user(self):
        success, frame = self.cap.read()
        
        if not success:
            self.status_label.configure(
                text = "Camera Error: Unable to capture image",
                text_color = "red"
            )
            return
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            face_locations
        )
        
        if len(face_encodings) == 0:
            self.status_label.configure(
                text="No face detected. Please try again.",
                text_color="red"
            )
            return
        
        dialog = ctk.CTkInputDialog(
            text="Enter the name of the user to register:",
            title="Register User"
        )
        name = dialog.get_input()
        
        if not name:
            return
        
        encoding = face_encodings[0] # Use the first detected face encoding for registration
        encoding_list = encoding.tolist() # Convert numpy array to list for storage
        
        sql = """INSERT INTO users (name, Encoding)
        VALUES (%s, %s)
        """
        
        values = (
            name,str(encoding_list)
        )
        
        self.cursor.execute(sql, values)
        self.connection.commit()
        self.load_users() # Refresh known users after registration
        
        self.status_label.configure(
            text = f"{name} Registered Successfully!",
            text_color = "lightgreen"
        )
        print(f"Registered user: {name}")

    def recognized_user(self):
        # Change status to recognized state
        self.status_label.configure(
            text="User Recognized!",
            text_color="lightgreen"
        )
        print("Simulating successful recognition...")
        
        
    def update_camera(self):
        
        if not self.scanning:
            return  # Skip updating camera if not scanning
        success, frame = self.cap.read()
        if success:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)

                name = "Unknown"
                color = "red"

                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]
                        color = "lightgreen"

                self.status_label.configure(text=f"User Detected: {name}", text_color=color)

            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=imgtk, text="")
            self.camera_label.image = imgtk

        self.root.after(10, self.update_camera)
    
    
    def load_users(self):
        self.cursor.execute("SELECT name, Encoding FROM users")
        rows = self.cursor.fetchall()
        self.known_names.clear()
        self.known_encodings.clear()

        for row in rows:
            name = row[0]
            encoding_string = row[1]
            encoding = np.array(eval(encoding_string))
            self.known_names.append(name)
            self.known_encodings.append(encoding)

        print("Loaded users from database:", self.known_names)

    def close_app(self):
        self.cap.release()  # Release the webcam resource
        self.root.destroy()  # Close the application window

    def run(self):
        # Start the GUI event loop
        self.root.mainloop()