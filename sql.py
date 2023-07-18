import sqlite3

_conn = sqlite3.connect("data/database.db", isolation_level=None)
c = _conn.cursor()
print("New Conn")
c.execute("PRAGMA foreign_keys = 1;")

c.execute("""
CREATE TABLE IF NOT EXISTS users(
name CHAR(20) PRIMARY KEY NOT NULL,
email CHAR(30) NOT NULL,
password CHAR(30) NOT Null);
""")
c.execute("""
CREATE TABLE IF NOT EXISTS scores(
name INTEGER PRIMARY KEY,
game CHAR(20) NOT NULL,
score INTEGER NOT NULL,
FOREIGN KEY (name)
    REFERENCES users (name)
);
""")


def login(name, password):
    pswd = c.execute("SELECT password from users WHERE name=?", (name,)).fetchone()
    try:
        return pswd[0] == password
    except TypeError:
        return False


def register(name, email, password):
    try:
        c.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", (name, email, password))
        return True
    except sqlite3.IntegrityError:
        return False


def get_score(name, game):
    try:
        return c.execute("SELECT score FROM scores WHERE name=? AND game=?;", (name, game)).fetchone()[0]
    except TypeError:
        return 0


def insert_score(name, game, score):
    if score > get_score(name, game):
        c.execute("DELETE FROM scores WHERE name=?", name)
        c.execute("INSERT INTO scores(name, game, score) VALUES (?, ?, ?)", (name, game, score))


def close_conn():
    c.close()  # Handler beenden
    _conn.close()  # Verbindung beenden - wichtig!
    print("Datenbank geschlossen")  # Rückmeldung
