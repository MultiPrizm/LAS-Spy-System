import sqlite3, time, win32crypt, os

if not os.path.exists("Data"):
    os.makedirs("Data")

class DBManager():

    def __init__(self) -> None:
        
        self.db: sqlite3.Connection = sqlite3.connect("Data/app.db")
        self.cursor: sqlite3.Cursor = self.db.cursor()
    
    def setup_secure_string_data(self, key: str, data: str):

        self.cursor.execute("SELECT * FROM secure_string_data WHERE id = ?", (key,))

        if len(self.cursor.fetchall()) != 0:
            self.cursor.execute("UPDATE secure_string_data SET data = ? WHERE id = ?", (win32crypt.CryptProtectData(data.encode()), key))
        else:
            self.cursor.execute("INSERT INTO secure_string_data(id, data) VALUES(?, ?)", (key, win32crypt.CryptProtectData(data.encode())))

        self.db.commit()
    
    def get_secure_string_data(self, key: str):

        self.cursor.execute("SELECT data FROM secure_string_data WHERE id = ?", (key,))
        data = self.cursor.fetchall()

        try:
            data = win32crypt.CryptUnprotectData(data[0][0])

            return data[1].decode()
        except IndexError:
            return None
    
    def addUser(self, id: str, face_hash: str = "None"):

        self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))

        if len(self.cursor.fetchall()) != 0:
            self.cursor.execute("UPDATE users SET face_hash = ? WHERE id = ?", (face_hash, id))
        else:
            self.cursor.execute("INSERT INTO users(id, face_hash) VALUES(?, ?)", (id, face_hash))

        self.db.commit()
    
    def getUsers(self):

        self.cursor.execute("SELECT * FROM users")

        return self.cursor.fetchall()
    
    def delet_user(self, id: str):
        
        self.cursor.execute("DELETE FROM users WHERE id = ?", (id,))

        self.db.commit()

async def db_setup_script(output = None):

    def out_mess(mess: str, progress: int, deley: float = 0):
        if output:
            output(mess, progress)
            time.sleep(deley)

    db: sqlite3.Connection = sqlite3.connect("Data/app.db")
    cursor: sqlite3.Cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(id TEXT PRIMORY KEY, face_hash TEXT)")
    out_mess("Installing users table...", 25, 1)

    cursor.execute("CREATE TABLE IF NOT EXISTS secure_string_data(id TEXT PRIMORY KEY, data BLOB)")
    out_mess("Installing secure table...", 50, 1)

    db.commit()
    out_mess("Finishing...", 99, 2)

    out_mess("", 100, 0)