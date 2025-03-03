import pygame, globals, logging, math
from utilities import *

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velx = 0
        self.vely = 0
        self.terminalVelocity = 0.5
        self.speed = 0.02
        self.texture = pygame.Surface((globals.scaling*globals.tile_size, globals.scaling*globals.tile_size))  # Fixed Surface creation
        self.texture.fill((255, 0, 0))  # Red player texture

    def update(self, dt, currentMap, layers):
        # Apply friction to slow down movement gradually
        self.velx *= 0.8
        self.vely *= 0.8
        
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w] or pressedKeys[pygame.K_UP]:  # Move Up
            self.vely = clamp(-self.terminalVelocity, self.vely - self.speed * dt, self.terminalVelocity)

        if pressedKeys[pygame.K_s] or pressedKeys[pygame.K_DOWN]:  # Move Down
            self.vely = clamp(-self.terminalVelocity, self.vely + self.speed * dt, self.terminalVelocity)

        if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_LEFT]:  # Move Left
            self.velx = clamp(-self.terminalVelocity, self.velx - self.speed * dt, self.terminalVelocity)

        if pressedKeys[pygame.K_d] or pressedKeys[pygame.K_RIGHT]:  # Move Right
            self.velx = clamp(-self.terminalVelocity, self.velx + self.speed * dt, self.terminalVelocity)

        if abs(self.velx) < 0.001:
            self.velx = 0
        if abs(self.vely) < 0.001:
            self.vely = 0

        self.x += self.velx * dt
        self.y += self.vely * dt

        centerPos = (self.x + (globals.scaledTileSize)/2, self.y + (globals.scaledTileSize)/2)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = round(math.degrees(math.atan2(mouse_y - centerPos[1], mouse_x - centerPos[0])) - 37.5)
        globals.lightMap.draw_light(centerPos, currentMap, layers, radius=500, light_strength=0, angle=75, startAngle=angle)
        globals.lightMap.draw_light(centerPos, currentMap, layers, radius=200, light_strength=40)

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # light_x = mouse_x 
        # light_y = mouse_y 
        # globals.lightMap.draw_light((light_x, light_y), currentMap, layers, radius=200, light_strength=40)

        self.x += self.velx * dt

        if self.velx<0:
            tile_x = int(self.x // globals.scaledTileSize)
            tile_y = int(self.y // globals.scaledTileSize)
            bottom_left_corner = int((self.y + globals.scaledTileSize) // globals.scaledTileSize)
            if layers[currentMap[tile_y][tile_x]] == 1 or layers[currentMap[bottom_left_corner][tile_x]] == 1:
                self.velx=0
                self.x = (tile_x + 1) * globals.scaledTileSize + 0.1

        if self.velx > 0:
            tile_x = int((self.x + globals.scaledTileSize) // globals.scaledTileSize)
            tile_y = int(self.y // globals.scaledTileSize)
            bottom_right_corner = int((self.y + globals.scaledTileSize) // globals.scaledTileSize)
            if layers[currentMap[tile_y][tile_x]] == 1 or layers[currentMap[bottom_right_corner][tile_x]] == 1:
                self.velx=0
                self.x = tile_x * globals.scaledTileSize - globals.scaledTileSize - 0.1

        self.y += self.vely * dt

        if self.vely < 0:
            tile_x = int(self.x // globals.scaledTileSize)
            tile_y = int(self.y // globals.scaledTileSize)
            top_right_corner = int((self.x + globals.scaledTileSize) // globals.scaledTileSize)
            if layers[currentMap[tile_y][tile_x]] == 1 or layers[currentMap[tile_y][top_right_corner]] == 1:
                self.vely = 0
                self.y = (tile_y + 1) * globals.scaledTileSize + 0.1

        if self.vely > 0:
            tile_x = int(self.x // globals.scaledTileSize)
            tile_y = int((self.y + globals.scaledTileSize) // globals.scaledTileSize)
            bottom_right_corner = int((self.x + globals.scaledTileSize) // globals.scaledTileSize)
            if layers[currentMap[tile_y][tile_x]] == 1 or layers[currentMap[tile_y][bottom_right_corner]] == 1:
                self.vely = 0
                self.y = tile_y * globals.scaledTileSize - globals.scaledTileSize - 0.1
            


    def draw(self, surface):
        screen_x = self.x
        screen_y = self.y

        surface.blit(self.texture, (screen_x, screen_y))
        # for radius in range(95, 45, -1):  # Decreasing radius
        #     alpha = int(mapValue(radius, 45, 95, 0, 245))  # Map radius correctly to alpha
        #     color = (0, 0, 0, alpha)  # RGBA color with mapped alpha

        #     pygame.draw.circle(
        #         globals.lightMap.surface,
        #         color,
        #         (screen_x + self.texture.get_width() // 2, screen_y + self.texture.get_height() // 2),
        #         radius
        #     )

        #     self.drawFlashlight((screen_x, screen_y), 45, 400, 600, 10)


    def drawFlashlight(self, pos, angle, startLength, endLength, steps):
        return #TODO: this is hard