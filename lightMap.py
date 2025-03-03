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
        :param size: (width, height) of the full-resolution surface
        :param downscale_factor: How much to downscale rendering (higher = better performance, lower quality)
        """
        self.full_size = size
        self.downscale_factor = globals.lightMapDownscale
        self.low_res_size = (size[0] // self.downscale_factor, size[1] // self.downscale_factor)
        self.surface = pygame.Surface(self.low_res_size, pygame.SRCALPHA)
        self.temp_surface = pygame.Surface(self.low_res_size, pygame.SRCALPHA)

    def clear(self):
        """ Clears the light map with a semi-transparent dark overlay. """
        self.surface.fill((0, 0, 0, 255))

    def cast_light(self, light_pos, game_map, layers, radius=200, num_rays=100, angle=360, startAngle=0):
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

        # Adjust light position for low resolution
        light_pos = (light_pos[0] // self.downscale_factor, light_pos[1] // self.downscale_factor)
        scaled_radius = radius // self.downscale_factor
        if angle<360:
            rays.append((light_pos[0]+globals.camerax*0, light_pos[1]+globals.cameray*0))

        for angle in range(startAngle, angle+startAngle, max(1, angle // num_rays)):
            rad = math.radians(angle)
            dx, dy = math.cos(rad), math.sin(rad)
            x, y = light_pos

            for _ in range(scaled_radius // globals.lightRayStepSize):
                x += dx * globals.lightRayStepSize
                y += dy * globals.lightRayStepSize
                tile_x, tile_y = int(x // (globals.tile_size * globals.scaling // self.downscale_factor)), \
                                 int(y // (globals.tile_size * globals.scaling // self.downscale_factor))

                # Check if we are out of bounds
                # Check if the ray is outside the screen bounds
                screen_x = x * self.downscale_factor - globals.camerax
                screen_y = y * self.downscale_factor - globals.cameray
                if screen_x < 0 or screen_x >= self.full_size[0] or screen_y < 0 or screen_y >= self.full_size[1]:
                    break  # Stop if the ray is outside the screen

                if 0 <= tile_x < map_width and 0 <= tile_y < map_height:
                    tile_char = game_map[tile_y][tile_x]  # Get the tile character
                    if layers.get(tile_char, 0) == 1:  # Look up in layers; default to '0'
                        break  # Stop light at this wall
                else:
                    break  # Stop if out of bounds

            rays.append((x+globals.camerax*0, y+globals.cameray*0))
        return rays

    def draw_light(self, light_pos, game_map, layers, radius=200, light_strength=100, angle=360, startAngle=0):
        """
        Draws the light effect onto the low-resolution surface.
        :param light_pos: (x, y) position of the light source
        :param game_map: 2D list representing the game world
        :param layers: Dictionary mapping characters to properties
        :param radius: Maximum light distance
        """
        self.temp_surface.fill((0,0,0))
        light_points = self.cast_light(light_pos, game_map, layers, radius, num_rays=globals.lightRayCount, angle=angle, startAngle=startAngle)
        screen_light_pos = (light_pos[0]-globals.camerax, light_pos[1]-globals.cameray)
        for i in range(len(light_points)):
            light_points[i] = (light_points[i][0]-globals.camerax/2, light_points[i][1]-globals.cameray/2)
        if len(light_points) > 2:
            # Draw the base light shape in low resolution
            pygame.draw.polygon(self.temp_surface, (0, 0, 0, light_strength), light_points)

            # Smooth fading effect using a radial gradient slightly larger than the polygon
            scaled_radius = (radius+5) // self.downscale_factor
            gradient = pygame.Surface((scaled_radius * 2, scaled_radius * 2), pygame.SRCALPHA)
            for i in range(scaled_radius, 0, -globals.lightGradientStep):
                alpha = int(((i) / (scaled_radius)) * 
                            (255 - light_strength) + light_strength)
                pygame.draw.circle(gradient, (0, 0, 0, alpha), (scaled_radius, scaled_radius), i)

            # Center the gradient at the light source
            gradient_x = screen_light_pos[0] // self.downscale_factor - scaled_radius
            gradient_y = screen_light_pos[1] // self.downscale_factor - scaled_radius

            self.temp_surface.blit(gradient, (gradient_x, gradient_y))
            self.surface.blit(self.temp_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def draw(self, target_surface):
        """
        Scales up the low-resolution light map and blits it onto the target surface.
        :param target_surface: The surface to render the light onto
        """
        # Scale up with smoothing
        high_res_surface = pygame.transform.smoothscale(self.surface, self.full_size)
        target_surface.blit(high_res_surface, (0, 0))
