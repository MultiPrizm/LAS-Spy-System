from Servises.CameraManager import CameraServise
import cv2, asyncio

class DebugServise():

    def __init__(self, camera: CameraServise) -> None:
        self.camera = camera
    
    async def LaunchServise(self):

        while True:

            ret, frame = self.camera.get_cadr()

            if not ret:
                await asyncio.sleep(0.1)

                continue

            cv2.imshow("Debag", frame)
            cv2.waitKey(30)

            await asyncio.sleep(0.1)
