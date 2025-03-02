import pygame, logging, time, os
from utilities import *
import globals
from player import Player


class World:
    def __init__(self):
        self.currentMap = []
        
        self.tileNames = {
            ".": "floor",
            "@": "floor",
            "#": "wall-s",
        }

        self.tileLayers = {
            ".": 0,
            "@": 0,
            "#": 1
        }
        self.spawnPoint = (0,0)
        self.tile_textures = self.load_tile_textures("assets/tiles")
        self.player = Player()

    def load_tile_textures(self, path):
        """Loads tile textures from the given directory."""
        textures = {}
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                tile_name = filename.split(".")[0]  # Extract character from filename
                image = pygame.image.load(os.path.join(path, filename)).convert_alpha()

                # Scale the texture based on globals.scaling
                scaled_size = int(globals.scaledTileSize)
                textures[tile_name] = pygame.transform.scale(image, (scaled_size, scaled_size))

        return textures

    def loadMap(self, map):
        with open(map) as f:
            mapdata = f.read().split("\n")
        
        isCompressed = mapdata[0][0] == "C"

        self.spawnPoint = (int(mapdata[0].split()[1]),int(mapdata[0].split()[2]))
        self.player.x = self.spawnPoint[0] * globals.scaledTileSize
        self.player.y = self.spawnPoint[1] * globals.scaledTileSize

        if not isCompressed:
            self.currentMap = [list(row) for row in mapdata[1:]]
            return

        for line in mapdata[1:]:
            self.currentMap.append(list(rleDecode(line)))
    
    def update(self, dt): 
        self.player.update(dt, self.currentMap, self.tileLayers)

    def draw(self, surface):
        if not self.currentMap:
            return
        
        scaled_size = int(globals.scaledTileSize)  # Adjusted tile size

        for row_idx, row in enumerate(self.currentMap):
            for col_idx, tile in enumerate(row):
                if self.tileLayers[tile] == 1:
                    continue

                screen_x = (col_idx * scaled_size)
                screen_y = (row_idx * scaled_size)

                # Ensure only visible tiles are drawn
                if (
                    0 <= screen_x < surface.get_width() and
                    0 <= screen_y < surface.get_height()
                ):
                    texture = self.tile_textures.get(self.tileNames.get(tile, None), None)
                    if texture:
                        surface.blit(texture, (screen_x, screen_y))
                    else:
                        pygame.draw.rect(surface, (255, 0, 255), (screen_x, screen_y, scaled_size, scaled_size))  # Magenta for missing textures

        self.player.draw(surface)


    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F7:
                logging.info("Reloading tile textures.")
                self.tile_textures = self.load_tile_textures("assets/tiles")