import sqlite3, time, win32crypt, os

if not os.path.exists("Data"):
    os.makedirs("Data")

class DBManager():

    def __init__(self, encripting: bool = False) -> None:
        
        self.db: sqlite3.Connection = sqlite3.connect("Data/app.db")
        self.cursor: sqlite3.Cursor = self.db.cursor()
    
    def setup_secure_string_data(self, key: str, data: str):
        
        self.cursor.execute("INSERT INTO secure_string_data(id, data) VALUE(?, ?)", (key, win32crypt.CryptProtectData(data)))

async def db_setup_script(output = None):

    def out_mess(mess: str, progress: int, deley: float = 0):
        if output:
            output(mess, progress)
            time.sleep(deley)

    db: sqlite3.Connection = sqlite3.connect("Data/app.db")
    cursor: sqlite3.Cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS secure_string_data(id TEXT PRIMORY KEY, data BLOB)")
    out_mess("Installing secure table...", 50, 2)

    db.commit()
    out_mess("Finishing...", 99, 2)

    out_mess("", 100, 0)

