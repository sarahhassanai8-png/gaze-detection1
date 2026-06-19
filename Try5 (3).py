import cv2
import mediapipe as mp
import numpy as np
import winsound  # for sound (Windows only)

# ================== CONFIG ==================
ALERT_FRAMES = 20
THRESH_X = 0.08   # horizontal sensitivity
THRESH_Y = 0.05   # vertical sensitivity (more sensitive)

# ================== INIT ==================
cap = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# ================== LANDMARKS ==================
LEFT_IRIS  = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

LEFT_EYE_CORNERS  = [33, 133]
RIGHT_EYE_CORNERS = [362, 263]

LEFT_EYE_LIDS     = [159, 145]
RIGHT_EYE_LIDS    = [386, 374]

# ================== STATE ==================
off_center_count = 0
alert_active = False


# ================== FUNCTION ==================
def get_eye_deviation(frame, landmarks, iris_idxs, corner_idxs, lid_idxs, w, h):

    iris_pts = np.array([
        (int(landmarks.landmark[i].x * w),
         int(landmarks.landmark[i].y * h))
        for i in iris_idxs
    ])

    (cx, cy), _ = cv2.minEnclosingCircle(iris_pts)
    cx, cy = int(cx), int(cy)

    x1 = int(landmarks.landmark[corner_idxs[0]].x * w)
    x2 = int(landmarks.landmark[corner_idxs[1]].x * w)

    y_top = landmarks.landmark[lid_idxs[0]].y * h
    y_bottom = landmarks.landmark[lid_idxs[1]].y * h

    x_center = (x1 + x2) // 2
    y_center = int((y_top + y_bottom) / 2)

    eye_width = abs(x2 - x1)

    dx = (cx - x_center) / eye_width
    dy = (cy - y_center) / eye_width

    # -------- Draw visuals --------
    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
    cv2.circle(frame, (x_center, y_center), 3, (255, 0, 0), -1)
    cv2.line(frame, (x_center, y_center), (cx, cy), (0, 255, 0), 2)

    # box visualization
    box_x = int(eye_width * THRESH_X)
    box_y = int(eye_width * THRESH_Y)

    cv2.rectangle(
        frame,
        (x_center - box_x, y_center - box_y),
        (x_center + box_x, y_center + box_y),
        (255, 0, 255),
        1
    )

    return dx, dy


# ================== MAIN LOOP ==================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    deviations = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            d1 = get_eye_deviation(
                frame, face_landmarks,
                LEFT_IRIS, LEFT_EYE_CORNERS, LEFT_EYE_LIDS,
                w, h
            )

            d2 = get_eye_deviation(
                frame, face_landmarks,
                RIGHT_IRIS, RIGHT_EYE_CORNERS, RIGHT_EYE_LIDS,
                w, h
            )

            deviations = [d1, d2]

    # -------- Decision --------
    gaze_status = "Center"

    if deviations:
        avg_dx = sum(d[0] for d in deviations) / len(deviations)
        avg_dy = sum(d[1] for d in deviations) / len(deviations)

        if abs(avg_dx) > THRESH_X or abs(avg_dy) > THRESH_Y:
            gaze_status = "Not Center"

        cv2.putText(frame, gaze_status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

    # -------- Alert logic --------
    if gaze_status == "Not Center":
        off_center_count += 1
    else:
        off_center_count = 0
        alert_active = False

    if off_center_count > ALERT_FRAMES:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        cv2.putText(frame, 'FOCUS!', (w // 3, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 4)

        # 🔊 Sound (only once per alert)
        if not alert_active:
            winsound.Beep(1000, 300)
            alert_active = True

    cv2.imshow("Eye Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()