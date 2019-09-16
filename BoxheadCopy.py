import pygame, sys, glob, random, math
from pygame import *
from random import *
pygame.init()
w = 850
h = 750
screen = pygame.display.set_mode((w, h), 0, 32)

#image import
PlayerWalk1 = pygame.image.load("PlayerM4.png")
PlayerWalk2 = pygame.image.load("PlayerM4.2.png")
PlayerBullet = pygame.image.load("Bullet.png")
#sndGunfire = pygame.mixer.Sound(#_#_#_#)
HealthBar = pygame.image.load("HealthBar5.png")
Health = 5
direction = ""
RunGame = True
WalkImage = 1

class Player:
	def __init__(self):
		if WalkImage == 1:
			self.image = pygame.image.load(PlayerWalk1)
		elif WalkImage == -1:
			self.image = pygame.image.load(PlayerWalk2)
		self.x = 425
		self.y = 375
		self.xVelocity = 0
		self.yVelocity = 0
		self.nextx = self.x+self.xVelocity
		self.nexty = self.y+self.yVelocity
		
	def move(self,direction):
		if self.direction == "right":
			self.xVelocity = 1
		elif self.direction == "left":
			self.xVelocity = -1
		elif self.direction == "up":
			self.yVelocity = -1
		elif self.direction == "down":
			self.yVelocity = 1
		else:
			self.xVelocity = 0
			self.yVelocity = 0
		#self.x = self.x + xVelocity
		#self.y = self.y + yVelocity
		#self.nextx = self.x + self.xVelocity
		#self.nexty = self.y + self.yVelocity
		#Rotate image

	def update(self):
		self.x += self.xVelocity
		self.y += self.yVelocity
		self.nextx = self.x+self.xVelocity
		self.nexty =  self.y+self.yVelocity
		WalkImage = WalkImage*-1
		screen.blit(self.image, (self.x,self.y))
			
	def collision(self, ):
		self.xVelocity = 0
		self.yVelocity = 0
		self.update()
		
	def healthdown(self):
		Health -= 1
		if Health == 5:
			HealthBar = pygame.image.load("HealthBar5.png")
		elif Health == 4:
			HealthBar = pygame.image.load("HealthBar4.png")
		elif Health == 3:
			HealthBar = pygame.image.load("HealthBar3.png")
		elif Health == 2:
			HealthBar = pygame.image.load("HealthBar2.png")
		elif Health == 1:
			HealthBar = pygame.image.load("HealthBar1.png")
		elif Health <= 0:
			screen = pygame.fill(0,0,0)
			RunGame = False
			screen.blit("GameOver.jpeg", (100,100)) #location TBD
			
	def getx(self):
		return  self.x
	def gety(self):
		return self.y
	def getnextx(self):
		return self.nextx
	def getnexty(self):
		return self.nexty

class Bullet:
	def __init__(self):
		self.image = pygame.image.load(PlayerBullet)
		self.x = Player.getx
		self.y = Player.gety
		if Player.xVelocity  < 0:
			self.xSpeed = 3
		else:
			self.xSpeed = -3
		if Player.yVelocity < 0:
			self.ySpeed = 3
		else:
			self.ySpeed = -3
		self.nextx = self.x + self.xSpeed
		self.nexty = self.y + self.ySpeed

	def shoot(self):
		#for event in pygame.event.get():
			#if event.type == SPACEKEY:   #maybe should do this in game loop
				#Bullet.shoot
		self.x += xSpeed
		self.y += ySpeed
		self.nextx += self.x
		self.nexty += self.y
		sndGunfire.play()
		screen.blit(self.image, (Player.getnextx, Player.getnexty))
		
	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getnextx(self):
		return self.nextx
	def getnexty(self):
		return self.nexty
		
def RotateImage(image, angle):
	# as angle increases the rotation of the object goes counter clockwise
	# taken from the pygame cookbook
 
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

def AngleDifference(X1, Y1, X2, Y2):
	# X1 and Y1 = object moving towards target
	# X2 and Y2 = object to move to
	return math.degrees(math.atan2(Y1.y-(Y2.y), (X2.x)-X1.x)) #calculates the angle of difference btwn two obj		
		
class Zombies:
	def __init__(self):
		self.image = pygame.image.load(PlayerBullet)
		self.x = randrange(0, 850)
		self.y = randrange(0, 2)
		#follow player

	def follow(self):
		Angle = AngleDifference(self.x, self.y, Player.getnextx, Player.getnexty)
		RotatedArrow = RotateImage(self.image, Angle)
		BlitOffsetX = self.image.get_width()/2
		BlitOffsetY = self.image.get_height()/2
		if self.x > Player.getnextx:
			self.x-=5
		if self.x < Player.getnextx:
			self.x+= 5
		if self.y < Player.getnexty:
			self.y+=5
		if self.y > Player.getnexty:
			self.y-=5
	
	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getnextx(self):
		return self.nextx
	def getnexty(self):
		return self.nexty
				
def Distance(x1,y1,x2,y2):
	dist = math.sqrt((x2.getx - x1.getx)**2 + (y2.gety - y1.getnexty)**2)
	return dist	
		#need a loop to check all the bullets for collision and make them disappear

BulletList = []
BulletCount = 0
ZombieList = []
ZombieCount = 0
RunGame = True

while RunGame == True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == SPACEKEY:
				BulletList.append(Bullet())
				Bullet.shoot #add bullet to screen/list
			else:
				Player.move
			if event.type == pygame.QUIT:
				RunGame = False
			if event.key == K_RIGHT:
				Player.move("right")
			if event.key == K_LEFT:
				Player.move("left")
			if event.key == K_UP:
				Player.move("up")
			if event.key == K_DOWN:
				Player.move("down")
		elif event.type == pygame.QUIT:
			RunGame = False
	#add zombie to screen/list
	
	#check for player collide with zombie
	for index in range(0, len(ZombieList)-1):
		if Distance(Player,ZombieList[index], Player, ZombieList[index]) < 5:
			Player.collision
			Player.healthdown
			ZombieList.remove(ZombieList[index])
	
	#check for bullet hit zombie
	for index1 in range(0, len(BulletList)-1):
		for index2 in range(0, len(ZombieList)-1):
			if Distance(BulletCount[index1],ZombieList[index2],BulletList[index1],ZombieList[index2]) < 5:
				BulletList.remove(BulletList[index1])
				ZombieList.remove(BulletList[index13]) #might need to modify this later
			else:
				ZombieList[index2].follow
