import threading

import sql

benutzer = ""

sql.register("hurensohn", "sadfsef", "fsdafedasf")


def wahl(message, optionen):
    msg = message + " "
    i = 1
    for key in optionen:
        msg += "(" + str(i) + ") " + key + " "
        i += 1
    inp = int(input(msg))
    while len(optionen) < inp:
        print("Choice not on the list try again")
        inp = int(input())
    return optionen[inp - 1]


while benutzer == "":
    login_register = wahl("Willst du dich", ("Einloggen", "Registrieren"))
    if login_register == "Einloggen":
        cont = True
        while benutzer == "" and cont:
            name = input("Gib deinen Name ein: ")
            password = input("Gib dein Password ein: ")
            if sql.login(name, password):
                benutzer = name
                print("Erfolgreich Eingeloggt")
            else:
                if wahl("Password Falsch!", ("Nochmal Versuchen", "Zurück")) == "Zurück":
                    cont = False
    else:
        cont = True
        while benutzer == "" and cont:
            name = input("Gib deinen Name ein: ")
            email = input("Gib deine Email ein: ")
            password = input("Gib dein Password ein: ")
            if sql.register(name, email, password):
                benutzer = name
                print("Erfolgreich Registriert")
            else:
                if wahl("Name ist schon genommen", ("Nochmal Versuchen", "Zurück")) == "Zurück":
                    cont = False

playing = True
while playing:
    spiel = wahl("Wähle Spiel aus: ", ("Snake", "4 Gewinnt", "Panzer Spiel", "Beenden"))
    if spiel == "Snake":
        import games.snake as snake
        thread = threading.Thread(target=snake.game_loop(benutzer))
        thread.start()
    elif spiel == "4 Gewinnt":
        import games.viergewinnt
    elif spiel == "Panzer Spiel":
        import Panzerfaust.panzer
    elif spiel == "Beenden":
        playing = False
sql.close_conn()
