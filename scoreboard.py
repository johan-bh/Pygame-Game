import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	"""A class to keep track of scores."""
	def __init__(self,ai_settings,screen,stats):
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		#Font settings and score info
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,35)

		#Prepare the initial score and level images
		self.prep_score()
		self.prep_ships()
		self.prep_high_score()
		self.prep_level()

	def prep_score(self):
		"""Turn the initial score into a rendered image."""
		rounded_score = int(round(self.stats.score,-1))
		score_string = "Score: " + "{:}".format(rounded_score)
		self.score_image = self.font.render(score_string, True, self.text_color, self.ai_settings.bg_color)

		#Display the score at the top right corner of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = self.screen_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = int(round(self.stats.high_score, -1))
		high_score_string = "High Score: " + "{:}".format(high_score)
		self.high_score_image = self.font.render(high_score_string, True, self.text_color, self.ai_settings.bg_color)

		#Display the score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top

	def prep_level(self):
		"""Turn the current level into a rendered image."""
		self.level_image = self.font.render("Level: " + str(self.stats.level), True, self.text_color,self.ai_settings.bg_color)

		#Display the score 10 pixels below the scoreboard.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
			""""Turn the current amount of ships into a rendered image."""
			self.ships = Group()
			for ship_number in range(self.stats.ships_left):
				ship = Ship(self.ai_settings, self.screen)
				ship.rect.x = 10 + ship_number * ship.rect.width
				ship.rect.y = 10
				self.ships.add(ship)

	def show_score(self):
		"""Blit the score, high score and level to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		#Draw the ships to the screen.
		self.ships.draw(self.screen)





