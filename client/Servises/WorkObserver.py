import mediapipe as mp
from Servises.CameraManager import CameraServise
from asyncio import sleep

class WorkObserver():

    def __init__(self, camera: CameraServise):
        self.__mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
        self.__camera: CameraServise = camera

        self.break_status: bool = False
        self.work_station_status: bool = False
        self.not_active_time: float = 0

    async def LaunchServise(self):

        while True:

            ret, cadr = self.__camera.get_cadr()

            if ret:
                result = self.check_face(cadr)

                if result and self.break_status:
                    print("finish")

                    self.break_status = False
                    
                elif not result and not self.break_status:
                    print("start")

                    self.break_status = True
            
            await sleep(5)
    
    def check_face(self, cadr):

        results = self.__mp_face_detection.process(cadr)

        if results.detections:

            return True

        else:

            return False
