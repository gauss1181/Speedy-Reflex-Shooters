# Speedy Reflex Shooters
# 15-112 Term Project
# Megan Chen, meganche, section E

import math, copy, random, string, time
import sys, os
import pygame
from pygame.locals import *

pygame.init()

def showInstructions():
    windowWidth = 640
    windowHeight = 480
    screen = -1
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    White = (255, 255, 255)
    
    instructionsFont = pygame.font.SysFont(None, 36)
    instructionsLabel = instructionsFont.render("Instructions", 2, Red)
    windowSurface.fill(Black)
    windowSurface.blit(instructionsLabel, (0.35*windowWidth, 0.02*windowHeight))
    controlsFont = pygame.font.SysFont(None, 36)
    controlsLabel1 = controlsFont.render("A and D keys, or arrow keys: Move Left/Right", 2, White)
    windowSurface.blit(controlsLabel1, (0.02*windowWidth, 0.1*windowHeight))
    controlsLabel2 = controlsFont.render("W key or Up arrow key: Jump", 2, White)
    windowSurface.blit(controlsLabel2, (0.02*windowWidth, 0.15*windowHeight))
    controlsLabel3 = controlsFont.render("Ctrl or Space: Fire bullets", 2, White)
    windowSurface.blit(controlsLabel3, (0.02*windowWidth, 0.2*windowHeight))
    controlsLabel4 = controlsFont.render("Q key: Return to start screen", 2, White)
    windowSurface.blit(controlsLabel4, (0.02*windowWidth, 0.25*windowHeight))
    controlsLabel5 = controlsFont.render("E key: Next level (only after all enemies are dead)", 2, White)
    windowSurface.blit(controlsLabel5, (0.02*windowWidth, 0.3*windowHeight))
    goalLabel1 = controlsFont.render("Fight your way through all the enemies and progress", 2, White)
    windowSurface.blit(goalLabel1, (0.02*windowWidth, 0.6*windowHeight))
    goalLabel2 = controlsFont.render("through the levels while keeping your health as high", 2, White)
    windowSurface.blit(goalLabel2, (0.02*windowWidth, 0.7*windowHeight))
    goalLabel3 = controlsFont.render("as possible!", 2, White)
    windowSurface.blit(goalLabel3, (0.02*windowWidth, 0.8*windowHeight))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == ord('q')):
                runStartScreen()
    pygame.quit()

def gameOver():
    windowWidth = 640
    windowHeight = 480
    screen = -1
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    # colors
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    gameOverFont = pygame.font.SysFont(None, 60)
    gameOverLabel = gameOverFont.render("GAME OVER! :(", 3, Red)
    windowSurface.blit(gameOverLabel, (0.25*windowWidth, 0.45*windowHeight))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == ord('q')):
                runStartScreen()
    pygame.quit()
                
def runLevelOne():
    # set up initial variables
    windowWidth = 640
    windowHeight = 480
    groundLevel = int(windowHeight * 0.9)
    platform1 = int(1.95*groundLevel - windowHeight)
    platform2 = int(platform1 * 0.8)
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    counter = 1
    secondsPerFrame = 1.0 / 35

    # set colors, movement variables, and other constants
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    LightBlue = (0, 180, 255)
    Yellow = (255, 255, 0)
    Orange = (255, 165, 0)
    Brown = (165, 42, 42)

    x = 30
    y = groundLevel-30
    vx = 0
    vy = 0
    g = 1
    onGround = False
    jumping = False
    facingLeft = False
    level = 1
    score1 = 0
    health = 40

    # set up platforms (stored in a list)
    platforms = [(0, groundLevel, windowWidth),
                (0.2 * windowWidth, platform1, 0.6 * windowWidth),
                (0.4 * windowWidth, platform2, 0.2 * windowWidth)]

    # set up bullets
    bullets = []

    # set up enemies
    enemies = [[int(0.6*windowWidth), groundLevel-30, -8, 0,
                int(0.2*windowWidth+30), windowWidth-30, 2],
                [int(0.5*windowWidth), platform1-30, 6, 0,
                 int(0.2*windowWidth+30), int(0.8*windowWidth-30), 2]]

    # Draws the background and scenery features
    def drawScenery():
        # draw background
        windowSurface.fill(LightBlue)
        # draw the ground
        pygame.draw.rect(windowSurface, Green,
                         (0, groundLevel, windowWidth, windowHeight))
            
    # make enemies move
    def moveEnemies():
        for enemy in enemies:
            enemy[0] += enemy[2]
            if (enemy[0] >= enemy[5] - enemy[2] or
                enemy[0] <= enemy[4] - enemy[2]):
                # when enemy reaches path boundary
                enemy[2] *= -1 # changes direction
                    
    # draw platforms
    def drawPlatforms():
        pygame.draw.rect(windowSurface, Brown, (0.2*windowWidth, platform1, 0.2*windowWidth, groundLevel-platform1))
        pygame.draw.rect(windowSurface, Brown, (0.6*windowWidth, platform1, 0.2*windowWidth, groundLevel-platform1))
        pygame.draw.rect(windowSurface, Brown, (0.4*windowWidth, platform2, 0.2*windowWidth, groundLevel-platform2))
        pygame.draw.line(windowSurface, Black, (0.2*windowWidth, platform1), (0.8*windowWidth, platform1), 3)
        pygame.draw.line(windowSurface, Black, (0.4*windowWidth, platform2), (0.6*windowWidth, platform2), 3)
        pygame.draw.line(windowSurface, Black, (0, groundLevel), (windowWidth, groundLevel), 3)

    # Updates the enemies list by removing all dead enemies, keeps living ones
    def filterDeadEnemies(enemies):
        livingEnemies = []
        for enemy in enemies:
            if (enemy[6] > 0): # alive
                livingEnemies += [enemy]
        return livingEnemies

    # Draws the headings at the top of the screen
    def drawTextHeaders():
        levelFont = pygame.font.SysFont("Comic Sans MS", 24)
        levelLabel = levelFont.render("Level: " + str(level), 1, Black)
        windowSurface.blit(levelLabel, (0.01*windowWidth, 0.01*windowHeight))
        scoreFont = pygame.font.SysFont("Comic Sans MS", 24)
        scoreLabel = scoreFont.render("Score: " + str(score1), 1, Black)
        windowSurface.blit(scoreLabel, (0.4*windowWidth, 0.01*windowHeight))
        healthFont = pygame.font.SysFont("Comic Sans MS", 24)
        healthLabel = healthFont.render("Health: " + str(health), 1, Black)
        windowSurface.blit(healthLabel, (0.8*windowWidth, 0.01*windowHeight))

    def drawBullets():
        for bullet in bullets:
            pygame.draw.circle(windowSurface, Orange, (bullet[0], bullet[1]),4)
            
    def drawEnemies():
        for enemy in enemies:
            pygame.draw.circle(windowSurface, Red, (enemy[0], enemy[1]), 30)
                
    # run game loop
    while True:
        delayTime = time.clock()
        # check for events
        for event in pygame.event.get():
            if (event.type == KEYDOWN and
                (event.key == K_UP or event.key == ord('w')) and onGround):
                vy = -15
                onGround = False
                jumping = True
            if (event.type == KEYUP and
                (event.key == K_UP or event.key == ord('w')) and
                not onGround and vy < 0):
                vy = 0
                jumping = False
            if (event.type == KEYDOWN and
                (event.key == K_SPACE or event.key == K_LCTRL)):
                bullets.append((x, y, (1, -1)[facingLeft] * 15))
        pressedKeys = pygame.key.get_pressed()
        if ((pressedKeys[K_LEFT] or pressedKeys[ord('a')]) and x > 30):
            x -= 4
            facingLeft = True
        if ((pressedKeys[K_RIGHT] or pressedKeys[ord('d')]) and
            x < windowWidth-30):
            x += 4
            facingLeft = False
        if (pressedKeys[ord('q')]):
            runStartScreen()
        if (len(enemies) == 0 and pressedKeys[ord('e')]):
            runLevelTwo(score1)
        # compute physics
        newBullets = []
        for bullet in bullets:
            if (-700 < bullet[0] - x < 700):
                newBullets.append((bullet[0]+bullet[2], bullet[1], bullet[2]))
            for enemy in enemies:
                if (-10 < bullet[0] - enemy[0] < 10 and
                    -10 < bullet[1] - enemy[1] < 10):
                    enemy[6] -= 1
                    score1 += 10
            enemies = filterDeadEnemies(enemies)
        bullets = newBullets
        y += vy
        x += vx
        vy = min(vy + g, 15)
        onGround = False
        for platform in platforms:
            if vy > 0 and x >= platform[0] and x <= platform[0] + platform[2]:
                if y + 30 >= platform[1] and y + 30 < platform[1] + vy:
                    y = platform[1] - 30
                    vy = 0
                    onGround = True
                    break
        for enemy in enemies:
            if (-60 < enemy[0] - x < 60 and -60 < enemy[1] - y < 60):
                health -= 1
                if (score1 > 0):
                    score1 -= 1
                if health <= 0:
                    gameOver()
        jumping = jumping and vy < 0
        drawScenery()
        drawPlatforms()
        drawBullets()
        drawEnemies()
        moveEnemies()
        # draw the character
        pygame.draw.circle(windowSurface, Yellow, (x, y), 30)
        # draw text
        drawTextHeaders()
        # draw the window onto the screen
        pygame.display.flip()
        counter += 1
        time.sleep(secondsPerFrame - (time.clock() - delayTime))
    pygame.quit()

def runLevelTwo(score1):
    # set up initial variables
    windowWidth = 640
    windowHeight = 480
    groundLevel = int(windowHeight * 0.9)
    platform1 = int(1.95*groundLevel - windowHeight)
    platform2 = int(platform1 * 0.8)
    platform3 = int(platform1 * 0.6)
    platform4 = int(platform1 * 0.4)
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    counter = 1
    secondsPerFrame = 1.0 / 35

    # set colors, movement variables, and other constants
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    LightBlue = (0, 180, 255)
    Yellow = (255, 255, 0)
    Orange = (255, 165, 0)
    Brown = (165, 42, 42)

    x = 30
    y = groundLevel-30
    vx = 0
    vy = 0
    g = 1
    onGround = False
    jumping = False
    facingLeft = False
    level = 2
    score2 = score1
    health = 40

    # set up platforms (stored in a list)
    platforms = [(0, groundLevel, windowWidth),
                (0.2 * windowWidth, platform1, 0.6 * windowWidth),
                (0.4 * windowWidth, platform2, 0.2 * windowWidth),
                (0, platform3, 0.3 * windowWidth),
                (0.7 * windowWidth, platform3, 0.3 * windowWidth),
                (0.3 * windowWidth, platform4, 0.4 * windowWidth)]

    # set up bullets
    bullets = []

    # set up enemies
    enemies = [[int(0.6*windowWidth), groundLevel-30, -6, 0, 30,
                windowWidth-30, 10],
               [int(0.6*windowWidth), groundLevel-30, 6, 0, 30,
                windowWidth-30, 10],
               [int(0.5*windowWidth), platform1-30, 5, 0,
                int(0.2*windowWidth+30), int(0.8*windowWidth-30), 10],
               [30, platform3-30, 5, 0, 30, int(0.3*windowWidth-30), 10],
               [int(0.7*windowWidth+30), platform3-30, 5, 0,
                int(0.7*windowWidth+30), windowWidth-30, 10],
               [int(0.5*windowWidth), platform4-30, -5, 0,
                int(0.3*windowWidth+30), int(0.7*windowWidth-30), 10]]

    # Draws the background and scenery features
    def drawScenery():
        # draw background
        windowSurface.fill(LightBlue)
        # draw the ground
        pygame.draw.rect(windowSurface, White,
                         (0, groundLevel, windowWidth, windowHeight))
        # draw icy spikes on the ground
        for i in xrange(int(0.05*windowWidth), int(0.31*windowWidth)):
            pygame.draw.line(windowSurface, Black, (5*i, groundLevel),
                             (5*i, groundLevel-10), 3)
            
    # make enemies move
    def moveEnemies():
        for enemy in enemies:
            enemy[0] += enemy[2]
            if (enemy[0] >= enemy[5] - enemy[2] or
                enemy[0] <= enemy[4] - enemy[2]):
                # when enemy reaches path boundary
                enemy[2] *= -1 # changes direction
                    
    # draw platforms
    def drawPlatforms():
        for platform in platforms:
            pygame.draw.line(windowSurface, Black, (platform[0], platform[1]),
                             (platform[0]+platform[2], platform[1]), 5)

    # Updates the enemies list by removing all dead enemies, keeps living ones
    def filterDeadEnemies(enemies):
        livingEnemies = []
        for enemy in enemies:
            if (enemy[6] > 0): # alive
                livingEnemies += [enemy]
        return livingEnemies

    # Draws the headings at the top of the screen
    def drawTextHeaders():
        levelFont = pygame.font.SysFont("Comic Sans MS", 24)
        levelLabel = levelFont.render("Level: " + str(level), 1, Black)
        windowSurface.blit(levelLabel, (0.01*windowWidth, 0.01*windowHeight))
        scoreFont = pygame.font.SysFont("Comic Sans MS", 24)
        scoreLabel = scoreFont.render("Score: " + str(score2), 1, Black)
        windowSurface.blit(scoreLabel, (0.4*windowWidth, 0.01*windowHeight))
        healthFont = pygame.font.SysFont("Comic Sans MS", 24)
        healthLabel = healthFont.render("Health: " + str(health), 1, Black)
        windowSurface.blit(healthLabel, (0.8*windowWidth, 0.01*windowHeight))

    def drawBullets():
        for bullet in bullets:
            pygame.draw.circle(windowSurface, Orange, (bullet[0], bullet[1]),4)
            
    def drawEnemies():
        for enemy in enemies:
            pygame.draw.circle(windowSurface, Green, (enemy[0], enemy[1]), 30)

    # run game loop
    while True:
        delayTime = time.clock()
        # check for events
        for event in pygame.event.get():
            if (event.type == KEYDOWN and
                (event.key == K_UP or event.key == ord('w')) and onGround):
                vy = -15
                onGround = False
                jumping = True
            if (event.type == KEYUP and
                (event.key == K_UP or event.key == ord('w')) and
                not onGround and vy < 0):
                vy = 0
                jumping = False
            if (event.type == KEYDOWN and
                (event.key == K_SPACE or event.key == K_LCTRL)):
                bullets.append((x, y, (1, -1)[facingLeft] * 15))
        pressedKeys = pygame.key.get_pressed()
        if ((pressedKeys[K_LEFT] or pressedKeys[ord('a')]) and x > 30):
            x -= 4
            facingLeft = True
        if ((pressedKeys[K_RIGHT] or pressedKeys[ord('d')]) and
            x < windowWidth-30):
            x += 4
            facingLeft = False
        if (pressedKeys[ord('q')]):
            runStartScreen()
        if (len(enemies) == 0 and pressedKeys[ord('e')]):
            runLevelThree(score2)
        if (x >= 0.25*windowWidth and y == groundLevel-30):
                health -= 1 # spikes injure player
                if (score2 > 0):
                    score2 -= 1
                if (health <= 0):
                    gameOver()
        # compute physics
        newBullets = []
        for bullet in bullets:
            if (-700 < bullet[0] - x < 700):
                newBullets.append((bullet[0]+bullet[2], bullet[1], bullet[2]))
            for enemy in enemies:
                if (-10 < bullet[0] - enemy[0] < 10 and
                    -10 < bullet[1] - enemy[1] < 10):
                    enemy[6] -= 1
                    score2 += 10
            enemies = filterDeadEnemies(enemies)
        bullets = newBullets
        y += vy
        x += vx
        vy = min(vy + g, 15)
        onGround = False
        for platform in platforms:
            if vy > 0 and x >= platform[0] and x <= platform[0] + platform[2]:
                if y + 30 >= platform[1] and y + 30 < platform[1] + vy:
                    y = platform[1] - 30
                    vy = 0
                    onGround = True
                    break
        for enemy in enemies:
            if (-60 < enemy[0] - x < 60 and -60 < enemy[1] - y < 60):
                health -= 1
                if (score2 > 0):
                    score2 -= 1
                if health <= 0:
                    gameOver()
        jumping = jumping and vy < 0
        drawScenery()
        drawPlatforms()
        drawBullets()
        drawEnemies()
        moveEnemies()
        # draw the character
        pygame.draw.circle(windowSurface, Yellow, (x, y), 30)
        # draw text
        drawTextHeaders()
        # draw the window onto the screen
        pygame.display.flip()
        counter += 1
        time.sleep(secondsPerFrame - (time.clock() - delayTime))
    pygame.quit()

def runLevelThree(score2):
    # set up initial variables
    windowWidth = 640
    windowHeight = 480
    groundLevel = int(windowHeight * 0.9)
    platform1 = int(windowHeight * 0.8)
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    counter = 1
    secondsPerFrame = 1.0 / 35

    # set colors, movement variables, and other constants
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    LightBlue = (0, 180, 255)
    Yellow = (255, 255, 0)
    Orange = (255, 165, 0)
    Brown = (165, 42, 42)

    x = 30
    y = groundLevel-30
    vx = 0
    vy = 0
    g = 1
    onGround = False
    jumping = False
    facingLeft = False
    level = 3
    score3 = score2
    health = 40

    # set up platforms (stored in a list)
    platforms = [(0, groundLevel, windowWidth),
                 (0.4*windowWidth, platform1, 0.2*windowWidth)]

    # set up bullets
    bullets = []

    # set up enemies
    enemies = [[int(0.5*windowWidth), groundLevel-30, -10,
                0, 30, windowWidth-30, 20]]

    # Draws the background and scenery features
    def drawScenery():
        # draw background
        windowSurface.fill(LightBlue)
        # draw the ground
        pygame.draw.rect(windowSurface, Green,
                         (0, groundLevel, windowWidth, windowHeight))
            
    # make enemies move
    def moveEnemies():
        for enemy in enemies:
            enemy[0] += enemy[2]
            if (enemy[0] >= enemy[5] - enemy[2] or
                enemy[0] <= enemy[4] - enemy[2]):
                # when enemy reaches path boundary
                enemy[2] *= -1 # changes direction

    # draw platforms
    def drawPlatforms():
        for platform in platforms:
            pygame.draw.line(windowSurface, Black,
                             (platform[0], platform[1]),
                             (platform[0]+platform[2], platform[1]), 5)

    # Updates the enemies list by removing all dead enemies, keeps living ones
    def filterDeadEnemies(enemies):
        livingEnemies = []
        for enemy in enemies:
            if (enemy[6] > 0): # alive
                livingEnemies += [enemy]
        return livingEnemies

    # Draws the headings at the top of the screen
    def drawTextHeaders():
        levelFont = pygame.font.SysFont("Comic Sans MS", 24)
        levelLabel = levelFont.render("Level: " + str(level), 1, Black)
        windowSurface.blit(levelLabel, (0.01*windowWidth, 0.01*windowHeight))
        scoreFont = pygame.font.SysFont("Comic Sans MS", 24)
        scoreLabel = scoreFont.render("Score: " + str(score3), 1, Black)
        windowSurface.blit(scoreLabel, (0.4*windowWidth, 0.01*windowHeight))
        healthFont = pygame.font.SysFont("Comic Sans MS", 24)
        healthLabel = healthFont.render("Health: " + str(health), 1, Black)
        windowSurface.blit(healthLabel, (0.8*windowWidth, 0.01*windowHeight))

    def drawBullets():
        for bullet in bullets:
            pygame.draw.circle(windowSurface, Orange, (bullet[0], bullet[1]),4)
            
    def drawEnemies():
        for enemy in enemies:
            pygame.draw.circle(windowSurface, Blue, (enemy[0], enemy[1]), 30)
                
    # run game loop
    while True:
        delayTime = time.clock()
        # check for events
        for event in pygame.event.get():
            if (event.type == KEYDOWN and
                (event.key == K_UP or event.key == ord('w')) and onGround):
                vy = -15
                onGround = False
                jumping = True
            if (event.type == KEYUP and
                (event.key == K_UP or event.key == ord('w')) and
                not onGround and vy < 0):
                vy = 0
                jumping = False
            if (event.type == KEYDOWN and
                (event.key == K_SPACE or event.key == K_LCTRL)):
                bullets.append((x, y, (1, -1)[facingLeft] * 15))
        pressedKeys = pygame.key.get_pressed()
        if ((pressedKeys[K_LEFT] or pressedKeys[ord('a')]) and x > 30):
            x -= 4
            facingLeft = True
        if ((pressedKeys[K_RIGHT] or pressedKeys[ord('d')]) and
            x < windowWidth-30):
            x += 4
            facingLeft = False
        if (pressedKeys[ord('q')]):
            runStartScreen()
        if (len(enemies) == 0 and pressedKeys[ord('e')]):
            congratulations(score3)
        # compute physics
        newBullets = []
        for bullet in bullets:
            if (-700 < bullet[0] - x < 700):
                newBullets.append((bullet[0]+bullet[2], bullet[1], bullet[2]))
            for enemy in enemies:
                if (-10 < bullet[0] - enemy[0] < 10 and
                    -10 < bullet[1] - enemy[1] < 10):
                    enemy[6] -= 1
                    score3 += 10
            enemies = filterDeadEnemies(enemies)
        bullets = newBullets
        y += vy
        x += vx
        vy = min(vy + g, 15)
        onGround = False
        for platform in platforms:
            if vy > 0 and x >= platform[0] and x <= platform[0] + platform[2]:
                if y + 30 >= platform[1] and y + 30 < platform[1] + vy:
                    y = platform[1] - 30
                    vy = 0
                    onGround = True
                    break
        for enemy in enemies:
            if (-60 < enemy[0] - x < 60 and -60 < enemy[1] - y < 60):
                health -= 2
                if (score3 > 0):
                    score3 -= 1
                if health <= 0:
                    gameOver()
        jumping = jumping and vy < 0
        drawScenery()
        drawPlatforms()
        drawBullets()
        drawEnemies()
        moveEnemies()
        # draw the character
        pygame.draw.circle(windowSurface, Yellow, (x, y), 30)
        # draw text
        drawTextHeaders()
        # draw the window onto the screen
        pygame.display.flip()
        counter += 1
        time.sleep(secondsPerFrame - (time.clock() - delayTime))
    pygame.quit()

def congratulations(score3):
    windowWidth = 640
    windowHeight = 480
    screen = -1
    score = 0
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    # colors
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    congratsFont = pygame.font.SysFont(None, 60)
    congratsLabel = congratsFont.render("CONGRATULATIONS!!!", 3, Red)
    windowSurface.blit(congratsLabel, (0.15*windowWidth, 0.35*windowHeight))
    winnerFont = pygame.font.SysFont(None, 36)
    winnerLabel = winnerFont.render("You've won the game with " + str(score3) +
                                    " points! :-)", 3, Red)
    windowSurface.blit(winnerLabel, (0.1*windowWidth, 0.5*windowHeight))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == ord('q')):
                runStartScreen()
    pygame.quit()

def runStartScreen():
    windowWidth = 640
    windowHeight = 480
    screen = -1
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Speedy Reflex Shooters')
    # colors
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    titleFont = pygame.font.SysFont(None, 60)
    titleLabel = titleFont.render("Speedy Reflex Shooters", 3, Red)
    windowSurface.blit(titleLabel, (0.15*windowWidth, 0.35*windowHeight))
    subFont = pygame.font.SysFont(None, 36)
    subLabel = subFont.render("Press 1 to start, 2 for instructions", 2, Red)
    windowSurface.blit(subLabel, (0.15*windowWidth, 0.5*windowHeight))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == ord('q')):
                runStartScreen()
            if (event.type == KEYDOWN and event.key == ord('1')):
                runLevelOne()
            if (event.type == KEYDOWN and event.key == ord('2')):
                showInstructions()
    pygame.quit()
    
runStartScreen()
