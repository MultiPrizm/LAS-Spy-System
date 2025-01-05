from django.shortcuts import render
from authorization.views import auth_decorator
from django.http import HttpResponse
from spy_app.models import DailyWorkReport, Worker, BrowserHistoryItem
from django.utils.timezone import localdate, localtime
import json
from datetime import datetime


@auth_decorator
def send_work_report(request):
    client_report = request.headers.get("Report")
    
    try:
        client_report = json.loads(client_report)
    except json.JSONDecodeError:
        return HttpResponse(status = 403)
    
    worker = Worker.objects.filter(id = client_report["worker"], station = request.user["station"]).first()

    if worker is None:
        return HttpResponse(status = 404)
    
    report = DailyWorkReport.objects.filter(worker = worker, date = localdate()).first()

    start_time = datetime.strptime(client_report["start_time"], '%H:%M:%S').time()

    break_time = [0, 0, 0]
    start_break_time = None

    break_info_list = ""
    break_info = ""

    def calc_break_time(break_time: list, finish_time: str, start_time: str, break_info: str) -> str:

        _finish_time = list(map(int, str(finish_time).split(":")))
        start_time = list(map(int, str(start_time).split(":"))) 

        if _finish_time[2] < start_time[2]:
            _finish_time[2] += 60
            _finish_time[1] -= 1
        
        if _finish_time[1] < start_time[1]:
            _finish_time[1] += 60
            _finish_time[0] -= 1
        
        _finish_time[0] -= start_time[0]
        _finish_time[1] -= start_time[1]
        _finish_time[2] -= start_time[2]

        break_time[0] += _finish_time[0]
        break_time[1] += _finish_time[1]
        break_time[2] += _finish_time[2]

        return break_time, break_info + f"{finish_time}\n"

    for i in client_report["time_points"]:

        if i["type"] == "start_break":
            start_break_time = i["date"]
            break_info =  f"Break: {i['date']}--"

        elif i["type"] == "finish_break":
            break_time, break_info = calc_break_time(break_time, i["date"], start_break_time, break_info)
            break_info_list += break_info
    
    if start_break_time:
        break_time, break_info = calc_break_time(break_time, datetime.now().time().strftime("%H:%M:%S"), start_break_time, break_info)
        break_info_list += break_info
    
    if break_time[2] >= 60:
        break_time[1] += break_time[2] // 60
        break_time[2] = break_time[2] % 60
    
    if break_time[1] >= 60:
        break_time[0] += break_time[1] // 60
        break_time[1] = break_time[1] % 60
    
    if break_time[2] < 0:
            break_time[1] -= 1
            break_time[2] = 60 + break_time[2]
        
    if break_time[1] < 0:
        break_time[0] -= 1
        break_time[1] = 60 + break_time[1]

    common_break_time = f"{break_time[0]}:{break_time[1]}:{break_time[2]} (h/m/s)"

    if report:

        report.finish_time = datetime.now().time().strftime("%H:%M:%S")
        report.additional = break_info_list
        report.common_break_time = common_break_time

        calc_start_time = list(map(int, str(report.start_time).split(":")))
        calc_finish_time = list(map(int, str(report.finish_time).split(":")))
        
        calc_finish_time[2] -= calc_start_time[2]
        calc_finish_time[1] -= calc_start_time[1]
        calc_finish_time[0] -= calc_start_time[0]

        if calc_finish_time[2] >= 60:
            calc_finish_time[1] += calc_finish_time[2] // 60
            calc_finish_time[2] = calc_finish_time[2] % 60
    
        if calc_finish_time[1] >= 60:
            calc_finish_time[0] += calc_finish_time[1] // 60
            calc_finish_time[1] = calc_finish_time[1] % 60
        
        if calc_finish_time[2] < 0:
            calc_finish_time[1] -= 1
            calc_finish_time[2] = 60 + calc_finish_time[2]
        
        if calc_finish_time[1] < 0:
            calc_finish_time[0] -= 1
            calc_finish_time[1] = 60 + calc_finish_time[1]
     
        report.common_work_time = f"{calc_finish_time[0]}:{calc_finish_time[1]}:{calc_finish_time[2]} (h/m/s)"

        common_work_time = list(map(int, str(report.common_work_time.split(" ")[0]).split(":")))
        work_time = common_work_time[1] + (common_work_time[0]*60)

        common_break_time = list(map(int, str(report.common_break_time.split(" ")[0]).split(":")))
        break_time = common_break_time[1] + (common_break_time[0]*60)

        break_procent = (break_time / work_time) * 100
        report.work_efficiency = f"{round(100 - break_procent, 2)}%"

    else:
        report = DailyWorkReport(worker = worker, start_time = start_time, finish_time = datetime.now().time().strftime("%H:%M:%S"), additional = break_info_list)
    
    report.save()
    
    return HttpResponse(status = 200)

@auth_decorator
def sent_browser_history(request):
    
    client_history = request.headers.get("History")

    try:
        client_history = json.loads(client_history)
    except json.JSONDecodeError:
        return HttpResponse(status = 403)

    for i in client_history["history"]:

        item = BrowserHistoryItem.objects.filter(worker = client_history["worker"], title = i["title"], date = localdate()).first()
        
        if item == None:

            worker = Worker.objects.filter(id = client_history["worker"]).first()

            if worker != None:
                item = BrowserHistoryItem(worker = worker, profile = i["profile"], url = i["url"], title = i["title"])
                item.save()

            else:
                pass

    return HttpResponse(status = 200)