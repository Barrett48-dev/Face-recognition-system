import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Create window
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("800x600")

# Title
title = tk.Label(root, text="Face Recognition System", font=("Arial", 20))
title.pack(pady=10)

# Video frame label
video_label = tk.Label(root)
video_label.pack()

# OpenCV camera
cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL image
        img = Image.fromarray(frame)

        # Convert to Tkinter image
        imgtk = ImageTk.PhotoImage(image=img)

        # Show in label
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Repeat every 10 ms
    video_label.after(10, update_frame)

# Start camera loop
update_frame()

# Buttons
start_btn = tk.Button(root, text="Start Recognition", width=20)
start_btn.pack(pady=5)

register_btn = tk.Button(root, text="Register User", width=20)
register_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", width=20, command=root.quit)
exit_btn.pack(pady=5)

# Run app
root.mainloop()

# Release camera when closed
cap.release()
cv2.destroyAllWindows()