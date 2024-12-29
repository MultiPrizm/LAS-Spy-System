import asyncio

from Servises.WorkObserver import WorkObserver
from Servises.CameraManager import CameraServise
from Servises.DebugServise import DebugServise

DEBUG = True

async def shut_up_system():

    camera = CameraServise()

    work_observer = WorkObserver(camera)
    debug =  DebugServise(camera)

    if DEBUG:
        asyncio.Task(debug.LaunchServise())

    await work_observer.LaunchServise()

if __name__ == "__main__":
    asyncio.run(shut_up_system())