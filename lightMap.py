import pygame, logging, time
from utilities import *
import globals

class LightMap:
    def __init__(self, size):
        self.surface = pygame.surface.Surface(size, pygame.SRCALPHA)
    
    def clear(self):
        self.surface.fill((0,0,0,245))

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.surface, (0,0))