import pygame
from sys import exit
import math
import random
import time

pygame.init()
display_width = 1200
display_height = 900

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
tankcolor = (13.7,16.9,0)

display = pygame.display.set_mode((display_width,display_height))
display_rect = display.get_rect()
floor = pygame.image.load(("floor.png"))
floorRect = floor.get_rect(topleft=(0,820))
pygame.display.set_caption('TANK')
clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)
text1 = font.render(('Du hast verloren!'), True, green, black)
text1Rect = text1.get_rect()
text1Rect.center = (600,100)
deathexplosion4 = pygame.image.load(("deathexplosion.png"))
deathexplosion5 = pygame.image.load(("deathexplosion1.png"))
deathexplosion6 = pygame.image.load(("deathexplosion2.png"))
deathexplosion7 = pygame.image.load(("deathexplosion3.png"))
deathexplosion3 = pygame.image.load(("deathexplosion4.png"))
deathexplosion2 = pygame.image.load(("deathexplosion5.png"))
deathexplosion1 = pygame.image.load(("deathexplosion6.png"))
tanksprite = pygame.image.load(('sprite1.png'))
projektil1 = pygame.image.load(("projektil.png"))
projektil2 = pygame.image.load(("projektile1.png"))
projektil3 = pygame.image.load(("projektil2.png"))
projektil4 = pygame.image.load(("projektil3.png"))
projektil5 = pygame.image.load(("projektil4.png"))
tankwidth = 50
tankheight = 20
tankspeed = 5
tankstärke = 25
tankwinkel = 45
tankhealth = 500

class Player1:
    def __init__(self, screen_rect, level):
        self.screen_rect = screen_rect
        self.width = tankwidth
        self.height = tankheight
        self.image = tanksprite
        self.rect = self.image.get_rect(bottomleft=(screen_rect.left + 60,screen_rect.bottom - 80))
        self.projektil = projektil1
        self.projektil1 = projektil2
        self.projektil2 = projektil3
        self.projektil3 = projektil4
        self.projektil4 = projektil5
        self.speed = tankspeed
        self.stärke = tankstärke
        self.winkel = tankwinkel
        self.schuss = False
        self.death = False
        self.treffer = False
        self.schussrohrx = 0
        self.schussrohry = 0
        self.g = gravity
        self.treffercounter = 0
        self.health = tankhealth
        self.spieleramzug = 1
        self.counter = 0
        self.level = level
        self.winkelchanger = False

    def schussrohr(self):
        x = round(math.cos(self.winkel/360*math.pi*2)*40)
        y = round(math.sqrt(40**2-x**2))
        self.schussrohrx = self.rect.x+x+ self.width/2
        self.schussrohry = self.rect.y -y
        return (self.schussrohrx, self.schussrohry)

    def schussexecute(self):
        if self.schuss:
            self.counter += 1
            if not self.treffer:
                for i in range(self.counter//10+1):
                    if i < 5:
                        list = self.position(i)
                        angle = list[1]
                        xy = list[0]
                        display.blit(self.rot_center(self.projektil, angle), xy)
            elif self.treffer:
                self.explosion()
                
    def explosion(self):
        self.treffercounter += 1
        for i in range(4-self.treffercounter//10):
            i = 3-i
            if self.treffercounter <= 40:
                list = self.position(i+1)
                angle = list[1]
                xy = list[0]
                display.blit(self.rot_center(self.projektil, angle), xy)
        if self.treffercounter <= 5:
            self.explosionanimation()
        elif self.treffercounter >= 10 and self.treffercounter <=15:
            self.explosionanimation()
        elif self.treffercounter >= 20 and self.treffercounter <=25:
            self.explosionanimation()
        elif self.treffercounter >= 30 and self.treffercounter <=35:
            self.explosionanimation()
        elif self.treffercounter >= 40 and self.treffercounter <=45:
            self.explosionanimation()
        elif self.treffercounter >=46:
            self.schuss = False
            self.treffer = False
            self.treffercounter = 0
            self.counter = 0
            self.spieleramzug = 2

    def explosionanimation(self):
            projektilRect = self.projektil4.get_rect(center=self.position(self.treffercounter*0.1)[0])
            projektilRect.x += 20
            zahl = self.treffercounter % 5
            if zahl == 0:
                display.blit(self.projektil4,projektilRect)
            elif zahl == 1:
                display.blit(self.projektil3,projektilRect)
            elif zahl == 2:
                display.blit(self.projektil2,projektilRect)
            elif zahl == 3:
                display.blit(self.projektil2,projektilRect)
            elif zahl == 4:
                display.blit(self.projektil1,projektilRect)

    def position(self, nummer):
        stärkeneu = self.stärke * 10 / 60
        t = self.counter - nummer*10
        v = math.cos(self.winkel/360*math.pi*2)*stärkeneu
        h = math.sqrt(stärkeneu**2-v**2)
        x = v*t - 15
        y = 0.5*self.g*(t**2) + h*t +15
        x = round(self.schussrohrx + x - 3, 0)
        y = round(self.schussrohry - y, 0)
        angle = self.g*t + h
        angle = math.degrees(math.atan(angle))
        player2x = player2.rect.x
        player2y = player2.rect.y
        if y >= player2y:
            if player2x-40 <= x and x <= player2x+40:
                self.treffer = True
                if self.treffercounter % 6 == 0:
                    player2.health -= 20
        if y >= 800:
            self.treffer = True
        if obstacle.x >= x and x >= obstacle.x - obstacle.width:
            if obstacle.y >= y and y >= obstacle.y - obstacle.height:
                self.treffer = True
        if player1.level > 1:
            if obstacle.x - obstacle.xchanger >= x and x >= obstacle.x - obstacle.width - obstacle.xchanger:
                if obstacle.y >= y and y >= obstacle.y - obstacle.height + obstacle.ychanger:
                    self.treffer = True
            if player1.level > 3:
                if obstacle.x - obstacle.xchanger-200 >= x and x >= obstacle.x - obstacle.width - obstacle.xchanger-200:
                    if obstacle.y >= y and y >= obstacle.y - obstacle.height + obstacle.ychanger + 50:
                        self.treffer = True
        return (x, y), angle
    
##    def positionfinder(self):
##        v = 10
##        player1x =  player2.rect.x - self.schussrohrx
##        schussrohry = self.schussrohry
##        teil1 = -2*self.g*(15-schussrohry+800)
##        nenner1 = (teil1 - (((self.g**2)*(player1x**2)+30*(self.g**2)*player1x+(self.g**2)*225)/(v**2)))*v
##        nenner2 = (nenner1 / (2*(self.g*player1x+15*self.g)))**2
##        stärke = math.sqrt(nenner2 + (v**2))
##        winkel = math.acos(v/stärke)*180/math.pi
##        stärke = stärke*6
##        print(winkel,stärke)
##        self.winkelstärke = [winkel,stärke]

    def healthbar(self, surface):
        if self.health > 300:
            pygame.draw.line(surface, green, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        elif self.health > 150:
            pygame.draw.line(surface, yellow, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        elif self.health > 0:
            pygame.draw.line(surface, red, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        else:
            self.death = True
            
    def update(self, keys):
        if not self.schuss:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                if self.rect.x < 700:
                    self.rect.x += self.speed
            self.rect.clamp_ip(self.screen_rect)
            if keys[pygame.K_UP] and self.stärke < 60:
                self.stärke += 0.5
                print(self.stärke)
            if keys[pygame.K_DOWN] and self.stärke > 10:
                self.stärke -= 0.5
                print(self.stärke)
            if keys[pygame.K_LEFT] and self.winkel < 170:
                self.winkel += 0.3
                print(self.winkel)
            if keys[pygame.K_RIGHT] and self.winkel > 10:
                self.winkel -= 0.3
                print(self.winkel)
            if keys[pygame.K_RETURN]:
                self.schuss = True

    def drawplayer(self, surface):
        if spielbool ==  True or self.spieleramzug == 1:
            pygame.draw.line(surface, tankcolor, (self.rect.x+30,self.rect.y+7.5), self.schussrohr(), 5)
            surface.blit(self.image, self.rect)
            self.healthbar(surface)
            if self.stärke >= 45:
                pygame.draw.line(surface, red, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
                font = pygame.font.Font('freesansbold.ttf', 10)
                text = font.render(str(round(self.stärke)), True, black, red)
                textRect = text.get_rect()
                textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
                surface.blit(text,textRect)
            elif self.stärke >= 30:
                pygame.draw.line(surface, yellow, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
                font = pygame.font.Font('freesansbold.ttf', 10)
                text = font.render(str(round(self.stärke)), True, black, yellow)
                textRect = text.get_rect()
                textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
                surface.blit(text,textRect)
            else:
                pygame.draw.line(surface, green, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
                font = pygame.font.Font('freesansbold.ttf', 10)
                text = font.render(str(round(self.stärke)), True, black, green)
                textRect = text.get_rect()
                textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
                surface.blit(text,textRect)
            return self.spieleramzug
        
    def draw(self):
        self.schussexecute()

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def deathanimation(self, t, surface):
        if t <= 5:
            surface.blit(deathexplosion7, (self.rect.x-20, self.rect.y - 170))
        elif t <= 10:
            surface.blit(deathexplosion6, (self.rect.x-20, self.rect.y - 170))
        elif t <= 15:
            surface.blit(deathexplosion5, (self.rect.x-20, self.rect.y - 170))
        elif t<= 20: 
            display.blit(deathexplosion4, (self.rect.x-20, self.rect.y - 170))
        elif t <= 25:
            surface.blit(deathexplosion3, (self.rect.x-20, self.rect.y - 170))
        elif t <= 30:
            surface.blit(deathexplosion2, (self.rect.x-20, self.rect.y - 170))
        elif t <= 35:
            display.blit(deathexplosion1, (self.rect.x-20, self.rect.y - 170))
        else:
            t = 0
            surface.blit(text1,text1Rect)
            spielbool = False
        
class Player2:
    def __init__(self, screen_rect, difficulty):
        self.screen_rect = screen_rect
        self.width = tankwidth
        self.height = tankheight
        self.image = tanksprite
        self.rect = self.image.get_rect(bottomright=(screen_rect.right - 60,screen_rect.bottom - 80))
        self.projektil = projektil1
        self.projektil1 = projektil2
        self.projektil2 = projektil3
        self.projektil3 = projektil4
        self.projektil4 = projektil5
        self.speed = tankspeed
        self.stärke = tankstärke
        self.winkel = 180 - tankwinkel
        self.schuss = False
        self.death = False
        self.treffer = False
        self.vswitch = True
        self.schussrohrx = 0
        self.schussrohry = 0
        self.g = gravity
        self.treffercounter = 0
        self.health = tankhealth
        self.counter = 0
        self.winkelstärke = []
        self.difficulty = difficulty
        self.levelchanged = True

    def schussrohr(self):
        x = round(math.cos(self.winkel/360*math.pi*2)*40)
        y = round(math.sqrt(40**2-x**2))
        self.schussrohrx = self.rect.x+x+ self.width/2
        self.schussrohry = self.rect.y -y
        return (self.schussrohrx, self.schussrohry)
    
    def schussexecute(self):
        if self.schuss:
            self.counter += 1
            if not self.treffer:
                for i in range(self.counter//10+1):
                    if i < 5:
                        list = self.position(i)
                        angle = list[1]
                        xy = list[0]
                        display.blit(self.rot_center(self.projektil, angle), xy)
            elif self.treffer:
                self.explosion()
        elif player1.spieleramzug ==2:
            if self.vswitch:
                self.positionfinder()
                self.vswitch = False
            if round(self.winkelstärke[0]) > self.winkel:
                self.winkel = self.winkel +0.5
            elif round(self.winkelstärke[0]) < self.winkel:
                self.winkel = self.winkel - 0.5
            else:
                if round(self.winkelstärke[1]) > round(self.stärke):
                    self.stärke = self.stärke + 0.5
                elif round(self.winkelstärke[1]) < round(self.stärke):
                    self.stärke = self.stärke - 0.5
                else:
                    self.vswitch = True
                    self.schuss = True
            clock.tick(40)
                
    def explosion(self):
        self.treffercounter += 1
        for i in range(4-self.treffercounter//10):
            i = 3-i
            if self.treffercounter <= 40:
                list = self.position(i+1)
                angle = list[1]
                xy = list[0]
                display.blit(self.rot_center(self.projektil, angle), xy)
        if self.treffercounter <= 5:
            self.explosionanimation()
        elif self.treffercounter >= 10 and self.treffercounter <=15:
            self.explosionanimation()
        elif self.treffercounter >= 20 and self.treffercounter <=25:
            self.explosionanimation()
        elif self.treffercounter >= 30 and self.treffercounter <=35:
            self.explosionanimation()
        elif self.treffercounter >= 40 and self.treffercounter <=45:
            self.explosionanimation()
        elif self.treffercounter >=46:
            self.schuss = False
            self.treffer = False
            self.treffercounter = 0
            self.counter = 0
            player1.spieleramzug = 1
            
    def explosionanimation(self):
        projektilRect = self.projektil4.get_rect(center=self.position(self.treffercounter*0.1)[0])
        projektilRect.x += 20
        zahl = self.treffercounter % 5
        if zahl == 0:
            display.blit(self.projektil4, projektilRect)
        elif zahl == 1:
            display.blit(self.projektil3, projektilRect)
        elif zahl == 2:
            display.blit(self.projektil2, projektilRect)
        elif zahl == 3:
            display.blit(self.projektil2, projektilRect)
        elif zahl == 4:
            display.blit(self.projektil1, projektilRect)


    def position(self, nummer):
        stärkeneu = self.stärke * 10 / 60
        t = self.counter - nummer*10
        v = math.cos(self.winkel/360*math.pi*2)*stärkeneu
        h = math.sqrt(stärkeneu**2-v**2)
        x = v*t
        y = 0.5*self.g*(t**2) + h*t +15
        x = round(self.schussrohrx + x  - 6, 0)
        y = round(self.schussrohry - y, 0)
        angle = self.g*t + h
        angle = math.degrees(math.atan(angle))*-1+180
        player1x = player1.rect.x
        player1y = player1.rect.y
        if y >= player1y:
            if player1x-40 <= x and x <= player1x+40:
                self.treffer = True
                if self.treffercounter % 6 == 0:
                    player1.health -= 20
        if y >= 800:
            self.treffer = True
        if obstacle.x >= x and x >= obstacle.x - obstacle.width:
            if obstacle.y >= y and y >= obstacle.y - obstacle.height:
                self.treffer = True
        if player1.level > 1:
            if obstacle.x - obstacle.xchanger >= x and x >= obstacle.x - obstacle.width - obstacle.xchanger:
                if obstacle.y >= y and y >= obstacle.y - obstacle.height + obstacle.ychanger:
                    self.treffer = True
            if player1.level > 3:
                if obstacle.x - obstacle.xchanger-200 >= x and x >= obstacle.x - obstacle.width - obstacle.xchanger-200:
                    if obstacle.y >= y and y >= obstacle.y - obstacle.height + obstacle.ychanger + 50:
                        self.treffer = True
        return (x, y), angle

    def positionfinder(self):
        v = random.randint(3,10)
        player2x =  self.schussrohrx - player1.rect.x-self.width/2
        schussrohry = self.schussrohry
        teil1 = -2*self.g*(15-schussrohry+800)
        nenner1 = (teil1 - (((self.g**2)*(player2x**2)+30*(self.g**2)*player2x+(self.g**2)*225)/(v**2)))*v
        nenner2 = (nenner1 / (2*(self.g*player2x+15*self.g)))**2
        stärke = math.sqrt(nenner2 + (v**2))
        winkel = 180-math.acos(v/stärke)*180/math.pi
        stärke = stärke*6 + random.randint(-10 + self.difficulty*2,10 - self.difficulty*2)+0.5
        self.winkelstärke = [winkel,stärke]

    def healthbar(self, surface):
        if self.health > 300:
            pygame.draw.line(surface, green, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        elif self.health > 150:
            pygame.draw.line(surface, yellow, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        elif self.health > 0:
            pygame.draw.line(surface, red, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), 4)
        else:
           self.death = True

##    def update(self, keys):
##        if not self.schuss:
##            if keys[pygame.K_a]:
##                self.rect.x -= self.speed
##            if keys[pygame.K_d]:
##                self.rect.x += self.speed
##            self.rect.clamp_ip(self.screen_rect)
##            if keys[pygame.K_UP] and self.stärke < 60:
##                self.stärke += self.stärkeänder
##                print(self.stärke)
##            if keys[pygame.K_DOWN] and self.stärke > 10:
##                self.stärke -= self.stärkeänder
##                print(self.stärke)
##            if keys[pygame.K_LEFT] and self.winkel < 170:
##                self.winkel += self.winkeländer
##                print(self.winkel)
##            if keys[pygame.K_RIGHT] and self.winkel > 10:
##                self.winkel -= self.winkeländer
##                print(self.winkel)
##            if keys[pygame.K_RETURN]:
##                self.schuss = True

    def drawplayer(self, surface):
        pygame.draw.line(surface, tankcolor, (self.rect.x+30,self.rect.y+7.5), self.schussrohr(), 5)
        surface.blit(self.image, self.rect)
        self.healthbar(surface)
        if self.stärke >= 45:
            pygame.draw.line(surface, red, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
            font = pygame.font.Font('freesansbold.ttf', 10)
            text = font.render(str(round(self.stärke)), True, black, red)
            textRect = text.get_rect()
            textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
            surface.blit(text,textRect)
        elif self.stärke >= 30:
            pygame.draw.line(surface, yellow, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
            font = pygame.font.Font('freesansbold.ttf', 10)
            text = font.render(str(round(self.stärke)), True, black, yellow)
            textRect = text.get_rect()
            textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
            surface.blit(text,textRect)
        else:
            pygame.draw.line(surface, green, (self.rect.x,self.rect.y+40), (self.rect.x+self.stärke,self.rect.y+40), 10)
            font = pygame.font.Font('freesansbold.ttf', 10)
            text = font.render(str(round(self.stärke)), True, black, green)
            textRect = text.get_rect()
            textRect.center = (self.rect.x+self.stärke/2,self.rect.y+41)
            surface.blit(text,textRect)
        return player1.spieleramzug 

    def draw(self):
        self.schussexecute()

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def deathanimation(self, t, surface):
        if t <= 5:
            surface.blit(deathexplosion7, (self.rect.x-20, self.rect.y - 170))
        elif t <= 10:
            surface.blit(deathexplosion6, (self.rect.x-20, self.rect.y - 170))
        elif t <= 15:
            surface.blit(deathexplosion5, (self.rect.x-20, self.rect.y - 170))
        elif t<= 20: 
            display.blit(deathexplosion4, (self.rect.x-20, self.rect.y - 170))
        elif t <= 25:
            surface.blit(deathexplosion3, (self.rect.x-20, self.rect.y - 170))
        elif t <= 30:
            surface.blit(deathexplosion2, (self.rect.x-20, self.rect.y - 170))
        elif t <= 35:
            display.blit(deathexplosion1, (self.rect.x-20, self.rect.y - 170))
        else:
            t = 0
            player1.level = player1.level + 1
            self.difficulty += 1
            player2.levelchanged = True
            text2 = font.render(('Loading Level '+ str(player1.level)+' ...'), True, green, black)
            text2Rect = text2.get_rect()
            text2Rect.center = (600,100)
            surface.blit(text2,text2Rect)
            
            

class Obstacle:
    def __init__(self):
        self.x = random.randint(500, 950)
        self.width = 30
        self.y = random.randint(600, 800)
        self.height = random.randint(300, 400)
        self.xchanger = random.randint(100,500)
        self.ychanger = random.randint(50,150)
        self.level = player1.level
    def draw(self, surface):
        if self.level == 1:
            pygame.draw.line(surface, green, (self.x,self.y), (self.x,self.y-self.height), self.width)
        if self.level >= 2 and self.level <= 3:
            pygame.draw.line(surface, red, (self.x,self.y), (self.x,self.y-self.height), self.width)
            pygame.draw.line(surface, red, (self.x - self.xchanger, self.y), (self.x - self.xchanger,self.y-self.height + self.ychanger), self.width)
        if self.level >= 4 and self.level <= 5:
            pygame.draw.line(surface, blue, (self.x,self.y), (self.x,self.y-self.height), self.width)
            pygame.draw.line(surface, blue, (self.x - self.xchanger, self.y), (self.x - self.xchanger,self.y-self.height + self.ychanger), self.width)
            pygame.draw.line(surface, blue, (self.x - self.xchanger-200, self.y), (self.x - self.xchanger-200,self.y-self.height + self.ychanger+50), self.width)

spielbool = True
gravity = -5/60
player1 = Player1(display_rect, 1)
player2 = Player2(display_rect, 1)
        
while player2.levelchanged:
    print(player2.difficulty)
    globalcounter = 0
    spieleramzug = 1
    player1 = Player1(display_rect, player1.level)
    player2 = Player2(display_rect, player2.difficulty)
    obstacle = Obstacle()
    player2.levelchanged = False    
    while not player2.levelchanged:
        background = pygame.image.load(("background.png"))
        display.blit(background, (0,0))
        display.blit(floor,floorRect)
        obstacle.draw(display)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                      
        if player1.death == False:        
            if player1.spieleramzug  == 1:
                player1.update(keys)
            player1.drawplayer(display)
        else:
            globalcounter += 1
            player1.deathanimation(globalcounter, display)
        if player2.death == False:
            player2.drawplayer(display)
        else:
            globalcounter += 1
            player2.deathanimation(globalcounter, display)
        if player1.death == False: 
            player1.schussexecute()
        if player2.death == False:
            player2.schussexecute()
            
        pygame.display.update()
        clock.tick(60)
    player2.levelchanged = True
    time.sleep(10)
