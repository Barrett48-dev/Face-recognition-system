# Face Recognition System (Vision)

## Overview

This project implements a real-time face recognition application using Python, OpenCV, MediaPipe, face_recognition, and MySQL. It also includes a custom Tkinter-based GUI frontend for live webcam preview, face detection status, and simple user interaction.

The system supports:

- user registration with face encoding storage into a database
- face detection and recognition from a webcam feed
- live UI status updates, including recognized or unknown face feedback
- a database-backed known-user loader for runtime recognition

## Key Modules

- `register_module.py`
  - Registers a new user by capturing a webcam image and storing a face encoding in MySQL.
  - Converts the frame from BGR to RGB for `face_recognition`.
  - Generates a 128-dimensional face encoding and inserts it into the `users` table.

- `FaceDetectionModule.py`
  - Detects faces using MediaPipe Face Detection.
  - Returns bounding boxes and confidence scores for faces in video frames.

- `recognition.py`
  - Loads registered users and their encodings from MySQL at startup.
  - Runs a real-time recognition loop using webcam input.
  - Uses `face_recognition.compare_faces` and `face_recognition.face_distance` to match detected faces.
  - Displays recognized names in green and unknown faces in red.
  - Supports `r` to register a new user and `q` to quit.

- `ui_module.py`
  - Provides a customtkinter GUI with left-side controls and a right-side webcam preview.
  - Connects to the same MySQL database and loads known users.
  - Updates the status label when faces are detected or recognized.
  - Includes buttons for scanning, registration mode, recognition simulation, and exit.

## Database Schema (MySQL)

The DB `face_recognition_db` should include at least:

Table `users`

- `id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL
- `Encoding` TEXT NOT NULL

Each encoding is stored as a serialized list string (for example: `[0.123, -0.012, ...]`).

## How It Works (Detailed)

1. **Startup**
   - Initialize the face recognition or UI module.
   - Connect to MySQL and load registered users with their stored encodings.
   - Parse saved encoding strings into numpy arrays.
   - Store user names and encodings in memory for live comparison.

2. **Registration Flow**
   - `register_module.py` captures a face image and stores a new encoding.
   - `ui_module.py` can switch the status label to registration mode.
   - Registered encodings can be reloaded and used immediately by the recognition loop.

3. **Face Detection**
   - Use MediaPipe to find face bounding boxes in each frame.
   - Convert frames to RGB before generating face encodings.
   - Draw face boxes and confidence percentages in the recognition view.

4. **Real-Time Recognition**
   - Capture each webcam frame and process detected faces.
   - Generate encodings and compare them against all known users.
   - Choose the smallest distance match to determine identity.
   - Update UI or console status with the recognition result.

## UI Details

- `ui_module.py` uses `customtkinter` for a dark-themed interface.
- It displays a live webcam feed on the right side of the window.
- A left panel contains controls for scanning, registration, recognition simulation, and exiting.
- Face detection results update the status label dynamically.

## Steps to Run

1. Install dependencies:

   ```bash
   python -m pip install opencv-python face-recognition mediapipe mysql-connector-python numpy customtkinter pillow
   ```

2. Ensure MySQL is running and the database is created:

   ```sql
   CREATE DATABASE face_recognition_db;
   CREATE TABLE users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     Encoding TEXT NOT NULL
   );
   ```

3. Update database credentials in `recognition.py`, `register_module.py`, and `ui_module.py` to match your MySQL setup.

4. Run the recognition system:

   ```bash
   python recognition.py
   ```

5. Run the UI module by launching a wrapper or runner that creates `FaceRecognitionUI()` and calls `run()`.

## Important Notes

- Face detection works best with clear, frontal faces and good lighting.
- Registration saves one face encoding per user and requires a valid face in the frame.
- `ui_module.py` loads known users from the database and compares live webcam frames against them.
- The current UI logic parses database encodings with `eval()`; replacing it with `ast.literal_eval()` is recommended for security.
- Recognized names appear in green while unknown faces are shown in red.

## Recommended Improvements

- Replace `eval()` in `ui_module.py` with `ast.literal_eval()` for safer decoding.
- Store encodings as binary (pickle or numpy bytes) instead of plain text for reduced storage and faster parsing.
- Add a direct main launcher to `ui_module.py` to start the GUI from the command line.
- Add better error handling for failed database connections.
- Add logging for registration, detection, and recognition events.
- Add support for training and recognition threshold tuning.
- Add a dedicated GUI registration flow instead of simulated buttons.
# Face-recognition-system

