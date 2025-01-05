import datetime, enum, asyncio
from Servises.RequestManager import RequestsManager

class WorkTimeLineManager():

    def __init__(self, request_manager: RequestsManager):
        self.__time_line_list: dict[str, WorkTimeLine] = {}
        self.active_worker: str = None
        self.break_status: bool = False

        self.request_manager = request_manager
    
    async def LaunchServise(self):

        while True:

            if self.active_worker:
                report = {
                    "worker": self.active_worker,
                    "start_time": self.__time_line_list[self.active_worker].start_time,
                    "time_points": self.__time_line_list[self.active_worker].time_line
                }

                self.request_manager.send_report(report)
            
            await asyncio.sleep(10)
    
    def set_active_worker(self, name: str):

        if self.active_worker:
            self.__time_line_list[self.active_worker].finish_job()

        if not name in self.__time_line_list and name != None:
            self.__time_line_list[name] = WorkTimeLine(name)

        self.active_worker = name
    
    def start_break(self):
        if self.active_worker:
            self.__time_line_list[self.active_worker].start_break()

            self.break_status = True
    
    def finish_break(self):
        if self.active_worker:
            self.__time_line_list[self.active_worker].finish_break()

            self.break_status = False

class EventType(enum.Enum):
    start_job = "start_job"
    finish_job = "finish_job"
    start_break = "start_break"
    finish_break = "finish_break"

class WorkTimeLine():

    def __init__(self, worker_name: str):
        
        self.time_line = []
        self.start_time = datetime.datetime.now().time().strftime("%H:%M:%S")

        self.time_line.append({
            "type": EventType.start_job.value,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def start_job(self):
        self.time_line.append({
            "type": EventType.start_job.value,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def finish_job(self):
        self.time_line.append({
            "type": EventType.finish_job.value,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def start_break(self):
        self.time_line.append({
            "type": EventType.start_break.value,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })

    def finish_break(self):
        self.time_line.append({
            "type": EventType.finish_break.value,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })