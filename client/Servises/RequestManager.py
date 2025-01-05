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

    def load_users(self) -> bool:

        try:
            data = requests.get(self.url + "auth/", headers=self.headers)
        except requests.exceptions.ConnectionError:
            return False

        if data.status_code != 200:
            return False

        data = data.json()

        for i in data["users"]:
            self.db.addUser(i[0], i[1])
        
        return True
    
    def send_report(self, data):
        headers = copy.copy(self.headers)
        headers["Report"] = json.dumps(data)

        try:
            respons = requests.get(self.url + "app/report/", headers=headers)
        except requests.exceptions.ConnectionError:
            return

        if respons.status_code == 404:
            self.db.delet_user(data["worker"])
            self.load_users()
    
    def send_browser_history(self, data):
        
        headers = copy.copy(self.headers)
        headers["History"] = json.dumps(data)

        try:
            respons = requests.get(self.url + "app/history/", headers=headers)
        except requests.exceptions.ConnectionError:
            return