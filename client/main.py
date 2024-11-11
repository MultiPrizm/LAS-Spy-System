import cv2
import mediapipe as mp
import time, TimePline, ConfigManager

# Ініціалізація mediapipe для розпізнавання облич
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

DEBAG = False

# Відкрити з'єднання з веб-камерою
cap = cv2.VideoCapture(0)

# Перевірка, чи камера доступна
while not cap.isOpened():
    exit()
    time.sleep(5)


# Використовуємо mediapipe для розпізнавання обличчя
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()

        # Якщо кадр успішно зчитано
        if not ret:
            print("Не вдалося отримати кадр")
            break

        # Перетворюємо BGR зображення у RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Використовуємо mediapipe для пошуку облич
        results = face_detection.process(rgb_frame)

        # Якщо обличчя знайдено, намалювати рамки навколо них
        if results.detections:
            if DEBAG:
                for detection in results.detections:
                    # Малюємо рамки на обличчі
                    mp_drawing.draw_detection(frame, detection)
            
            if TimePline.break_time != None:
                TimePline.FinishBreak()
        elif TimePline.break_time == None:
            TimePline.StartBreak()
            

        # Відображаємо кадр з веб-камери
        if DEBAG:
            cv2.imshow('Веб-камера з розпізнаванням облич', frame)

        time.sleep(ConfigManager.config.update_delay)
        

# Звільняємо ресурс камери і закриваємо вікно
cap.release()
cv2.destroyAllWindows()
