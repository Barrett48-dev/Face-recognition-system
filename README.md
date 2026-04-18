# Face Recognition System (Vision)

## Overview

This project implements a real-time face recognition application using Python, OpenCV, MediaPipe, face_recognition, and MySQL. It supports:

- user registration with face encoding storage into a database,
- face detection from a webcam feed,
- face recognition by comparing live captures against a known dataset.

## Key Modules

- `register_module.py`
  - Exposes `register_user(name, cap)` function to register a new user.
  - Displays live webcam feed and prompts user to press `s` to capture registration image.
  - Converts frame from BGR to RGB (required for face_recognition library).
  - Generates 128-dimensional face encoding using `face_recognition.face_encodings`.
  - Stores user name and encoding (as string) in MySQL `users` table.
  - Press `q` to cancel registration.
  - Closes window after registration completes.

- `FaceDetectionModule.py`
  - Uses MediaPipe Face Detection (`mp.solutions.face_detection`).
  - Detects faces in each frame and returns bounding boxes + confidence scores.
  - Draws rectangles and confidence percentage on the image.

- `recognition.py`
  - Initializes face detector with 70% confidence threshold.
  - Connects to MySQL database at startup and loads all registered users and their encodings.
  - Starts webcam capture and runs real-time face recognition loop.
  - For each detected face: crops region, generates encoding, and compares against all known users.
  - Uses `face_recognition.compare_faces` and `face_recognition.face_distance` to find best match.
  - Displays recognized name in **green** text (matched user) or **Unknown in red** (no match).
  - Press `r` key to register a new user (calls `register_module.register_user`; reloads user list after).
  - Press `q` key to quit application.
  - Releases camera and closes windows on exit.

## Database Schema (MySQL)

The DB `face_recognition_db` should include at least:

Table `users`

- `id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(...) NOT NULL
- `Encoding` TEXT NOT NULL

Each encoding is stored as a serialized list string (e.g. `[0.123, -0.012, ...]`).

## How It Works (Detailed)

1. **Startup** (in `recognition.py`)
   - Initialize MediaPipe-based face detector with 70% confidence threshold.
   - Connect to MySQL database and load all registered users.
   - For each user record, parse stored encoding string back into numpy array.
   - Store all names in `known_names` list and encodings in `known_encodings` list.
   - Display loaded user count in console.

2. **Registration Flow** (in `register_module.py`)
   - Function `register_user(name, cap)` called when user presses `r` during recognition.
   - Opens camera and displays live preview in "Register User" window.
   - Waits for user to press `s` to capture and register face.
   - When `s` pressed: converts frame from BGR to RGB format.
   - Generates 128-dimensional face encoding using `face_recognition.face_encodings`.
   - If face detected: converts encoding to string and inserts into MySQL `users` table.
   - Confirms successful registration or prompts retry if no face detected.
   - Press `q` to cancel registration at any time.

3. **Face Detection** (in `FaceDetectionModule.py`)
   - Each frame converted to RGB and processed by MediaPipe Face Detection model.
   - Returns bounding boxes (normalized coordinates) and confidence scores for each detected face.
   - Bounding box coordinates translated from normalized (0-1) to pixel values.
   - Rectangles and confidence percentages drawn on frame for visualization.

4. **Real-Time Recognition** (in `recognition.py` main loop)
   - Capture frame from webcam continuously.
   - Detect all faces using `FaceDetectionModule.Face_Module.findFaces()`.
   - For each detected face:
     - Crop face region from image.
     - Convert to RGB format (critical for face_recognition library).
     - Generate 128-dimensional encoding using `face_recognition.face_encodings`.
     - Compare encoding against all known encodings using `face_recognition.compare_faces`.
     - Calculate distance to each known face using `face_recognition.face_distance`.
     - Find best match (smallest distance).
     - If match found: display name in **green**; otherwise display **"Unknown" in red**.
   - Display live video with labels.
   - Check for key presses (`r` = register, `q` = quit).
   - If `r` pressed: call registration function and reload user list from database.
   - If `q` pressed: exit loop, release camera, close all windows.

## Steps to Run

1. Install dependencies:

   ```bash
   python -m pip install opencv-python face-recognition mediapipe mysql-connector-python numpy
   ```

2. Ensure MySQL is running and database created:

   ```sql
   CREATE DATABASE face_recognition_db;
   CREATE TABLE users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     Encoding TEXT NOT NULL
   );
   ```

3. Update database credentials in both `recognition.py` and `register_module.py`:
   - Modify `host`, `user`, `password` to match your MySQL setup.

4. Run the recognition system:

   ```bash
   python recognition.py
   ```

5. **During Runtime:**
   - Press `r` to register a new user (live face detection required).
   - Press `q` to quit the application.

## Important Notes

- **Face Detection Sensitivity:** `face_recognition.face_encodings` performs best with clear frontal faces in good lighting. Ensure proper face positioning.
- **Registration:** One face is captured and saved per registration. If no face detected, try again with `s`.
- **Dynamic User Loading:** All registered users are loaded from database at startup. New users registered during runtime are immediately loaded into the recognition list.
- **Encoding Format:** Face encodings stored as string representation of numpy arrays in database for easy storage/retrieval.
- **Color Coding:** Recognized users display name in **green**; unrecognized faces show **"Unknown" in red**.

## Recommended Improvements

- Replace `eval()` on DB `Encoding` column with `ast.literal_eval()` for enhanced security.
- Save encodings as binary (pickle/numpy byte format) instead of plain text for more efficient storage.
- Add validation to ensure at least one face is captured during registration before allowing retry.
- Add a GUI overlay for user prompts instead of console input.
- Implement distance threshold parameter to control recognition sensitivity.
- Add Ctrl-C handler for graceful shutdown.
- Add logging for registration and recognition events.
- Cache encodings in memory to reduce database queries on every recognition loop.
# Face-recognition-system
