import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    #Initialize game with the init() function:
    pygame.init()
    #Create an instance of the class Settings:
    ai_settings = Settings()
    #Create a screen object with the 'set_mode()' function - using settings from the Settings():
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    #Make the name of the window "Alien Invasion" using the 'set_caption()' fucntion:
    pygame.display.set_caption("Alien Invasion")
    #Set the background color using the settings from the Settings():
    bg_color = (ai_settings.bg_color)
    #Create an instance of the class Button:
    play_button = Button(ai_settings,screen,"Play")
    #Create an instance of the class GameStats:
    stats = GameStats(ai_settings)
    #Create and instance of the class Scoreboard:
    sb = Scoreboard(ai_settings,screen,stats)
    #Create an instance of the class Ship:
    ship = Ship(ai_settings,screen)
    #Create a group to store bullets in using an instance of pygame.sprite.Group (a list with game functionality)
    bullets = Group()
    #Create a group to store aliens in using an instance of pygame.sprite.Group (a list with game functionality)
    aliens = Group()
    #Create a fleet of aliens
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #Create a 'main loop' that'll control the game using a 'while loop':
    while True:
        #Watch for mouse and keyboard events using the game_functions module:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
       
       
#Run the 'run_game()' command that initializes the game and starts the main loop:
run_game()

            
    