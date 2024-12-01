import cv2
import mediapipe as mp
import time, TimePline, ConfigManager, FaceMesh


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

DEBAG = False

cap = cv2.VideoCapture(0)

while not cap.isOpened():
    exit()
    time.sleep(5)


face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
test = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("Не вдалося отримати кадр")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_detection.process(rgb_frame)

    if results.detections:
        if DEBAG:
            for detection in results.detections:

                mp_drawing.draw_detection(frame, detection)
        
        if TimePline.break_time != None:
            TimePline.FinishBreak()
    elif TimePline.break_time == None:
        TimePline.StartBreak()

    if test != None:
        FaceMesh.face_comparator(test, face_mesh.process(rgb_frame))

    test = face_mesh.process(rgb_frame)

    if DEBAG:
        cv2.imshow('Веб-камера з розпізнаванням облич', frame)

    time.sleep(ConfigManager.config.update_delay)
        

cap.release()
cv2.destroyAllWindows()
