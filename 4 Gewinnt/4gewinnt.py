import pygame

# Initializieren
pygame.init()

#Farben
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

#Fenster kreieren
screen = pygame.display.set_mode((1020,920))
screen.fill(blue)
pygame.display.set_caption('4Gewinnt')
clock = pygame.time.Clock()

#Refreshender Background für den Cursor
background = pygame.image.load(("4Gewinnt.png"))
screen.blit(background,(0,0))
background1 = pygame.image.load(("4Gewinnt1.png"))

#Welcher Spieler beginnt
#gelb=1 rot=2
spielerdran = 1

#Variable ob das Spiel läuft
spielbool = True

#Cursor startposition
x = 50
reihe = 0

#Liste machen
spielsteinchenliste = []
for i in range(42):
    spielsteinchenliste.append(0)
    
#Spielsteinmalen und Liste informationen geben
def spielermalen(spielerdran,reihe):
    for i in range(6):
        if spielsteinchenliste[reihe*6+i] == 0:
        #Kreise der Spieler malen
            if spielerdran == 1:
                spielsteinchenliste[reihe*6+i] = 1
                pygame.draw.circle(screen, yellow, (90 + reihe*140,850 - i*140), 50)
                pygame.draw.circle(screen, black, (90 + reihe*140,850 - i*140), 52, 3)
            elif spielerdran == 2:
                spielsteinchenliste[reihe*6+i] = 2
                pygame.draw.circle(screen, red, (90 + reihe*140,850 - i*140), 50)
                pygame.draw.circle(screen, black, (90 + reihe*140,850 - i*140), 52, 3)
            typprüfer()
            break
 #Beendet das Spiel und Zeichnet die letzen Zeichen(Wenn jemand gewonnen hat)       
def typprüfer():
    global spielbool
    x = gewinnüberprüfen(spielerdran)
    if x[0] == 1:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(('Spieler_' + str(spielerdran) + ' hat gewonnen'), True, black)
        textRect = text.get_rect()
        textRect.center = (510,150)
        pygame.draw.line(screen, black, (90 + x[1]*140,850 - x[2]*140), (90 + (x[1] +3)*140,850 - (x[2] -3)*140), 6)
        screen.blit(text, textRect)
        spielbool = False
    if x[0]  == 2:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(('Spieler_' + str(spielerdran) + ' hat gewonnen'), True, black)
        textRect = text.get_rect()
        textRect.center = (510,150)
        pygame.draw.line(screen, black, (90 + x[1]*140,850 - x[2]*140), (90 + (x[1] +3)*140,850 - x[2] *140), 6)
        screen.blit(text, textRect)
        spielbool = False
    if x[0] == 3:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(('Spieler_' + str(spielerdran) + ' hat gewonnen'), True, black)
        textRect = text.get_rect()
        textRect.center = (510,150)
        pygame.draw.line(screen, black, (90 + x[1]*140,850 - x[2]*140), (90 + (x[1] +3)*140,850 - (x[2] +3)*140), 6)
        screen.blit(text, textRect)
        spielbool = False
    if x[0] == 4:
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(('Spieler_' + str(spielerdran) + ' hat gewonnen'), True, black)
        textRect = text.get_rect()
        textRect.center = (510,150)
        pygame.draw.line(screen, black, (90 + x[1]*140,850 - x[2]*140), (90 + (x[1] )*140,850 - (x[2] +3)*140), 6)
        screen.blit(text, textRect)
        spielbool = False

#Überprüfen ob jemand schon gewonnen hat
def gewinnüberprüfen(spielerdran):
    counter = 0
    for e in range(7):
        for i in range(6):
            nummer = e*6+i
            if spielsteinchenliste[nummer] == spielerdran:
                #diagonal unten
                counter = rechnertyp1(nummer)
                if counter >= 4:
                    return 1, e, i
                    break
                counter = 0
                #waagrecht
                counter = rechnertyp2(nummer)
                if counter >= 4:
                    return 2, e, i
                    break
                counter = 0
                #diagonal hoch
                counter = rechnertyp3(nummer)
                if counter >= 4:
                    return 3, e, i
                    break
                counter = 0
                #grade hoch
                counter = rechnertyp4(nummer)
                if counter >= 4:
                    return 4, e, i
                    break
                counter = 0
    return 0, e, i
                     
def rechnertyp1(nummerneu): 
    if not nummerneu % 6 == 0:
        if nummerneu + 5 <= 41:
            if spielsteinchenliste[nummerneu+5] == spielerdran:
               return (1 + rechnertyp1(nummerneu+5))
            else:
                return 1
        else:
            return 1
    else:
        return 1

def rechnertyp2(nummerneu):
    if nummerneu + 6 <= 41:
        if spielsteinchenliste[nummerneu+6] == spielerdran:
           return (1 +  rechnertyp2(nummerneu+6))
        else:
           return 1
    else:
        return 1

def rechnertyp3(nummerneu):
    if not nummerneu % 6 == 5:
        if nummerneu + 7 <= 41:
            if spielsteinchenliste[nummerneu+7] == spielerdran:
               return (1 +  rechnertyp3(nummerneu+7))
            else:
                return 1
        else:
            return 1
    else:
           return 1

def rechnertyp4(nummerneu):
    if not nummerneu % 6 == 5:
        if nummerneu + 1 <= 41:
            if spielsteinchenliste[nummerneu+1] == spielerdran:
               return (1 +  rechnertyp4(nummerneu+1))
            else:
                return 1
        else:
            return 1
    else:
           return 1

#Spielloop
while spielbool:
    
    for event in pygame.event.get():
        #Fenster schließen
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()   
        elif event.type == pygame.KEYDOWN:
            #Linksbewegung
            if event.key == pygame.K_LEFT and x > 50:
                x = x - 140
                reihe = reihe  - 1
            #Rechtsbewegung
            elif event.key == pygame.K_RIGHT and x < 830:
                x = x + 140
                reihe = reihe + 1
             #Bestätigungstaste   
            elif event.key == pygame.K_DOWN :
                #Spielerfarbe ändern
                if spielerdran == 1:
                    spielermalen(spielerdran,reihe)
                    spielerdran = 2
                    continue
                 #Spielerfarbe ändern   
                if spielerdran == 2:
                    spielermalen(spielerdran,reihe)
                    spielerdran = 1
                    
    screen.blit(background1,(0,0))                        
    pygame.draw.polygon(screen, white, [(x,5),(x+40,59),(x+80,5)])

    pygame.display.update()
    clock.tick(60)
 #Fenster schließen wenn das spiel fertig ist   
while True:
    for event in pygame.event.get():
            #Fenster schließen
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

