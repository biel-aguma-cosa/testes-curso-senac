import pygame
import random
import math
import os

dir = os.path.realpath(os.path.dirname(__file__))

bird = pygame.transform.scale(pygame.image.load(os.path.join(dir,'pasro.png')),(40,40))
post_0 = pygame.transform.scale(pygame.image.load(os.path.join(dir,'poste.png')),(60,320))
post_1 = pygame.transform.rotate(post_0,180)
sky_0  = pygame.transform.scale(pygame.image.load(os.path.join(dir,'chao.png'))  ,(602,400))
sky_1  = pygame.transform.flip(sky_0,True,False)

running = True
dt = 0

clock = pygame.Clock()
screen = pygame.display.set_mode((600,400))
pygame.init()

font = pygame.font.Font(pygame.font.match_font('consolas'),20)

try:
    with open(os.path.join(dir,'hs.data'),'r') as save_file:
        HIGH_SCORE = int(save_file.read())
        save_file.close()
except:
    with open(os.path.join(dir,'hs.data'),'w') as save_file:
        save_file.write('0')
        save_file.close()
    HIGH_SCORE = 0

PAUSED = True
SCORE = 0
GAP = 120

bird.set_colorkey('white')

player = pygame.sprite.Sprite()
player.rect  = pygame.rect.Rect(100,200,40,40)
player.radius = 20
player.image = bird.convert_alpha()

y_speed = 0

sky_rect = [
    pygame.rect.Rect(0  ,0,600,400),
    pygame.rect.Rect(600,0,600,400)
    ]

pipes = [
    [pygame.rect.Rect(600,0,60,400),pygame.rect.Rect(600,0,60,400)],
    [pygame.rect.Rect(900,0,60,400),pygame.rect.Rect(900,0,60,400)]
]
passed = [False,False]

def collide_circle_rect(sprite,rect):
    closest_x = max(rect.left,min(sprite.rect.centerx,rect.right ))
    closest_y = max(rect.top ,min(sprite.rect.centery,rect.bottom))
    distance = math.hypot(closest_x-sprite.rect.centerx,closest_y-sprite.rect.centery)
    return distance < sprite.radius

pipes[0][0].bottom = random.randint(0,400-(GAP+10))
pipes[1][0].bottom = random.randint(0,400-(GAP+10))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                y_speed = -200
                if PAUSED:
                    SCORE = 0
                    pipes[0][0].bottom = random.randint(0,400-(GAP+10))
                    pipes[1][0].bottom = random.randint(0,400-(GAP+10))
                    pipes[0][0].left = 600
                    pipes[1][0].left = 900
                    player.rect.topleft = 100, 200
                    PAUSED = False
    screen.fill('black')


    if not PAUSED:
        y_speed += 5
        player.rect.top += y_speed*dt

        sky_rect[0].left -= 1
        sky_rect[1].left -= 1
        if sky_rect[0].right < 0:
            sky_rect[0].left = 600
        if sky_rect[1].right < 0:
            sky_rect[1].left = 600

        for i, pair in enumerate(pipes):
            if pair[0].right < 0:
                passed[i] = False
                pair[0].bottom = random.randint(0,400-(GAP+10))
                pair[0].left = 601

            pair[0].left -= 100*dt
            pair[1].topleft = (pair[0].left,pair[0].bottom+GAP)

            if collide_circle_rect(player,pair[0]) or collide_circle_rect(player,pair[1]):
                PAUSED = True
            elif player.rect.left > pair[0].right and not passed[i]:
                SCORE += 1
                passed[i] = True
    if player.rect.top > 400:
        PAUSED = True

    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
        with open(os.path.join(dir,'hs.data'),'w') as save_file:
            save_file.write(str(HIGH_SCORE))
            save_file.close()

    screen.blit(sky_0,sky_rect[0])
    screen.blit(sky_1,sky_rect[1])

    screen.blit(post_1,(pipes[0][0].left,pipes[0][0].bottom-320))
    screen.blit(post_1,(pipes[1][0].left,pipes[1][0].bottom-320))

    screen.blit(post_0,pipes[0][1])
    screen.blit(post_0,pipes[1][1])

    screen.blit(player.image,player.rect)
    screen.blit(font.render(f'HIGH SCORE: {HIGH_SCORE}',False,'white'),(10,10))
    screen.blit(font.render(f'     SCORE: {SCORE}',False,'white'),(10,30))
    
    pygame.display.flip()
    dt = clock.tick(60)/1000