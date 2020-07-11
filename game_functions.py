import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from pygame.sprite import Sprite

pygame.init()
pygame.mixer.music.load("alien_sound.wav")
crash_sound = pygame.mixer.Sound("crash_sound.wav")
fleet_landing = pygame.mixer.Sound("fleet_landing.wav")

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_ESCAPE:
		sys.exit()

def check_keyup_events(event, ship):
	"""Respond to key releases"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets):
	"""Respond to keypresses and mouse events:"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen,stats,sb,play_button,ship, aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings, screen,stats,sb,play_button,ship, aliens,bullets,mouse_x,mouse_y):
	"""Start a new game if the player clicks on the play button."""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#Reset game speed settings:
		ai_settings.initialize_dynamic_settings()
		#Hide the mouse cursor
		pygame.mouse.set_visible(False)
		#Reset game statistics
		stats.reset_stats()
		stats.game_active = True

		#Reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#Empty lists of aliens ands bullets
		aliens.empty()
		bullets.empty()

		#Create new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		#Play background music
		pygame.mixer.music.play(-1)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet - unless the limit of 3 has beeen reached."""
	#Create a bullet and add it to the bullets to group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Update images on the screen and flip to the new screen."""
	#Make sure the screen redraws with the background color every time it passes through the loop using the 'screen.fill()' method:
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets behind the ship and aliens. The bullets.sprites() method returns a list of all sprites in the group bullets.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	#Show the score info:
	sb.show_score()

	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
	#Make the most recently drawn screen visible using the 'pygame.display.flip()' method.
	#If there are game elements in the window, this will create the illusion of smooth movement:
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update the position of bullets and remove bullets as they disappear from the window."""
	#Update bullet positions:
	bullets.update()
	#Get rid of bullets when they disappear from the window.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

	#Check for any bullets that have hit aliens. If so, get rid of the bullet as well as the alien.
	if len(aliens) == 0:
		#If the fleet is destroyed start a new level.
		bullets.empty()
		ai_settings.increase_speed()

		#Increase level
		stats.level += 1
		sb.prep_level()

		#Create fleet and centering
		create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to collisions between bullets and aliens."""
	#If a collision is detected: remove the bullet and the aliens
	collisions = pygame.sprite.groupcollide(bullets, aliens,True, True)
	for aliens in collisions.values():
		stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()
		pygame.mixer.Sound.play(crash_sound)

	check_high_score(stats,sb)

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine how many aliens that can fit in a row."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height, alien_height):
	"""Determine the number of rows that fit on the screen - while leaving extre space at the bottom."""
	available_space_y = ai_settings.screen_height - (3*alien_height) - ship_height
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in a row."""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = 2* alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create an entire fleet of aliens."""
	#Create an alien and find the highest possible amount of aliens in a row.
	#Spacing between each alien is equal to one alien width.
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	#Create a fleet of aliens. Use nested loops - when create_alien() is called, we include an argument for the row number so each row can be placed farther down the screen:
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings, aliens):
	"""Make the program respond appropriately if any aliens have reached an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Make the fleet change direction and drop it down."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Respond when a ship is hit by an alien."""
	if stats.ships_left > 0:
	#Decrement number of ships left
		stats.ships_left -= 1
		
		#Play sound effect when the fleet hits the ship or the bottom
		pygame.mixer.Sound.play(fleet_landing)

		#Update scoreboard.
		sb.prep_ships()

		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#Pause the game briefly so the player can prepare for the next round.
		sleep(1.5)

	else:
		pygame.mixer.Sound.play(fleet_landing)
		stats.game_active = False
		#Stop background music when the game is lost
		pygame.mixer.music.stop()
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if any of the aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Use same procedure as with alien-ship collisions
			pygame.mixer.Sound.play(fleet_landing)
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Update the positions of all the aliens."""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	#Look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats,sb, screen, ship, aliens, bullets)

	#Look for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
	"""Check if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()





