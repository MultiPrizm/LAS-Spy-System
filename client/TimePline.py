import datetime

class BreakTime():
    start_time = []
    finish_time = []

start_time = datetime.datetime.now().time()
break_time_list = []
break_time: BreakTime = None

def StartBreak():
    global break_time
    _time: str = datetime.datetime.now().time().strftime("%H:%M:%S")

    _time = _time.split(":")

    break_time = BreakTime()

    break_time.start_time = [_time[0], _time[1]]
    print("start")

def FinishBreak():
    global break_time
    _time: str = datetime.datetime.now().time().strftime("%H:%M:%S")

    _time = _time.split(":")

    break_time.finish_time = [_time[0], _time[1]]
    break_time_list.append(break_time)

    break_time = None
    print("finish")
