import pygame
from pygame.sprite import Sprite

#Create a class that takes two arguments: the self reference and the screen that the ship will be drawn on:
class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		"""Initialize the ship and set its starting postion."""
		super(Ship,self).__init__()

		#Initialize the attributes:
		self.screen = screen
		self.ai_settings = ai_settings

		#Load the image and get its 'rect' (rectangle - position). To load the image we'll use the 'pygame.image.load()' function.
		#This function returns a surface that represent the ship - store this in self.image:
		self.image = pygame.image.load('images/ship.bmp')
		#Once the image is loaded use the 'get_rect()' function to access the surface's rect attribute:
		self.rect = self.image.get_rect()
		#Store the screen's rect:
		self.screen_rect = screen.get_rect()

		#Make sure the ship starts in the bottom center of the screen.
		#Make the x-coordinate of the ship's center match the x-coordinate of the center of the screen rect:
		self.rect.centerx = self.screen_rect.centerx
		#Make the y-coordinate of the ship's bottom match the y-coordinate of the bottom of the screen rect:
		self.rect.bottom = self.screen_rect.bottom

		#Store a decimal value for the ship's center (you can only move the rect using integers, not floats)
		self.center = float(self.rect.centerx)

		#Movement flags:
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		"""Update the ship's position based on the movement flag."""
		#Update the ship's center value, not the rect.
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0 :
			self.center -= self.ai_settings.ship_speed_factor
		#Update rect object from the self.center attribute that holds the float value:
		self.rect.centerx = self.center

	#Define a function that will draw the image to the screen at the specified position - self.rect (the rectangle of the ship)
	def blitme(self):
		"""Draw the ship at its correct position"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on the screen."""
		self.center = self.screen_rect.centerx
		

