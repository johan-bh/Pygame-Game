class Settings():
	"""A class to store settings for the Alien Invasion game."""

	def __init__(self):
		"""Initialize static settings for the game."""
		#Screen settings:
		self.screen_width = 1440
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#Ship settings:
		self.ship_speed_factor = 1
		self.ship_limit = 3

		#Bullet settings:
		self.bullet_speed_factor = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60,60,60
		self.bullets_allowed = 3

		#Alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 1
		self.alien_points = 50
		#fleet direction of 1 represents right movement and -1 represents left movement.
		self.fleet_direction = 1

		#Scale for how quickly the game speeds up for each level
		self.speedup_scale = 1.2
		#Scale for how much aliens_points increase for each level
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize the game settings that'll change throughout the game."""
		self.ship_speed_factor = 0.5
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 0.5
		#A fleet direction of 1 represents right movement; -1 represents left movement
		self.fleet_direction = 1
		#Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increases the speed settings and alien_points."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
