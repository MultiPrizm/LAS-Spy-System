from Servises.RequestManager import RequestsManager
from Servises.TimePline import WorkTimeLineManager
import asyncio, os, sqlite3, shutil
from datetime import datetime, timedelta


class BrowserHistoryManager():

    def __init__(self, request_manager: RequestsManager, time_manager: WorkTimeLineManager):
        
        self.request_manager = request_manager
        self.time_manager = time_manager
    
    async def LaunchServise(self):

        while True:
            history = self.get_chrome_history()

            self.send_history(history)

            await asyncio.sleep(10)
    
    def send_history(self, history):

        if self.time_manager.active_worker == None:
            
            return

        self.request_manager.send_browser_history({
            "worker": self.time_manager.active_worker,
            "history": history
        })
    
    def get_chrome_history(self):

        _history = []

        user_path = os.path.expanduser('~')
        chrome_user_data_path = os.path.join(user_path, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        epoch_start = datetime(1601, 1, 1)
        today_start_webkit = int((today_start - epoch_start).total_seconds() * 1_000_000)
        
        temp_db_path = os.path.join(user_path, 'AppData', 'Local', 'Temp', 'chrome_history_copy_copy.db')
        profiles = ["Default"]

        for i in os.listdir(chrome_user_data_path):
            if i.split(" ")[0] == "Profile":
                profiles.append(i)

        for profile in profiles:
            history_db_path = os.path.join(chrome_user_data_path, profile, 'History')

            if not os.path.exists(history_db_path):
                continue

            try:
                shutil.copy2(history_db_path, temp_db_path)
            except Exception as e:
                continue

            try:
                conn = sqlite3.connect(temp_db_path)
                cursor = conn.cursor()

                cursor.execute(f"""
                    SELECT url, title, visit_count, last_visit_time
                    FROM urls
                    WHERE last_visit_time >= {today_start_webkit}
                    ORDER BY last_visit_time DESC
                """)

                history = cursor.fetchall()

                for row in history:
                    
                    url, title, visit_count, last_visit_time = row[:4]

                    _history.append({
                        "profile": profile,
                        "title": title,
                        "url": url,
                        "time": last_visit_time
                    })

                    #_history.append(f"Profile: {profile} Title: {title}, URL: {url}, Visits: {visit_count}, Time: {last_visit_time}")

                conn.close()

            except sqlite3.OperationalError as e:
                continue

            if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)

        return _history