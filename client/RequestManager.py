import requests

def login():
    data = requests.get("http://127.0.0.1:8000/auth/login")
    print(data.content)

login()