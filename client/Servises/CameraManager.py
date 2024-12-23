from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB

class CameraServise():

    __camera: VideoCapture

    def __init__(self):
        
        self.__camera = VideoCapture(0)
    
    def get_cadr(self):
        ret, frame = self.__camera.read()

        if ret:

            return ret, cvtColor(frame, COLOR_BGR2RGB)
        else:
            return False
    