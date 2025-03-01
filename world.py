import pygame, logging, time, os
from utilities import *
import globals

tileNames = {
    ".": "floor",
    "@": "floor", 
    "#": "wall",
}

class World:
    def __init__(self):
        self.currentMap = []
        self.tile_textures = self.load_tile_textures("assets/tiles")

    def load_tile_textures(self, path):
        """Loads tile textures from the given directory."""
        textures = {}
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                tile_name = filename.split(".")[0]  # Extract character from filename
                image = pygame.image.load(os.path.join(path, filename)).convert_alpha()

                # Scale the texture based on globals.scaling
                scaled_size = int(globals.tile_size * globals.scaling)
                textures[tile_name] = pygame.transform.scale(image, (scaled_size, scaled_size))

        return textures

    def loadMap(self, map):
        with open(map) as f:
            mapdata = f.read().split("\n")
        
        isCompressed = mapdata[0][0] == "C"

        if not isCompressed:
            self.currentMap = [list(row) for row in mapdata[1:]]
            return

        for line in mapdata[1:]:
            self.currentMap.append(list(rleDecode(line)))

    def draw(self, surface, cameraPos):
        if not self.currentMap:
            return

        cam_x, cam_y = cameraPos
        scaled_size = int(globals.tile_size * globals.scaling)  # Adjusted tile size

        for row_idx, row in enumerate(self.currentMap):
            for col_idx, tile in enumerate(row):
                screen_x = (col_idx * scaled_size) - cam_x
                screen_y = (row_idx * scaled_size) - cam_y

                # Ensure only visible tiles are drawn
                if (
                    0 <= screen_x < surface.get_width() and
                    0 <= screen_y < surface.get_height()
                ):
                    texture = self.tile_textures.get(tileNames.get(tile, None), None)
                    if texture:
                        surface.blit(texture, (screen_x, screen_y))
                    else:
                        pygame.draw.rect(surface, (255, 0, 255), (screen_x, screen_y, scaled_size, scaled_size))  # Magenta for missing textures
