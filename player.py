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

        centerPos = (self.x + (globals.tile_size*globals.scaling)/2, self.y + (globals.tile_size*globals.scaling)/2)

        if pressedKeys[pygame.K_f]:
            globals.lightMap.draw_light(centerPos, currentMap, layers, radius=700, light_strength=0)
        else:
            globals.lightMap.draw_light(centerPos, currentMap, layers, radius=500, light_strength=50)
        

        self.x += self.velx * dt
        self.y += self.vely * dt

        #tile size and player size globals.tile_size*globals.scaling
        # check if tile should collide layers[currentMap[tilex][tiley]] == 1

        # Calculate the player's corner positions for x direction
        # corners_x = [
        #     (self.x + self.velx, self.y),
        #     (self.x + self.velx + globals.tile_size * globals.scaling, self.y),
        #     (self.x + self.velx, self.y + globals.tile_size * globals.scaling),
        #     (self.x + self.velx + globals.tile_size * globals.scaling, self.y + globals.tile_size * globals.scaling)
        # ]


    def draw(self, surface, cameraPos):
        screen_x = self.x - cameraPos[0]
        screen_y = self.y - cameraPos[1]

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