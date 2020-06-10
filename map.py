import pygame
from settings import *

class Map:
   
    def __init__(self, filename):

        with open(filename, 'r') as f:
            self.data = []
            for row in f:
                tmp_row = row.strip().split(',')
                final_row = []
                for tile in tmp_row:
                    final_row.append(tile.strip())
                self.data.append(final_row)

        self.name = filename
        self.tilewidth = len(self.data[0])
        print(self.tilewidth)
        self.tileheight = len(self.data)
        print(self.tileheight)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        print(self.width)
        print(self.height)

        # zmienne służące do możliwego przesunięcia w pionie lub poziomie
        self.horizontal_move = 0
        self.vertical_move = 0

        # ile mapa może się przesunąć maksymalnie
        self.MARGIN_LEFT = 0
        self.MARGIN_RIGHT = self.tilewidth - MAPWIDTH
        self.MARGIN_BOTTOM = self.tileheight - MAPHEIGHT
        print(self.MARGIN_RIGHT)
        print(self.MARGIN_BOTTOM)
        self.MARGIN_UP = 0    
