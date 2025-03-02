import pygame, logging, time, globals
from world import World
from player import Player
from lightMap import LightMap
from utilities import *
pygame.init()

# Set up the display
screen = pygame.display.set_mode((0 , 0))
pygame.display.set_caption("Blindsided")

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('log.txt'),
                        logging.StreamHandler()
                    ])
logging.info('Starting game...')

world = World() 
world.loadMap("./map.txt")
cameraPos = (0,0)

globals.lightMap = LightMap((screen.get_width(), screen.get_height()))

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick() # ms

    globals.lightMap.clear()

    for event in pygame.event.get():
        world.handleEvent(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                globals.debugMode = not globals.debugMode

    screen.fill((0, 0, 0))

    world.update(dt)
    world.draw(screen, cameraPos)

    # Update and draw light
    if not globals.debugMode:
        globals.lightMap.draw(screen)

    if globals.debugMode:
        drawFPSCounter(screen, clock)
        screen.blit(renderText(f"Player velocity: {world.player.velx:.2f}, {world.player.vely:.2f}; x: {world.player.x:.2f}, {world.player.y:.2f}"), (0, 20))

    pygame.display.update()

pygame.quit()