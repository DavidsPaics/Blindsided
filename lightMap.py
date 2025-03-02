import pygame
import math
import logging
import time
from utilities import *
import globals

class LightMap:
    def __init__(self, size):
        """
        Initializes the LightMap.
        :param size: (width, height) of the surface
        :param light_strength: Controls how bright the light is (0-255)
        """
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

    def clear(self):
        """ Clears the light map with a semi-transparent dark overlay. """
        self.surface.fill((0, 0, 0, 255)) 
        
    def cast_light(self, light_pos, game_map, layers, radius=200, num_rays=100):
        """
        Casts light rays dynamically and stops at walls.
        :param light_pos: (x, y) position of the light source
        :param game_map: 2D list of characters representing the tile map
        :param layers: Dictionary mapping characters to properties (e.g., '1' = solid wall)
        :param radius: Maximum light distance
        :param num_rays: Number of rays for light casting
        :return: List of end points for the light polygon
        """
        rays = []
        map_width = len(game_map[0])  # Number of columns
        map_height = len(game_map)    # Number of rows

        for angle in range(0, 360, 360 // num_rays):
            rad = math.radians(angle)
            dx, dy = math.cos(rad), math.sin(rad)
            x, y = light_pos

            counter = 0

            for _ in range(radius):  # Step forward along the ray
                x += dx
                y += dy
                tile_x, tile_y = int(x // (globals.tile_size*globals.scaling)), int(y // (globals.tile_size*globals.scaling))

                # Check if we are out of bounds
                if 0 <= tile_x < map_width and 0 <= tile_y < map_height:
                    tile_char = game_map[tile_y][tile_x]  # Get the tile character
                    if layers.get(tile_char, 0) == 1:  # Look up in layers; default to '0'
                        counter -= 1
                        if counter < 1:
                            break  # Stop light at this wall
                else:
                    break  # Stop if out of bounds

            rays.append((x, y))
        return rays


    def draw_light(self, light_pos, game_map, layers, radius=200, light_strength=100):
        """
        Draws the light effect onto the light surface.
        :param light_pos: (x, y) position of the light source
        :param game_map: 2D list representing the game world
        :param layers: Dictionary mapping characters to properties
        :param tile_size: Size of each tile
        :param radius: Maximum light distance
        """
        self.clear()  # Clear the surface before drawing new lights
        light_points = self.cast_light(light_pos, game_map, layers, radius, num_rays=globals.lightRayCount)

        if len(light_points) > 2:
            # Draw the base light shape
            pygame.draw.polygon(self.surface, (0, 0, 0, light_strength), light_points)

            # Smooth fading effect using a radial gradient slightly larger than the polygon
            larger_radius = radius + 10  # Increase the radius slightly for the gradient
            gradient = pygame.Surface((larger_radius * 2, larger_radius * 2), pygame.SRCALPHA)
            for i in range(larger_radius, 50, -globals.lightGradientStep):
                alpha = int(((i - 50) / (larger_radius - 50)) * (255 - light_strength) + light_strength)
                pygame.draw.circle(gradient, (0, 0, 0, alpha), (larger_radius, larger_radius), i)

            # Center the gradient at the light source
            gradient_x = light_pos[0] - larger_radius
            gradient_y = light_pos[1] - larger_radius

            self.surface.blit(gradient, (gradient_x, gradient_y))
            gradient = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            for i in range(radius, 50, -globals.lightGradientStep):
                alpha = int(((i - 50) / (radius - 50)) * (255 - light_strength) + light_strength)
                pygame.draw.circle(gradient, (0, 0, 0, alpha), (radius, radius), i)

            # Center the gradient at the light source
            gradient_x = light_pos[0] - radius
            gradient_y = light_pos[1] - radius

            self.surface.blit(gradient, (gradient_x, gradient_y))

    def draw(self, target_surface):
        """
        Blits the light surface onto a given target surface.
        :param target_surface: The surface to render the light onto
        """
        target_surface.blit(self.surface, (0, 0))
