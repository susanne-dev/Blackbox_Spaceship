import pygame
import time

from ui import Renderer
from storage import Storage
from input import InputHandler
from menus import MenuApi
from simulation import Simulation

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption('Blackbox Spaceship')
screen = pygame.display.set_mode((1600, 900))

Simulation.startArea() # Temp

isServer = True
isRunning = True
tick = 1

while isRunning:
    if tick == 11:
        tick = 1

    time.sleep(0.1)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            InputHandler.keyPress(event)

    if isServer:
        Simulation.run(tick)
        # Update clients
    #else:
        # Receive from server

    MenuApi.update()

    Renderer.clearScreen(screen)
    if (Storage.loading):
        Renderer.loadingAnimation(screen)
    else:      #Renderer._areaTest(screen)
        Renderer.displayMenu(screen)
        Renderer.displayConsole(screen)
    if (Storage.activeMenu == "Piloting"):
        Renderer.displayRadar(screen, (800, 500), 400)
    else:
        Renderer.displayRadar(screen)

    pygame.display.update()

    tick += 1 