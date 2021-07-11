import pygame
import random 
import math
from pygame import mixer
#intialize the pygame
pygame.init()

#create a screen
screen=pygame.display.set_mode((800,600))

#caption and icon 
pygame.display.set_caption("Space Invader")
icon=pygame.image.load('logo.png')
pygame.display.set_icon(icon)

#background img
background=pygame.image.load('background.png')
#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10;
textY=10
#game_over
over_font=pygame.font.Font('freesansbold.ttf',64)

#sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

#player
playerImg=pygame.image.load('spaceship.png')
playerX=370
playerY=480
playerX_change=0

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[];
num_of_enemy=6
for i in range(num_of_enemy):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(4)
	enemyY_change.append(40)

#bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

def show_score(x,y):
	score=font.render("Score : "+str(score_value),True,(255,255,255))
	screen.blit(score,(x,y))
def game_over_text():
	over_text=over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_text,(200,250))
	
def player(x,y):
	screen.blit(playerImg,(x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state="fire"
	screen.blit(bulletImg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
	if distance<27:
		return True
	return False
running =True
while running:
	screen.fill((0,0,0))
	screen.blit(background,(0,0))
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running=False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT:
				playerX_change=-4
			if event.key==pygame.K_RIGHT:
				playerX_change=4
			if event.key==pygame.K_SPACE:
				if bullet_state is "ready":
					bulletsound=mixer.Sound("laser.wav")
					bulletsound.play()
					bulletX=playerX
					fire_bullet(bulletX,bulletY)
		if event.type==pygame.KEYUP:
			if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
				playerX_change=0
	#updating position of player
	playerX+=playerX_change
	
	#edge case 
	if (playerX<=0):
		playerX=0
	if (playerX>=736):
		playerX=736
			
	player(playerX,playerY)
	
	playerX+=playerX_change
	
	#edge case
	for i in range(num_of_enemy):
		#game over 
		if enemyY[i]>440:
			for j in range(num_of_enemy):
				enemyY[j]=2000
			game_over_text()
			break
		enemyX[i]+=enemyX_change[i];
		if (enemyX[i]<=0):
			enemyX[i]=0
			enemyX_change[i]=4
			enemyY[i]+=enemyY_change[i]
		if (enemyX[i]>=736):
			enemyX[i]=736
			enemyX_change[i]=-4
			enemyY[i]+=enemyY_change[i]
		#collision 
		collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			#explosionsound=mixer.Sound("explosion.wav")
			#explosionsound.play()
			bulletY=480
			bullet_state="ready"
			score_value+=1
			enemyX[i]=random.randint(0,735)
			enemyY[i]=random.randint(50,150)
		enemy(enemyX[i],enemyY[i],i)
	#bullet movement
	if bulletY<=0:
		bulletY=480
		bullet_state="ready"
	
	if bullet_state is "fire":
		fire_bullet(bulletX,bulletY)
		bulletY-=bulletY_change
	show_score(textX,textY)
	pygame.display.update()
