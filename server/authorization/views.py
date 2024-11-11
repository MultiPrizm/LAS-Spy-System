from django.shortcuts import render
from django.http import JsonResponse

def login(req):
    data = {
        "test": 1
    }
    
    return JsonResponse(data)
