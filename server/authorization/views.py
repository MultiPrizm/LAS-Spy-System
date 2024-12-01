from django.shortcuts import render, redirect
from django.http import JsonResponse
from authorization.forms import AddWorkstationForm
from django.contrib import messages

def login(req):
    data = {
        "test": 1
    }
    
    return JsonResponse(data)

def add_work_station_model(request, admin_site):
    if request.method == "POST":
        form = AddWorkstationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запис успішно додано!")
            return redirect("admin:index")
