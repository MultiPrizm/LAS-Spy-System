import asyncio

from Servises.WorkObserver import WorkObserver
from Servises.CameraManager import CameraServise
from Servises.DebugServise import DebugServise
from Servises.TimePline import WorkTimeLineManager
from Servises.ConfigManager import DBManager
from Servises.RequestManager import RequestsManager
from Servises.BrowserHistoryManager import BrowserHistoryManager

DEBUG = True

async def shut_up_system():
    
    
    db = DBManager()
    camera = CameraServise()
    request_manager = RequestsManager(db)

    time_servise = WorkTimeLineManager(request_manager)
    work_observer = WorkObserver(camera, time_servise, db)
    debug =  DebugServise(camera)
    bhm = BrowserHistoryManager(request_manager, time_servise)

    request_manager.load_users()

    if DEBUG:
        asyncio.Task(debug.LaunchServise())

    asyncio.Task(time_servise.LaunchServise())
    asyncio.Task(bhm.LaunchServise())
    await work_observer.LaunchServise()

if __name__ == "__main__":
    asyncio.run(shut_up_system())
    