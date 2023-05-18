import pygame
from sys import exit
import math

pygame.init()
display_width = 1200
display_height = 900

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display = pygame.display.set_mode((display_width,display_height))
display_rect = display.get_rect()
floor = pygame.Surface((display_width,40))
floor.fill((blue))
floorRect = floor.get_rect(topleft=(0,860))
pygame.display.set_caption('TANK')
clock = pygame.time.Clock()

class Player1:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 20
        self.image = pygame.Surface((self.width,self.height)).convert()
        self.image.fill(white)
        self.rect = self.image.get_rect(bottomleft=(screen_rect.left + 60,screen_rect.bottom - 40))
        self.projektil = pygame.Surface((10,10)).convert()
        self.projektil.fill(white)
        self.projektile = pygame.Surface((30,30)).convert()
        self.projektile.fill(yellow)
        self.speed = 5
        self.stärke = 50
        self.stärkeänder = 1
        self.winkel = 45
        self.winkeländer = 0.3
        self.schuss = False
        self.counter = 0
        self.treffer = False
        self.schussrohrx = 0
        self.schussrohry = 0
        self.g = gravity
        self.treffercounter = 0
        self.health = 500
        self.spieleramzug = 1

    def schussrohr(self):
        x = round(math.cos(self.winkel/360*math.pi*2)*self.stärke)
        y = round(math.sqrt(self.stärke**2-x**2))
        self.schussrohrx = self.rect.x+x+ self.width/2
        self.schussrohry = self.rect.y -y
        return (self.schussrohrx, self.schussrohry)

    def schussexecute(self):
        if self.schuss:
            self.counter += 1
            if not self.treffer:
                for i in range(self.counter//10+1):
                    if i < 5:
                        display.blit(self.projektil,self.position(i))
            elif self.treffer:
                self.explosion()
                
    def explosion(self):
        self.treffercounter += 1
        for i in range(4-self.treffercounter//10):
            display.blit(self.projektil,self.position(self.treffercounter*0.1+i+1))
        if self.treffercounter <= 5:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 10 and self.treffercounter <=15:
            self.projektile.fill(yellow)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 20 and self.treffercounter <=25:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 30 and self.treffercounter <=35:
            self.projektile.fill(yellow)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 40 and self.treffercounter <=45:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >=46:
            self.schuss = False
            self.treffer = False
            self.treffercounter = 0
            self.counter = 0
            self.spieleramzug = 2

    def position(self, nummer):
        stärkeneu = self.stärke * 6
        t = self.counter - nummer*10
        v = math.cos(self.winkel/360*math.pi*2)*stärkeneu/60
        h = math.sqrt(stärkeneu**2-v**2)
        x = int(round(v*t, 0)) 
        y = int(round(0.5*(self.g/60)*(t**2) + (h/60)*t, 0))
        x = self.schussrohrx + x - 3
        y =  self.schussrohry - y
        player2x = player2.rect.x
        player2y = player2.rect.y
        if y >= player2y:
            if player2x <= x and x <= player2x+40:
                self.treffer = True
                if self.treffercounter % 6 == 0:
                    player2.health -= 20
        if y >= 840:
            self.treffer = True
        return (x, y)

    def healthbar(self, surface):
        if self.health > 300:
            pygame.draw.line(surface, green, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        elif self.health > 150:
            pygame.draw.line(surface, yellow, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        elif self.health > 0:
            pygame.draw.line(surface, red, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(('Spieler_' + '2' + ' hat gewonnen'), True, 'Green', 'Black')
            textRect = text.get_rect()
            textRect.center = (600,450)
            surface.blit(text,textRect)
            spielbool = False
    
    def update(self, keys):
        if not self.schuss:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            self.rect.clamp_ip(self.screen_rect)
            if keys[pygame.K_UP] and self.stärke < 100:
                self.stärke += self.stärkeänder
                print(self.stärke)
            if keys[pygame.K_DOWN] and self.stärke > 10:
                self.stärke -= self.stärkeänder
                print(self.stärke)
            if keys[pygame.K_LEFT] and self.winkel < 170:
                self.winkel += self.winkeländer
                print(self.winkel)
            if keys[pygame.K_RIGHT] and self.winkel > 10:
                self.winkel -= self.winkeländer
                print(self.winkel)
            if keys[pygame.K_RETURN]:
                self.schuss = True

    def drawplayer(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.line(surface, white, self.rect.center, self.schussrohr(), width = 12)
        self.healthbar(surface)
        return self.spieleramzug
        
    def draw(self):
        self.schussexecute()

class Player2:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 20
        self.image = pygame.Surface((self.width,self.height)).convert()
        self.image.fill(white)
        self.rect = self.image.get_rect(bottomright=(screen_rect.right - 60,screen_rect.bottom - 40))
        self.projektil = pygame.Surface((10,10)).convert()
        self.projektil.fill(white)
        self.projektile = pygame.Surface((30,30)).convert()
        self.projektile.fill(yellow)
        self.speed = 5
        self.stärke = 50
        self.stärkeänder = 1
        self.winkel = 135
        self.winkeländer = 0.3
        self.schuss = False
        self.counter = 0
        self.treffer = False
        self.schussrohrx = 0
        self.schussrohry = 0
        self.g = gravity
        self.treffercounter = 0
        self.health = 500
        self.spieleramzug = 2

    def schussrohr(self):
        x = round(math.cos(self.winkel/360*math.pi*2)*self.stärke)
        y = round(math.sqrt(self.stärke**2-x**2))
        self.schussrohrx = self.rect.x+x+ self.width/2
        self.schussrohry = self.rect.y -y
        return (self.schussrohrx, self.schussrohry)
    
    def schussexecute(self):
        if self.schuss:
            self.counter += 1
            if not self.treffer:
                for i in range(self.counter//10+1):
                    if i < 5:
                        display.blit(self.projektil,self.position(i))
            elif self.treffer:
                self.explosion()
                
    def explosion(self):
        self.treffercounter += 1
        for i in range(4-self.treffercounter//10):
            display.blit(self.projektil,self.position(self.treffercounter*0.1+i+1))
        if self.treffercounter <= 5:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 10 and self.treffercounter <=15:
            self.projektile.fill(yellow)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 20 and self.treffercounter <=25:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 30 and self.treffercounter <=35:
            self.projektile.fill(yellow)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >= 40 and self.treffercounter <=45:
            self.projektile.fill(red)
            display.blit(self.projektile,self.position(self.treffercounter*0.1))
        elif self.treffercounter >=46:
            self.schuss = False
            self.treffer = False
            self.treffercounter = 0
            self.counter = 0
            player1.spieleramzug = 1

    def position(self, nummer):
        stärkeneu = self.stärke * 6
        t = self.counter - nummer*10
        v = math.cos(self.winkel/360*math.pi*2)*stärkeneu/60
        h = math.sqrt(stärkeneu**2-v**2)
        x = int(round(v*t, 0)) 
        y = int(round(0.5*(self.g/60)*(t**2) + (h/60)*t, 0))
        x = self.schussrohrx + x - 3
        y =  self.schussrohry - y
        player1x = player1.rect.x
        player1y = player1.rect.y
        if y >= player1y:
            if player1x <= x and x <= player1x+40:
                self.treffer = True
                if self.treffercounter % 6 == 0:
                    player1.health -= 20
        if y >= 840:
            self.treffer = True
        return (x, y)

    def healthbar(self, surface):
        if self.health > 300:
            pygame.draw.line(surface, green, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        elif self.health > 150:
            pygame.draw.line(surface, yellow, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        elif self.health > 0:
            pygame.draw.line(surface, red, (self.rect.x, self.rect.y + 30), (self.rect.x + self.health/10, self.rect.y + 30), width = 8)
        else:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(('Spieler_' + '1' + ' hat gewonnen'), True, 'Green', 'Black')
            textRect = text.get_rect()
            textRect.center = (600,450)
            surface.blit(text,textRect)
            spielbool = False

    def update(self, keys):
        if not self.schuss:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            self.rect.clamp_ip(self.screen_rect)
            if keys[pygame.K_UP] and self.stärke < 100:
                self.stärke += self.stärkeänder
                print(self.stärke)
            if keys[pygame.K_DOWN] and self.stärke > 10:
                self.stärke -= self.stärkeänder
                print(self.stärke)
            if keys[pygame.K_LEFT] and self.winkel < 170:
                self.winkel += self.winkeländer
                print(self.winkel)
            if keys[pygame.K_RIGHT] and self.winkel > 10:
                self.winkel -= self.winkeländer
                print(self.winkel)
            if keys[pygame.K_RETURN]:
                self.schuss = True

    def drawplayer(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.line(surface, white, self.rect.center, self.schussrohr(), width = 12)
        self.healthbar(surface)
        return player1.spieleramzug 

    def draw(self):
        self.schussexecute()
        
spielbool = True
gravity = -5
spieleramzug = 1
player1 = Player1(display_rect)
player2 = Player2(display_rect)
     
while spielbool:
    keys = pygame.key.get_pressed()
    display.fill(black)
    display.blit(floor,floorRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielbool = False
            exit()
            
    if player1.spieleramzug  == 1:
        player1.update(keys)
    player1.drawplayer(display)
    if player1.spieleramzug  == 2:
        player2.update(keys)
    player2.drawplayer(display)
    player1.schussexecute()
    player2.schussexecute()

    pygame.display.update()
    clock.tick(60)
    
