import asyncio

from Servises.WorkObserver import WorkObserver
from Servises.CameraManager import CameraServise

async def shut_up_system():

    camera = CameraServise()

    work_observer = WorkObserver(camera)
    await work_observer.LaunchServise()

if __name__ == "__main__":
    asyncio.run(shut_up_system())