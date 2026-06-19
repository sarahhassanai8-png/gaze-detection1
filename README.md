# 👁️ Real-Time Eye Tracking & Attention Detection

A Computer Vision project that detects whether the user is looking at the center of the screen using **MediaPipe Face Mesh** and **OpenCV**.

If the user looks away from the center for a specified number of consecutive frames, the system displays a visual warning and plays an alert sound.

---

# 📖 Project Description

This project captures live video from a webcam and tracks both eyes using MediaPipe's Face Mesh.

The iris position is compared with the center of each eye to determine whether the user is looking at the screen.

If the gaze remains outside the predefined threshold for several frames, the system triggers an alert to help the user stay focused.

---

# ✨ Features

- 👁️ Real-time eye tracking
- 🎯 Gaze direction estimation
- ✅ Detects Center and Not Center gaze
- 🚨 Automatic visual alert
- 🔊 Sound alert using Windows Beep
- 📷 Live webcam processing
- ⚡ Fast and lightweight
- 📦 Uses MediaPipe Face Mesh with Iris landmarks

---

# 🛠 Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Winsound

---

# ⚙️ How It Works

### 1. Webcam Capture

The webcam continuously captures live video frames.

---

### 2. Face Detection

MediaPipe Face Mesh detects 468+ facial landmarks.

---

### 3. Iris Detection

The program extracts:

- Left Iris
- Right Iris

using MediaPipe refined landmarks.

---

### 4. Eye Center Calculation

For each eye, the program computes:

- Eye center
- Iris center

using the eye corners and eyelids.

---

### 5. Gaze Deviation

The horizontal (dx) and vertical (dy) deviation are calculated:

dx = (Iris Center X − Eye Center X) / Eye Width

dy = (Iris Center Y − Eye Center Y) / Eye Width

---

### 6. Gaze Classification

If

|dx| ≤ Threshold X

and

|dy| ≤ Threshold Y

→ Center

Otherwise

→ Not Center

---

### 7. Alert System

If the user keeps looking away for more than **20 consecutive frames**:

- Red transparent overlay
- "FOCUS!" message
- Beep sound

The alert automatically disappears once the user looks back to the center.

---

# 📂 Project Structure

```
EyeTracking/
│
├── main.py
├── README.md
├── requirements.txt
└── assets/
```

---

# 📦 Required Libraries

```
opencv-python
mediapipe
numpy
```

Install them using:

```bash
pip install opencv-python mediapipe numpy
```

---

# ▶️ Run the Project

```bash
python main.py
```

---

# 📌 Configuration

The following parameters can be adjusted:

```python
ALERT_FRAMES = 20
THRESH_X = 0.08
THRESH_Y = 0.05
```

Parameter | Description
----------|------------
ALERT_FRAMES | Number of consecutive frames before triggering alert
THRESH_X | Horizontal gaze sensitivity
THRESH_Y | Vertical gaze sensitivity

---

# 📊 Detection States

🟢 Center

- User is focused.
- Gaze remains inside the center area.

🟡 Not Center

- User looks away.
- Counter starts increasing.

🔴 Alert Triggered

- User remains distracted.
- Red overlay appears.
- "FOCUS!" message is displayed.
- Beep sound is played.

---

# 🧠 Algorithms Used

- Face Mesh Detection
- Iris Localization
- Eye Center Estimation
- Euclidean Geometry
- Gaze Deviation Calculation
- Threshold-Based Classification

---

# 💡 Applications

- Online Examination Monitoring
- Smart Learning Systems
- Student Attention Detection
- Productivity Monitoring
- Human Computer Interaction (HCI)
- Driver Attention Systems

---

# 🚀 Future Improvements

- Head Pose Estimation
- Blink Detection
- Drowsiness Detection
- Eye Movement Analytics
- Deep Learning Gaze Estimation
- Email Alert System
- Save Attention Statistics
- Dashboard for Session Analysis

---

# 👩‍💻 Author

**Sarah Hassan**

Computer Vision Project

---

# 📜 License

This project is developed for educational and research purposes.
