import sqlite3


class SQL:
    def __init__(self):
        self._conn = sqlite3.connect("data/database.db", isolation_level=None)
        self.c = self._conn.cursor()

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users(
            name CHAR(20) PRIMARY KEY NOT NULL,
            email CHAR(30) NOT NULL,
            password CHAR(30) NOT Null);""")
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS scores(
            name CHAR(20) NOT NULL,
            game CHAR(20) PRIMARY KEY NOT NULL,
            score INTEGER NOT NULL);""")

    def login(self, name, password):
        pswd = self.c.execute("SELECT password from users WHERE name=?", (name,)).fetchone()
        try:
            return pswd[0] == password
        except TypeError:
            return False

    def register(self, name, email, password):
        try:
            self.c.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", (name, email, password))
            return True
        except sqlite3.IntegrityError:
            return False

    def get_score(self, name, game):
        try:
            return self.c.execute("SELECT score FROM scores WHERE name=? AND game=?;", (name, game)).fetchone()[0]
        except TypeError:
            return 0

    def insert_score(self, name, game, score):
        if score > self.get_score(name, game):
            self.c.execute("DELETE FROM scores WHERE name=?", (name,))
            self.c.execute("INSERT INTO scores(name, game, score) VALUES (?, ?, ?)", (name, game, score))

    def close_conn(self):
        self.c.close()  # Handler beenden
        self._conn.close()  # Verbindung beenden - wichtig!
        print("Datenbank geschlossen")  # Rückmeldung
