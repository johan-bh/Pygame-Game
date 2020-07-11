import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class for the bullets fired by the rocket ship."""
	def __init__(self,ai_settings,screen,ship):
		super(Bullet, self).__init__()
		self.screen = screen

		#Create a bullet rect at (0,0) and then correct its position. Use the pygame.Rect() class to create the rects. 
		#The class require the x- and y-coordinates of the top left corner of the rect as well as its width and height.
		self.rect = pygame.Rect(0,0, ai_settings.bullet_width, ai_settings.bullet_height)
		#Make sure the center of the ship matches the center of the bullet.
		self.rect.centerx = ship.rect.centerx	
		self.rect.top = ship.rect.top

		#Store the bullet's position as a decimal value.
		self.y  = float(self.rect.y)

		#Store the bullet's color and speed settings:
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		"""Manages the bullet's position as it moves up the screen."""
		#Update the decimal position of the bullet. Subtract the speed_factor from the y-coordinate value.
		self.y -= self.speed_factor
		#Now update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""This class draws a bullet to the screen."""
		#Draw the bullet using the draw.rect() function:
		pygame.draw.rect(self.screen, self.color, self.rect)

