import pygame, logging, time, globals
from world import World
from player import Player
from lightMap import LightMap
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

player = Player()
globals.lightMap = LightMap((screen.get_width(), screen.get_height()))

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) # ms

    globals.lightMap.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    player.update(dt)
    world.draw(screen, cameraPos)
    player.draw(screen, cameraPos)

    globals.lightMap.draw(screen)

    pygame.display.update()

pygame.quit()