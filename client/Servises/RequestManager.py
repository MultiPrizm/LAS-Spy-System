import requests
from Servises.ConfigManager import DBManager
import copy, json

class RequestsManager():

    def __init__(self, db: DBManager):

        self.db: DBManager = db
        
        self.ip = self.db.get_secure_string_data("server_ip")
        self.token = self.db.get_secure_string_data("api_token")
        self.protocol = self.db.get_secure_string_data("protocol")

        self.url = f"{self.protocol}://{self.ip}/"

        self.headers = {
            "Auth": self.token
        }

        self.load_users()

    def set_csrf_token_from_cookie(self, cookies):
        for cookie in cookies:
            if cookie.name == 'csrftoken':
                print(cookie.value)
                self.headers["X-CSRFToken"] = cookie.value

    def load_users(self) -> bool:

        try:
            data = requests.get(self.url + "auth/", headers=self.headers)
        except requests.exceptions.ConnectionError:
            return False

        if data.status_code != 200:
            return False

        _data = data.json()

        for i in _data["users"]:
            self.db.addUser(i[0], i[1])
        
        self.set_csrf_token_from_cookie(data.cookies)
        
        return True
    
    def send_report(self, data):
        headers = copy.copy(self.headers)
        headers["Report"] = json.dumps(data)

        try:
            respons = requests.post(self.url + "app/report/", headers=headers)
        except requests.exceptions.ConnectionError:
            return

        if respons.status_code == 404:
            self.db.delet_user(data["worker"])
            self.load_users()
        
        self.set_csrf_token_from_cookie(respons.cookies)
    
    def send_browser_history(self, data):
        
        headers = copy.copy(self.headers)
        headers["History"] = json.dumps(data)

        try:
            respons = requests.post(self.url + "app/history/", headers=headers)
        except requests.exceptions.ConnectionError:
            return
        
        self.set_csrf_token_from_cookie(respons.cookies)