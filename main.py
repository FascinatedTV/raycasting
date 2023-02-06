import pygame
import math
import time
import sys

HEIGHT = 512
WIDTH = 1024

CAST_HEIGHT = 300

PI = 3.14159
PI2 = PI / 2
PI3 = 3 * PI / 2
DEG = PI / 180

pygame.init()
pygame.display.set_caption("Raycaster")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

playerX, playerY = 320, 240
playerAngle, playerDx, playerDy = 0, 5, 0
movementSpeed = 3

board = [
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 1, 1, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1,
]

tileSize = 64

def drawPlayer():
    pygame.draw.circle(screen, (255, 255, 0), (playerX, playerY), 5)
    pygame.draw.line(screen, (255, 0, 0), (playerX, playerY), (playerX + playerDx * movementSpeed, playerY + playerDy * movementSpeed ))

def drawBoard():
    for i in range(0, len(board)):
        if board[i] == 1:
            pygame.draw.rect(screen, (255, 255, 255), (i % 8 * tileSize + 1, i // 8 * tileSize + 1, tileSize - 1, tileSize - 1))
        else:
            pygame.draw.rect(screen, (25, 25, 25), (i % 8 * tileSize + 1, i // 8 * tileSize + 1, tileSize - 1, tileSize - 1))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def raycast():
    lines = []
    rayCount = 75
    ra = playerAngle - rayCount // 2 * DEG
    if ra < 0: ra += 2 * PI
    if ra > 2 * PI: ra -= 2 * PI


    for r in range(rayCount):
        mx = my = mp = dof = 0
        rx = ry = xo = yo = 0

        aTan = -1 / math.tan(ra + .0000001)
        Tan = -1 * math.tan(ra - .0000001)
        
        distH, hx, hy = math.inf, playerX, playerY

        # Check Horizontal Lines
        if ra > PI: 
            ry = math.floor(playerY / tileSize) * tileSize - 0.0001
            rx = (playerY - ry) * aTan + playerX
            yo = -tileSize
            xo = -yo * aTan
        if ra > 0 and ra < PI:
            ry = math.floor(playerY / tileSize) * tileSize + tileSize
            rx = (playerY - ry) * aTan + playerX
            yo = tileSize
            xo = -yo * aTan
        if ra == 0 or ra == PI:
            rx = playerX
            ry = playerY
            dof = 8
        while dof < 8:
            mx = math.floor(rx / tileSize)
            my = math.floor(ry / tileSize)
            mp = my * 8 + mx
            if mp > 0 and mp < 64 and board[mp] == 1:
                hx = rx
                hy = ry
                distH = distance(playerX, playerY, hx, hy)
                dof = 8
            else:
                rx += xo
                ry += yo
                dof += 1

        # pygame.draw.line(screen, (0, 255, 255), (playerX, playerY), (rx, ry))

        # Check Vertical Lines
        dof = 0
        distV, vx, vy = math.inf, playerX, playerY

        if ra > PI2 and ra < PI3: 
            rx = math.floor(playerX / tileSize) * tileSize - 0.0001
            ry = (playerX - rx) * Tan + playerY
            xo = -tileSize
            yo = -xo * Tan
        if ra < PI2 or ra > PI3:
            rx = math.floor(playerX / tileSize) * tileSize + tileSize
            ry = (playerX - rx) * Tan + playerY
            xo = tileSize
            yo = -xo * Tan
        if ra == PI2 or ra == PI3:
            ry = playerY
            rx = playerX
            dof = 8
        while dof < 8:
            mx = math.floor(rx / tileSize)
            my = math.floor(ry / tileSize)
            mp = my * 8 + mx
            if mp > 0 and mp < 64 and board[mp] == 1:
                vx = rx
                vy = ry
                distV = distance(playerX, playerY, vx, vy)
                dof = 8
            else:
                rx += xo
                ry += yo
                dof += 1

        rx, ry, distT, color =  (vx, vy, distV, (255, 0, 0)) if distV < distH else (hx, hy, distH, (150, 0, 0)) 
        pygame.draw.line(screen, (0, 255, 0), (playerX, playerY), (rx, ry))
        
        ca = playerAngle - ra
        # if ca < 0: ca += 2 * PI
        # if ca > 2 * PI: ca -= 2 * PI
        distT *= math.cos(ca)


        height = min( 64 / distT * 277, HEIGHT)
        offset = 70 - height / 2
        pygame.draw.line(screen, color, (WIDTH // 2 + (r + 1) * WIDTH / 2 / rayCount, offset + 100), (WIDTH / 2 + (r + 1) * WIDTH // 2 / rayCount, height + 100), 8)
        
        ra += DEG
        if ra < 0: ra += 2 * PI
        if ra > 2 * PI: ra -= 2 * PI
        



while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerY += playerDy * .1
        playerX += playerDx * .1
    if keys[pygame.K_s]:
        playerY -= playerDy * .1
        playerX -= playerDx * .1
    if keys[pygame.K_a]:
        playerAngle -= .005
        if playerAngle < 0: playerAngle += 2 * PI
        playerDx = movementSpeed * math.cos(playerAngle)
        playerDy = movementSpeed * math.sin(playerAngle)
    if keys[pygame.K_d]:
        playerAngle += .005
        if playerAngle > 2 * PI: playerAngle -= 2 * PI
        playerDx = movementSpeed * math.cos(playerAngle)
        playerDy = movementSpeed * math.sin(playerAngle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    drawBoard()
    drawPlayer()
    raycast()
    

    pygame.display.flip()