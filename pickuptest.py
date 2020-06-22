import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 1600, 900
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('MIO FUCK - DAS SPIEL')

bg = pygame.image.load('landscape.jpg').convert()
crashbg = pygame.image.load('crashscape.jpg')
startscreen = pygame.image.load('startscreenbg.jpg')
title = pygame.image.load('title.png')
tooth = pygame.image.load('tooth.png')
continuebutton = pygame.image.load('symbols/continuebutton.png')
homebutton = pygame.image.load('symbols/homebutton.png')

hitSound = pygame.mixer.Sound('sounds/doorcollision.wav')
gameoverSound = pygame.mixer.Sound('sounds/gameover.wav')




bgX = 0
bgX2 = bg.get_width()

showstartscreen = True

opendoor = False

startcollision = False
doorPassed = False
lifeCount = 4
alive = True

doorIsGreen = False

startpickup = False
btlPassed = False
btlCount = 0
dif = 5 #difficulty(add option to startscreen)

clock = pygame.time.Clock()

class player(object):

    ride = [pygame.image.load("0.png"), pygame.image.load("1.png"), pygame.image.load("2.png"), pygame.image.load("3.png"), pygame.image.load("4.png"), pygame.image.load("5.png"), pygame.image.load("6.png"), pygame.image.load("7.png")]
    jumpList = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,]#[1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.jumpCount = 0
        self.rideCount = 0


    def draw(self, win):
        if self.jumping:
            win.blit(self.ride[0], (self.x,self.y))
            self.y -= self.jumpList[self.jumpCount] * 2 #jumpheightmultiplier
            self.jumpCount += 1
            if self.jumpCount > 139:
                self.jumpCount = 0
                self.jumping = False

        else:
            if showstartscreen == False:

                if self.rideCount >63:
                    self.rideCount = 0
                win.blit(self.ride[self.rideCount//8], (self.x,self.y))
                self.rideCount += 1


class item(object):
    img = pygame.image.load('kimmyg.png')
    imgsc = pygame.transform.scale(img, (35, 105))
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, 35, 105)
        win.blit(self.imgsc, (self.x, self.y))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


class door(item):
    doorCL = pygame.image.load("reddoor.png")
    doorOP = pygame.image.load("doorpassed.png")
    doorGR = pygame.image.load("greendoor.png")
    #imgsc = pygame.transform.scale(img, (40,170))
    def draw(self,win):
        self.hitbox = (self.x,self.y,30,174)
        if opendoor == False:
            win.blit(self.doorCL, (self.x, self.y))
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        if opendoor == True:
            win.blit(self.doorOP, (self.x, self.y))
            #pygame.draw.rect(win, (255,0,0))



def redrawMainWindow():

    win.blit(bg, (bgX, -100))
    win.blit(bg, (bgX2, -100))
    score = font2.render(str(btlCount) + " ‰", 1, (255,255,255))
    # lifedisplay = font1.render(str(lifeCount) + " ECKZAHNE", 1, (255,255,255))
    # umlaut = font1.render("..", 1, (255,255,255))
    #win.blit(umlaut, (107, 3))
    win.blit(score, (1500,20))
    # win.blit(lifedisplay, (30, 20))
    biker.draw(win)

    if doorIsGreen == False:
        reddoor.draw(win)
    # if doorIsGreen == True:
    #     greendoor.draw(win)

    beam.draw(win)

    if lifeCount == 4:
        win.blit(tooth,(20,20))
        win.blit(tooth,(75,20))
        win.blit(tooth,(130,20))
        win.blit(tooth,(185,20))

    if lifeCount == 3:
        win.blit(tooth,(20,20))
        win.blit(tooth,(75,20))
        win.blit(tooth,(130,20))

    if lifeCount == 2:
        win.blit(tooth,(20,20))
        win.blit(tooth,(75,20))

    if lifeCount  == 1:
        win.blit(tooth,(20,20))

    pygame.display.update()


def redrawCrashWindow():
    win.blit(crashbg, (0, -100))
    crashmsg = font2.render("DER ZAHN IST RAUS!", 1, (255,255,255))
    # crashmsg2 = font1.render('press space to continue', 1, (255,255,255))
    # crashmsg3 = font1.render('esc for home')
    # win.blit(crashmsg, (520, 450))
    # win.blit(crashmsg2, (690, 490))
    win.blit(homebutton, (600, 400))
    win.blit(continuebutton, (900, 400))
    biker.draw(win)
    pygame.display.update()

def redrawStartWindow():
    win.blit(startscreen,(0, -100))
    win.blit(title,(0,0))
    startmsg = font1.render("press space to start", 1, (0,0,0))
    win.blit(startmsg, (680,600))
    biker.draw(win)
    pygame.display.update()


font1 = pygame.font.SysFont('comicsans', 31, False) #trueforboldtext
font2 = pygame.font.SysFont('comicsans', 60, False)
# font3 = pygame.font.SysFont('comicsans', )


greendoor = door(-200, 640, 30, 174)
reddoor = door(-200, 640 ,30 ,174) #enable for testing
beam = item(-200, 670, 49, 147) #enable for testing
biker = player(200, 650, 140, 160)
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(3000,7000))
speed = 100
run = True

objects = []

while run:

    if showstartscreen == True:
        redrawStartWindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            showstartscreen = False
            pygame.time.delay(500)


    else:
        if alive == True:
            if beam.x >= - beam.width:
                beam.x -= dif
            if reddoor.x >= - reddoor.width -300:
                reddoor.x -= dif


            bgX -= dif #bgspeed
            bgX2 -= dif
            if bgX < bg.get_width() * -1:
                bgX = bg.get_width() #scrollingbg
            if bgX2 < bg.get_width() * -1:
                bgX2 = bg.get_width()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == USEREVENT+1:
                    speed += 1
                if event.type == USEREVENT+2:
                    r = random.randrange(0,3)
                    if r == 0:                  #resetting items
                        if beam.x < - beam.width:
                            beam.x = 1600
                            startpickup = True
                    else:
                        if reddoor.x <= - reddoor.width:
                            reddoor.x = 1600
                            opendoor = False
                            startcollision = True
                    # else:
                    #     if greendoor.x <= - greendoor.width:
                    #         greendoor.x = 1600
                    #         opendoor = False
                    #         doorIsGreen = True



            keys = pygame.key.get_pressed()

            if not(biker.jumping):
                if keys[pygame.K_SPACE]:
                    biker.jumping = True

        ###bottle pickup/collision

            if btlPassed == False:
                if beam.x <= biker.x + biker.width and startpickup == True and biker.jumping == False and beam.x >= biker.x:
                    dif += 1
                    btlCount += 1
                    btlPassed = True
                    beam.x -= 500

            else:
                if beam.x > biker.x + biker.width:
                    btlPassed = False

        ###reddoor collision


            if doorPassed == False:
                if reddoor.x <= biker.x + biker.width and startcollision == True and reddoor.x >= biker.x and biker.y + biker.height >= reddoor.y:
                    hitSound.play()
                    lifeCount -= 1
                    doorPassed = True
                    opendoor = True

                # if greendoor.x <= biker.x + biker.width and startcollision == True and greendoor.x >= biker.x and biker.y + biker.height >= greendoor.y:
                #     doorPassed = True
                #     opendoor = True

            else:
                if reddoor.x > biker.x + biker.width:
                    doorPassed = False

            if lifeCount == 0:
                gameoverSound.play()
                alive = False


            clock.tick(speed)


            redrawMainWindow()

        else:
            ###crash screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                alive = True
                startcollision = False
                doorPassed = False
                lifeCount = 4
                startpickup = False
                btlPassed = False
                btlCount = 0
                beam.x = -200
                reddoor.x = -200
                dif = 5
                speed = 100
                pygame.time.delay(500)

            if keys[pygame.K_ESCAPE]:
                showstartscreen = Truealive = True
                startcollision = False
                doorPassed = False
                lifeCount = 4
                startpickup = False
                btlPassed = False
                btlCount = 0
                beam.x = -200
                reddoor.x = -200
                dif = 5
                speed = 100
                pygame.time.delay(500)

            redrawCrashWindow()

pygame.quit()
