from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.contrib import messages
from server.settings import JWT_KEY
from authorization.models import WorkStation
from spy_app.models import Worker
import jwt

def auth_decorator(func):

    def wrapper(request, *arg, **kwargs):

        auth_header = request.headers.get('Auth')
        
        if not auth_header:
            return JsonResponse({'error': 'Authorization token is missing'}, status=401)
        
        try:
            decoded_token = jwt.decode(auth_header, JWT_KEY, algorithms=["HS256"])

            request.user = decoded_token
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        return func(request, *arg, **kwargs)
    
    return wrapper

@require_GET
@auth_decorator
def load_users(requests):

    station = WorkStation.objects.filter(id = requests.user["station"])[0]

    worker_list = Worker.objects.filter(station = station)

    data = []

    for i in worker_list:
        print(i.id)
        data.append([i.id, i.face_hash.decode()]) 

    return JsonResponse({"users": data})