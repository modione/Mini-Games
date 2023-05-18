# SQLite als Alternative zu MySQLdb
# Super-Doku: http://docs.python.org/library/sqlite3.html
# Eine Tabelle mit Vor-, Nachname und eMail-Adresse
# wird mit Daten befüllt und ausgelesen...

import sqlite3                          # importiere das Modul
conn = sqlite3.connect("database.db")   # erstelle Verbindung: Daten ins RAM
c = conn.cursor()                       # Händler erzeugen

c.execute("""
CREATE TABLE IF NOT EXISTS person(
id INTEGER PRIMARY KEY AUTOINCREMENT,
vorname CHAR(20) NOT NULL,
nachname CHAR(20) NOT NULL,
email CHAR(30) NOT NULL,
score INTEGER NOT NULL,
level INTEGER NOT NULL);
""")                                    # Tabelle erstellen


datensatz = [("Spast","Seppl","D.Vader@sith-online.imp"),
             ("Obi-Wan","Kenobi","master.Kenobi@jedimaine.co")]
# c.executemany("""INSERT INTO person(id,vorname,nachname,email) VALUES (NULL, ?, ?, ?)""", datensatz)

for zeile in c.execute("SELECT * FROM person;"):
    print(zeile)                        # gehe durch die Erg.liste und
                                        # printe jedes Tupel

eingabe=True
while eingabe:
    vorname=input("Vorname(ENTER=quit): ")
    if not vorname:
        break
    nachname=input("Nachname: ")
    email=input("eMail-Adresse: ")
    score=input("score: ")
    level=input("level: ")
    
    c.execute("""
                INSERT INTO person
                VALUES(NULL,?,?,?,?,?)""",
              (vorname,nachname,email,score,level)); # einfügen
    conn.commit()                          # Daten physikalisch schreiben
    
    for zeile in c.execute("SELECT * FROM person;"):
        print(zeile)                    # gehe durch die Erg.liste und printe


#c.fetchall()                          # holt alle Datensätze in eine Liste von Tupeln
c.close()                               # Handler beenden
conn.close()                            # Verbindung beenden - wichtig!
print("Datenbank geschlossen")          # Rückmeldung

