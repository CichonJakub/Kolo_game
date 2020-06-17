import pygame
import logging

logging.basicConfig(level=logging.DEBUG)
#logging.debug('This will get logged')

class Player:
    def __init__(self):
        self.NAME = "TEST"
        self.SPRITE = pygame.image.load('./BULBA64.png')
        self.MAP = "first_map.txt"
        self.POS = [0,0]
        self.HEALTH = 100
        self.DIR = False
        self.MOVING = False
        self.VELOCITY = 16
        self.PREV_POS = []
        self.CURR_QUESTS = {}
