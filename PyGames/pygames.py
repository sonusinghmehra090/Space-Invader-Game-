import pygame 
import random
import math
from pygame import mixer

pygame.init()
# display --> caption logo screen size
pygame.display.set_caption("space Invader")
icon=pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)

screen=pygame.display.set_mode((800,600))

#background-music
mixer.music.load("backgroundmusic.wav")
mixer.music.play()
# player
playerImg=pygame.image.load("spaceship.png")
playerX=400  # 800/2
playerY=500
player_change=0

def player(x,y):
    screen.blit(playerImg,(x,y))

# bullets 
bulletImg=pygame.image.load("bullet.png")
bulletX=400
bulletY=500
bullet_change=30
bullet_state="ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+19,y+10))

# enemies
enemyImg=[]
enemyX=[]
enemyY=[]
enemy_change=[]
n_enemies=5
for i in range(n_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(2,740))
    enemyY.append(random.randint(2,100))
    enemy_change.append(random.uniform(0.1,0.5))

def enemy(x,y):
    screen.blit(enemyImg[i],(x,y))
#finding the distance(euler distance) between bullet and alien  d=sqrt((bulletX-enemyX)^2+(bulletY-enemyY)^2)

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(bulletX-enemyX,2)+math.pow(bulletY-enemyY,2))
    if distance<25:   # enemy img is 64px --> on approx alien img --> 55px 
        return True
    else:
        False

# adding a score bar inside our screen
score_val=0
score_font=pygame.font.Font('freesansbold.ttf', 32)
scoreX=10
scoreY=10
def show_score(x,y):
    # score_font will render the text
    score=score_font.render("score :" + str(score_val),True,(255,255,255))  # string concatenation 
    screen.blit(score,(x,y))

# game over text
over=pygame.font.Font("freesansbold.ttf",128)
GoverX=50
GoverY=200
def show_game_over(x,y):
    game_over=over.render("Game Over",True,(43, 115, 251))
    screen.blit(game_over,(x,y))


running=True
while running:
    
    backgroundImg=pygame.image.load("background.jpg")
    screen.blit(backgroundImg,(0,0))

    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            running=False
        
        if events.type==pygame.KEYDOWN:
            if events.key==pygame.K_LEFT:
                player_change=-7
            if events.key==pygame.K_RIGHT:
                player_change=7
            if events.key==pygame.K_SPACE:
                # adding laser music
                bulletsound=mixer.Sound("lasershot.wav")
                bulletsound.play()
                bulletX=playerX
                fire_bullet(bulletX,bulletY)
        if events.type==pygame.KEYUP:
            if events.key==pygame.K_LEFT or events.key==pygame.K_RIGHT:
                player_change=0

    #if collision happened 
    

    #player boundary
    if playerX >= 740:
        playerX = 740

    elif playerX<=0:
        playerX=0

    #bullet boundary
    if bulletY<=0:
        bulletY=500
        bullet_state="ready"

    #enemies boundary
    for i in range(n_enemies):
        if enemyY[i]>=480:
            show_game_over(GoverX,GoverY)
            player_change=0
            break
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision is True:
            expo=mixer.Sound("explostion.wav")
            expo.play()
            bulletY=500
            bullet_state="ready"
            score_val+=1
            enemyX[i]=random.randint(2,750)
            enemyY[i]=random.randint(2,150)

        if enemyX[i]>=750:
            enemy_change[i]=-1
        if enemyX[i]<=0:
            enemy_change[i] =1

        #enemy call
        enemyX[i] +=enemy_change[i]
        enemyY[i] +=random.uniform(0.2,1)
        enemy(enemyX[i],enemyY[i])

    #bullet call in loop
    if bullet_state=="fire":
        bulletY-=bullet_change
        fire_bullet(bulletX,bulletY)


    #player call
    playerX +=player_change
    player(playerX,playerY)

    #score call
    show_score(scoreX,scoreY)

    
    pygame.display.update()
