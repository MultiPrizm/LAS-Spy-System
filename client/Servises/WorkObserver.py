import mediapipe as mp
from Servises.CameraManager import CameraServise
from Servises.TimePline import WorkTimeLineManager
from Servises.ConfigManager import DBManager
from asyncio import sleep
from Servises.FaceMesh import get_face_vector, select_user_from_face, process_frame

class WorkObserver():

    def __init__(self, camera: CameraServise, time_servise: WorkTimeLineManager, db: DBManager):
        self.__mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
        self.__camera: CameraServise = camera
        self.db = db

        self.time_servise = time_servise

        self.break_status: bool = False
        self.work_station_status: bool = False
        self.not_active_time: float = 0

    async def LaunchServise(self):

        users = self.db.getUsers()
        self.time_servise.set_active_worker(users[0][0])

        while True:

            ret, cadr = self.__camera.get_cadr()

            if ret:

                result = self.check_face(cadr)

                if result and self.break_status:
                    self.time_servise.finish_break()

                    self.break_status = False
                    
                elif not result and not self.break_status:
                    self.time_servise.start_break()

                    self.break_status = True
            
            await sleep(5)
    
    def check_face(self, cadr):

        results = self.__mp_face_detection.process(cadr)

        if results.detections:

            return True

        else:

            return False
