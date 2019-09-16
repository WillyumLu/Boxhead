import pygame, sys, glob, random, math
from pygame import *
from random import *
pygame.init()
w = 850
h = 750
screen = pygame.display.set_mode((w, h), 0, 32)

#image import
PlayerBullet = pygame.image.load("Bullet.png")
#sndGunfire = pygame.mixer.Sound(#_#_#_#)
HealthBar = pygame.image.load("HealthBar5.png")
Health = 5
RunGame = True
WalkImage = 1

class Player:
	screen.fill((255,255,255))
	def __init__(self):
		if WalkImage == 1:
			self.image = pygame.image.load("PlayerM4.png")
		elif WalkImage == -1:
			self.image = pygame.image.load("PlayerM4.2.png")
		self.x = 425
		self.y = 375
		self.xVelocity = 0
		self.yVelocity = 0
		self.nextx = self.x+self.xVelocity
		self.nexty = self.y+self.yVelocity
		self.direction = ""
		
	def move(self):
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
		screen.blit(self.image, (self.x,self.y))
			
	def collision(self, ):
		self.xVelocity = 0
		self.yVelocity = 0
		
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
		return self.x
	def gety(self):
		return self.y
	def getnextx(self):
		return self.nextx
	def getnexty(self):
		return self.nexty

William = Player()


while RunGame == True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			#if event.key == K_SPACEKEY:
				#BulletList.append(Bullet())
				#Bullet.shoot #add bullet to screen/list
			#else:
				#Player.move
			WalkImage = WalkImage*-1
			if event.type == pygame.QUIT:
				RunGame = False
			if event.key == K_RIGHT:
				William.direction = "right"
			if event.key == K_LEFT:
				William.direction = "left"
			if event.key == K_UP:
				William.direction = "up"
			if event.key == K_DOWN:
				William.direction = "down"
		elif event.type == pygame.QUIT:
			RunGame = False
	pygame.display.update()		
	William.move()
	William.update
	print William.getx(), William.getnextx()

