import datetime, enum

class WorkTimeLineManager():

    def __init__(self):
        self.__time_line_list: dict[str, WorkTimeLine] = {}
        self.active_worker: str
        self.break_status: bool = False
    
    def set_active_worker(self, name: str):

        self.__time_line_list[self.active_worker].finish_job()

        if not name in self.__time_line_list and name:
            self.__time_line_list[name] = WorkTimeLine(name)

        self.active_worker = name
    
    def start_break(self):
        self.__time_line_list[self.active_worker].start_break()

        self.break_status = True
    
    def finish_break(self):
        self.__time_line_list[self.active_worker].finish_break()

        self.break_status = False

class EventType(enum.Enum):
    start_job = 1
    finish_job = 2
    start_break = 3
    finish_break = 4

class WorkTimeLine():

    def __init__(self, worker_name: str):
        
        self.time_line = []
        self.start_time = datetime.datetime.now().time().strftime("%H:%M:%S")

        self.time_line.append({
            "type": EventType.start_job,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def start_job(self):
        self.time_line.append({
            "type": EventType.start_job,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def finish_job(self):
        self.time_line.append({
            "type": EventType.finish_job,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })
    
    def start_break(self):
        self.time_line.append({
            "type": EventType.start_break,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })

    def finish_break(self):
        self.time_line.append({
            "type": EventType.finish_break,
            "date": datetime.datetime.now().time().strftime("%H:%M:%S")
        })