#William Lu 
#Pygame Boxhead Top-Down Shooter
#A cringy game :-)

import pygame, sys, glob, random, math
from pygame import *
from random import *

pygame.init()
w = 900
h = 637
screen = pygame.display.set_mode((w, h))
Background = pygame.image.load("China.png")
GameOver = pygame.image.load("Game_Over.png ")
Quit = False

#-----------------------------------------------------------------------Start Screen
StartScreen = pygame.image.load("StartScreen.png")
Start = True
myfont = pygame.font.SysFont("monospace", 20)
ContinueLabel = myfont.render("Press SPACE to continue", 1, (0,0,0))
while Start == True:
	screen.blit(StartScreen, (15, 0))
	screen.blit(ContinueLabel, (312,338))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Start = False
			Quit = True
		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE:
				Start = False
	pygame.display.flip()
	
#-----------------------------------------------------------------------Instructions Screen
Instructions = True
ArrowKey = pygame.image.load("ArrowKeys.png")
SpaceKey = pygame.image.load("SpaceKey.png")
ArrowInstruction = myfont.render("Use arrow keys to move around the window", 1, (0,0,0))
SpaceInstruction = myfont.render("Press space key to shoot", 1, (0,0,0))
Red = pygame.Color(255,5,5)
TitleFont = pygame.font.SysFont("monospace", 40, True, False)
TitleInstruction = TitleFont.render("Instructions", 1, (0,0,0))
while Instructions == True:
	if Quit == True:
		Instructions = False
	screen.fill(Red)
	screen.blit(TitleInstruction, (320, 10))
	screen.blit(ArrowKey, (50, 150)) #halfway right edge 370, 320
	screen.blit(SpaceKey, (365, 500)) #halfway right edge 565, 540
	screen.blit(ArrowInstruction, (390, 315))
	screen.blit(SpaceInstruction, (470, 535))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Instructions = False
			Quit = True
		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE:
				Instructions = False
	pygame.display.flip()
	
#-----------------------------------------------------------------------Player Declarations
sndGameover = pygame.mixer.Sound("gameend.flac")
sndPlayerShoot = pygame.mixer.Sound("MachineGun2.wav")
PlayerWalkUp = pygame.image.load("PlayerM4Up.png")
PlayerWalkDown = pygame.image.load("PlayerM4Down.png")
PlayerWalkRight = pygame.image.load("PlayerM4Right.png")
PlayerWalkLeft = pygame.image.load("PlayerM4Left.png")
PlayerWalkUpRight = pygame.image.load("PlayerM4UpRight.png")
PlayerWalkUpLeft = pygame.image.load("PlayerM4UpLeft.png")
PlayerWalkDownRight = pygame.image.load("PlayerM4DownRight.png")
PlayerWalkDownLeft = pygame.image.load("PlayerM4DownLeft.png")
PlayerWalkImage = pygame.image.load("PlayerM4Up.png")
MovingUp = False
MovingDown = False
MovingRight = False
MovingLeft = False
PlayerDirection = "up"
PlayerHealthCurrent = pygame.image.load("HealthBar5.png")
PlayerHealth5 = pygame.image.load("HealthBar5.png")
PlayerHealth4 = pygame.image.load("HealthBar4.png")
PlayerHealth3 = pygame.image.load("HealthBar3.png")
PlayerHealth2 = pygame.image.load("HealthBar2.png")
PlayerHealth1 = pygame.image.load("HealthBar1.png")
PlayerHealthXY = (700, 0)
Health = 5
PxVelocity = 0
PyVelocity = 0
Px = 450
Py = 318.5
Pnx = Px + PxVelocity
Pny = Py + PyVelocity
ZombieCount = -1
ZombieKill = 0
ZombieLoad = True
Level = 10
GG = False

def distance(obj1x, obj2x, obj1y, obj2y):
	# dist formula sqrt((x2-x1)^2+(y2-y1)^2)
	return math.sqrt(math.pow((obj1x-obj2x), 2) + math.pow((obj1y-obj2y), 2))

def turntofaceplayer(X,Y):
	deltax = X - Pnx
	deltay = Y - Pny
	angle = math.atan2(-deltax, -deltay)/math.pi*180.0    
	diff = (angle - 90) %360 #reset at 360
	return 0#diff

def rot_center(image, angle):
	# will only work with SQUARE rects
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#class Zombie
class Zombie:
	def __init__(self):
		self.image = pygame.image.load("HandsomeBlake.png")
		self.imagerot = self.image
		self.x = randrange(0, 850)
		self.y = randrange(0, 2)
		self.xVelocity = 0
		self.yVelocity = 0.3
		self.nextx = self.x + self.xVelocity
		self.nexty = self.y + self.yVelocity
		self.angle = 0
		self.offsetX = self.image.get_width() / 2
		self.offsetY = self.image.get_height() / 2

	def follow(self):
		turn = turntofaceplayer(self.x, self.y)
		self.imagerot = rot_center(self.imagerot, turn)
		if self.x > Pnx + 14:#14 is the offset value
			self.xVelocity = -0.28
			self.x += self.xVelocity
			self.nextx = self.x + self.xVelocity
		if self.x < Pnx + 14:
			self.xVelocity = 0.28
			self.x += self.xVelocity
			self.nextx = self.x + self.xVelocity
		if self.y < Pny + 12:
			self.yVelocity = 0.28
			self.y += self.yVelocity
			self.nexty = self.y + self.yVelocity
		if self.y > Pny + 12:
			self.yVelocity = -0.28
			self.y += self.yVelocity
			self.nexty = self.y + self.yVelocity
		screen.blit(self.imagerot, (self.x, self.y))
		
	def offsetX(self):
		offx = (self.image.get_width() / 2)
		return offx
	def offsetY(self):
		offy = (self.image.get_height() / 2)
		return offy 
	
	def getx(self):
		getx = self.x + 17
		return getx
	def gety(self):
		gety = self.y + 17
		return gety
	def getnextx(self):
		return self.nextx
	def getnexty(self):
		return self.nexty
ZombieList = []

#class Bullet
class Bullet:
	def __init__(self):
		self.image = pygame.image.load("Bullet.png")
		self.x = Pnx+26
		self.y = Pny+20
		if PlayerDirection == "right":
			self.xVelocity = 8
			self.yVelocity = 0
		elif PlayerDirection == "left":
			self.xVelocity = -8
			self.yVelocity = 0
		elif PlayerDirection == "up":
			self.xVelocity = 0
			self.yVelocity = -8
		elif PlayerDirection == "down":
			self.xVelocity = 0
			self.yVelocity = 8
		elif PlayerDirection == "upright":
			#Velocity on x and y is modified so the resultant velocity is ~8.0
			self.xVelocity = 5.657
			self.yVelocity = -5.657
		elif PlayerDirection == "downright":
			self.xVelocity = 5.657
			self.yVelocity = 5.657
		elif PlayerDirection == "downleft":
			self.xVelocity = -5.657
			self.yVelocity = 5.657
		elif PlayerDirection == "upleft":
			self.xVelocity = -5.657
			self.yVelocity = -5.657

	def shoot(self):
		self.x += self.xVelocity
		self.y += self.yVelocity
		screen.blit(self.image, (self.x, self.y))

	def getx(self):
		x = self.x + 2
		return x
	def gety(self):
		y = self.y + 2
		return y
BulletList = []

#fps clock
clock = pygame.time.Clock()
TickCounter = 0

#Game loop
RunGame = True
while RunGame == True:
	if Quit == True:
		RunGame = False
		
	#loop tick counter
	TickCounter += 1
	
	#check for keys
	if GG == False:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					MovingUp = True
					#print "up"
				if event.key == K_DOWN:
					MovingDown = True
					#print "down"
				if event.key == K_RIGHT:
					MovingRight = True
					#print "right"
				if event.key == K_LEFT:
					MovingLeft = True
					#print "left"
				if event.key == K_SPACE:
					BulletList.append(Bullet())
					sndPlayerShoot.play()
					#print "shoot"
			elif event.type == pygame.KEYUP:
				if event.key == K_UP:
					MovingUp = False
				if event.key == K_DOWN:
					MovingDown = False
				if event.key == K_RIGHT:
					MovingRight = False
				if event.key == K_LEFT:
					MovingLeft = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RunGame = False
			
	#orient Player and move Player
	if MovingUp == False and MovingDown == False and MovingRight == True and MovingLeft == False:
		PlayerDirection = "right"
		PlayerWalkImage = PlayerWalkRight
		PxVelocity = 0.8
		PyVelocity = 0
	elif MovingUp == False and MovingDown == False and MovingRight == False and MovingLeft == True:
		PlayerDirection = "left"
		PlayerWalkImage = PlayerWalkLeft
		PxVelocity = -0.8
		PyVelocity = 0
	elif MovingUp == False and MovingDown == True and MovingRight == False and MovingLeft == False:
		PlayerDirection = "down"
		PlayerWalkImage = PlayerWalkDown
		PxVelocity = 0
		PyVelocity = 0.8
	elif MovingUp == True and MovingDown == False and MovingRight == False and MovingLeft == False:
		PlayerDirection = "up"
		PlayerWalkImage = PlayerWalkUp
		PxVelocity = 0
		PyVelocity = -0.8
	elif MovingUp == True and MovingDown == False and MovingRight == True and MovingLeft == False:
		PlayerDirection = "upright"
		PlayerWalkImage = PlayerWalkUpRight
		PxVelocity = 0.5657
		PyVelocity = -0.5657
	elif MovingUp == True and MovingDown == False and MovingRight == False and MovingLeft == True:
		PlayerDirection = "upleft"
		PlayerWalkImage = PlayerWalkUpLeft
		PxVelocity = -0.5657
		PyVelocity = -0.5657
	elif MovingUp == False and MovingDown == True and MovingRight == True and MovingLeft == False:
		PlayerDirection = "downright"
		PlayerWalkImage = PlayerWalkDownRight
		PxVelocity = 0.5657
		PyVelocity = 0.5657
	elif MovingUp == False and MovingDown == True and MovingRight == False and MovingLeft == True:
		PlayerDirection = "downleft"
		PlayerWalkImage = PlayerWalkDownLeft
		PxVelocity = -0.5657
		PyVelocity = 0.5657
	# possibly should be elif ??
	elif MovingUp == False and MovingDown == False and MovingRight == False and MovingLeft == False:
		PxVelocity = 0
		PyVelocity = 0

	Pnx = Px + PxVelocity
	Pny = Py + PyVelocity
	if Pnx < -10 or Pnx > 870:
		PxVelocity = 0
	if Pny < -10 or Pny > 617:
		PyVelocity = 0
	Px += PxVelocity
	Py += PyVelocity
	
	#shoot bullet
	for c in range(0, len(BulletList)):
		BulletList[c].shoot()

	#update zombie
	if TickCounter%20 == 0 and ZombieLoad == True:
		if ZombieCount < Level:
			ZombieList.append(Zombie())
			ZombieCount += 1
		else:
			ZombieLoad = False
	if ZombieKill == Level:
		#NEXT LEVEL image/prompt
		Level += 10
		TickCounter = 0
		ZombieLoad = True
		ZombieCount = -1
		ZombieKill = 0

	for a in range(0, len(ZombieList)-1):
		ZombieList[a].follow()
		#check for collision with Bullet
		for b in range(0, len(BulletList)-1):
			if BulletList[b].getx() > 900 or BulletList[b].getx() < 0:
				BulletList.remove(BulletList[b])
			elif BulletList[b].gety() > 637 or BulletList[b].gety() < 0:
				BulletList.remove(BulletList[b])
			if distance(BulletList[b].getx(), ZombieList[a].getx(), BulletList[b].gety(), ZombieList[a].gety()) < 12.0:
				ZombieList.remove(ZombieList[a])
				ZombieKill += 1
		#check for collision with player                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	for d in range(0,len(ZombieList)-1):
		if distance(Pnx, ZombieList[d].getnextx(), Pny, ZombieList[d].getnexty()) < 12:
			Health -= 1
			ZombieList.remove(ZombieList[d])
			ZombieKill += 1
			
	if Health == 5:
		screen.blit(PlayerHealth5, PlayerHealthXY)
	elif Health == 4:
		screen.blit(PlayerHealth4, PlayerHealthXY)
	elif Health == 3:
		screen.blit(PlayerHealth3, PlayerHealthXY)
	elif Health == 2:
		screen.blit(PlayerHealth2, PlayerHealthXY)
	elif Health == 1:
		screen.blit(PlayerHealth1, PlayerHealthXY)
	elif Health <= 0:
		screen.blit(GameOver, (225,119))
		GG = True
		sndGameover.play()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				Quit = True

	pygame.display.update()	
	screen.blit(Background, (0,0))
	screen.blit(PlayerWalkImage, (Px, Py))
	print ZombieKill, ZombieCount
	clock.tick(60)
