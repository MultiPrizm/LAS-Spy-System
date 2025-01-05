from Servises.CameraManager import CameraServise
import mediapipe as mp
import cv2, asyncio

class DebugServise():

    def __init__(self, camera: CameraServise) -> None:
        self.camera = camera
        self.__mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    async def LaunchServise(self):

        while True:

            ret, frame = self.camera.get_cadr()

            results = self.__mp_face_detection.process(frame)

            if results.detections:
                for detection in results.detections:

                        self.mp_drawing.draw_detection(frame, detection)

            if not ret:
                await asyncio.sleep(0.1)

                continue

            cv2.imshow("Debag", frame)
            cv2.waitKey(30)

            await asyncio.sleep(0.1)
