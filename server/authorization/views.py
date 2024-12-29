from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from server.settings import JWT_KEY
import jwt

def auth_decorator(func):

    @wrapper(func)
    def wrapper(request, *arg, **kwargs):

        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return JsonResponse({'error': 'Authorization token is missing'}, status=401)
        
        try:
            decoded_token = jwt.decode(auth_header, JWT_KEY, algorithms=["HS256"])

            request.user = decoded_token
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        return func(request, *arg, **kwargs)
    
    return wrapper
