import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,collision_sprites):
		super().__init__(groups)

		self.idle_sprites = []
		self.idle_sprites.append(pygame.image.load('../graphics/player/idle/1.png'))
		self.idle_sprites.append(pygame.image.load('../graphics/player/idle/2.png'))
		self.idle_sprites.append(pygame.image.load('../graphics/player/idle/3.png'))
		self.idle_sprites.append(pygame.image.load('../graphics/player/idle/4.png'))
		self.sprite = 0
		self.image = self.idle_sprites[self.sprite]


		# self.run_sprites = []
		# self.run_sprites.append(pygame.image.load('../graphics/player/run/1.png'))

		# self.attack_sprites = []
		# self.attack_sprites.append(pygame.image.load('../graphics/player/attack/1.png'))

		# player movement 
		self.direction = pygame.math.Vector2()
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = 16
		self.collision_sprites = collision_sprites
		self.on_floor = False
		self.states = ['idle', 'run', 'jump', 'attack']
		self.state = self.states[0]
		self.rect = self.image.get_rect(topleft=pos)
		self.left = False



	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.left = False
			self.state = self.states[1]
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.left = True
			self.state = self.states[1]
		else:
			self.direction.x = 0
			self.state = self.states[0]

		if keys[pygame.K_SPACE] and self.on_floor:
			self.direction.y = -self.jump_speed

	def animate(self, state, direction):
		if state == 'idle':
			self.sprite += 0.18
			if self.sprite >= len(self.idle_sprites):
				self.sprite = 0
			self.image = self.idle_sprites[int(self.sprite)]
		if state == 'run':
			pass
		if state == 'jump':
			pass
		if state == 'attack':
			pass

		if direction.x > 0:
			self.image = pygame.transform.flip(self.image, True, False)


	def horizontal_collisions(self):
		for sprite in self.collision_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.direction.x < 0: 
					self.rect.left = sprite.rect.right
				if self.direction.x > 0: 
					self.rect.right = sprite.rect.left

	def vertical_collisions(self):
		for sprite in self.collision_sprites.sprites():
			if sprite.rect.colliderect(self.rect):
				if self.direction.y > 0:
					self.rect.bottom = sprite.rect.top
					self.direction.y = 0
					self.on_floor = True
				if self.direction.y < 0:
					self.rect.top = sprite.rect.bottom
					self.direction.y = 0

		if self.on_floor and self.direction.y != 0:
			self.on_floor = False

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self):
		self.input()
		self.rect.x += self.direction.x * self.speed
		self.horizontal_collisions()
		self.apply_gravity()
		self.vertical_collisions()

		self.animate(self.state, self.direction)
