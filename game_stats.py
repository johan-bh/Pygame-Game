class GameStats():
	"""Track statistics for the Alien Invasion game."""

	def __init__(self,ai_settings):
		#Initialize statistics (attributes)
		self.ai_settings = ai_settings
		self.reset_stats()
		#Start Alien Invasion in an inactive state
		self.game_active = False
		#High Score (should never be reset)
		self.high_score = 0

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
