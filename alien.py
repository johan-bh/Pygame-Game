import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class that represents aliens in the game."""
	def __init__(self, ai_settings, screen):
		#Initialize alien and place it in the top left corner.
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#Load the image of the alien and get its rect attributes:
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		#Create alien at the top left corner with added space around it that equates to the image's height and width.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store the alien's excact position (decimal value):
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw the image of the alien onto it's rect position."""
		self.screen.blit(self.image, self.rect)


	def check_edges(self):
		"""Return True if an alien is at the edge of the screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= screen_rect.left:
			return True

	def update(self):
		"""Moves the aliens to left or right."""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x














