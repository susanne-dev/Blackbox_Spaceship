import pygame
from pygame.math import Vector2
from typing import IO, Callable, Sequence, Tuple, Union
import random
import math
import numpy as np

from storage import Storage
from menus import MenuApi, Menu, MenuArea
from simulation import Simulation
from gameObject import GameObject, RotationObject
from utility import Utility


Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

class Renderer:
    def clearScreen(screen:pygame.Surface):
        font = pygame.font.SysFont('Consolas', 30)
        #textBackgroundTop = font.render(    "╔══════════════════════════════════════════════════════════════╗", False, (255, 255, 255))
        fill1 = ""
        fill2 = ""
        if (len(Storage.activeMenu) % 2 == 0):
            fillLen = 30 - len(Storage.activeMenu) / 2
            fill1 = "═" * int(fillLen)
            fill2 = "═" * int(fillLen)
        else:
            fillLen = 30 - len(Storage.activeMenu) / 2
            fill1 = "═" * math.floor(fillLen)
            fill2 = "═" * math.ceil(fillLen)

        textBackgroundTop = font.render(    "╔" + fill1 + "╡" + Storage.activeMenu + "╞" + fill2 + "╗", False, (255, 255, 255))
        textBackgroundMiddle1 = font.render("║                                                              ║", False, (255, 255, 255))
        textBackgroundMiddle2 = font.render("╠══════════════════════════════════════════════════════════════╣", False, (255, 255, 255))
        textBackgroundBottom = font.render( "╚══════════════════════════════════════════════════════════════╝", False, (255, 255, 255))

        background = pygame.Surface((1600, 900))
        background.fill(pygame.Color('#050041'))
        screen.blit(background, (0, 0))
        screen.blit(textBackgroundTop, (5, 0))

        for i in range(21):
            screen.blit(textBackgroundMiddle1, (5, 35 * i + 30))

        screen.blit(textBackgroundMiddle2, (5, 765))

        for i in range(2):
            screen.blit(textBackgroundMiddle1, (5, 35 * i + 800))
            
        screen.blit(textBackgroundBottom, (5, 870))

    def displayConsole(screen:pygame.Surface):
        font = pygame.font.SysFont('VT323', 30)

        textConsole1 = font.render(Storage.lastMessage, False, (255, 255, 255))

        if (Storage.cursorFrame >= 5):
            textConsole2 = font.render(">>> " + Storage.commands[Storage.commandIndex] + "|", False, (255, 255, 255))
        else:
            textConsole2 = font.render(">>> " + Storage.commands[Storage.commandIndex], False, (255, 255, 255))

        screen.blit(textConsole1, (40, 810))
        screen.blit(textConsole2, (40, 845))

        Storage.cursorFrame += 1
        if (Storage.cursorFrame >= 10):
            Storage.cursorFrame = 0

    def displayRadar(screen:pygame.Surface, radarCentre = (1350, 150), radius = 200) -> None:
        r1 = radius
        r2 = radius * 0.45
        sin = math.sin(30) * r1 / 20
        cos = math.cos(30) * r2 / 20
        pygame.draw.ellipse(screen, (0, 0, 0), (radarCentre[0] - r1, radarCentre[1] - r2, r1 * 2, r2 * 2))
        pygame.draw.ellipse(screen, (50, 50, 50), (radarCentre[0] - r1 * (1/4), radarCentre[1] - r2 * (1/4), r1 * 2 * (1/4), r2 * 2 * (1/4)), 1)
        pygame.draw.ellipse(screen, (50, 50, 50), (radarCentre[0] - r1 * (2/4), radarCentre[1] - r2 * (2/4), r1 * 2 * (2/4), r2 * 2 * (2/4)), 1)
        pygame.draw.ellipse(screen, (50, 50, 50), (radarCentre[0] - r1 * (3/4), radarCentre[1] - r2 * (3/4), r1 * 2 * (3/4), r2 * 2 * (3/4)), 1)
        pygame.draw.ellipse(screen, (255, 255, 255), (radarCentre[0] - r1 * (4/4), radarCentre[1] - r2 * (4/4), r1 * 2 * (4/4), r2 * 2 * (4/4)), 2)
        
        shipPos = Storage.shipObject.position
        radarSurface = pygame.Surface((r1 * 2.4, r2 * 2.4), pygame.SRCALPHA)
        radarSurface.set_alpha(128)
        for object in Storage.Simulation.objects:
            dist = Utility.distance(shipPos.Base, object.position.Base)
            if (dist <= 800):
                tempObject = object.__copy__()
                tempObject.position = RotationObject(Utility.mapToRelative(shipPos, object.position.Base))
                Renderer.displayRadarObject2(radarSurface, radarCentre, r1, r2, tempObject, int(dist))
        screen.blit(radarSurface, (radarCentre[0] - r1 * 1.2, radarCentre[1] - r2 * 1.2))
        
        for object in Storage.Simulation.objects:
            dist = Utility.distance(shipPos.Base, object.position.Base)
            if (dist <= 800):
                tempObject = object.__copy__()
                tempObject.position = RotationObject(Utility.mapToRelative(shipPos, object.position.Base))
                Renderer.displayRadarObject1(screen, radarCentre, r1, r2, tempObject, int(dist))
        
        pygame.draw.polygon(screen, (50, 255, 80), [(radarCentre[0], radarCentre[1] - r2 / 20), (radarCentre[0] + sin, radarCentre[1] + cos), (radarCentre[0] - sin, radarCentre[1] + cos)])

        #pygame.draw.line(screen, (255, 255, 255), (radarCentre[0] - r1, radarCentre[1]), (radarCentre[0] + r1, radarCentre[1]))
        #pygame.draw.line(screen, (255, 255, 255), (radarCentre[0], radarCentre[1] - r2), (radarCentre[0], radarCentre[1] + r2))

    def displayRadarObject1(screen:pygame.Surface, radarCentre: tuple[int, int], r1: int, r2: int, object: GameObject, dist: int) -> None:
        colourMult = 1 - (dist / 800)
        if object.team == -1:
            if dist < 250:
                colour = (255, 0, 0)
            else:
                colour = (30 + 225 * colourMult, 20 + 50 * colourMult, 40 * colourMult)
        elif object.team == 0: #replace 0 with fetch for own team value
            colour = (50, 255, 80)
        else:
            colour = (255, 20, 20)

        white = (255 - dist / 4, 255 - dist / 4, 255 - dist / 4)

        pos = object.position.Base
        xz = (radarCentre[0] + pos[0] / 800 * r1, radarCentre[1] - pos[2] / 800 * r2)
        xyz = (radarCentre[0] + pos[0] / 800 * r1, radarCentre[1] - pos[2] / 800 * r2 - pos[1] / 800 * r2)
        
        #pygame.draw.ellipse(screen, white, (xz[0] - r1 / 20, xz[1] - r2 / 20, r1 / 10, r2 / 10), 1)

        if object.type == "player":
            pygame.draw.line(screen, colour, xz, xyz, 4)
            pygame.draw.circle(screen, colour, xyz, 5)
        elif object.type == "asteroid":
            pygame.draw.line(screen, colour, xz, xyz, 4)
            pygame.draw.circle(screen, colour, xyz, int(r1 / 20))

    def displayRadarObject2(screen:pygame.Surface, radarCentre: tuple[int, int], r1: int, r2: int, object: GameObject, dist: int) -> None:
        colourMult = 1 - (dist / 800)
        if object.team == -1:
            if dist < 250:
                colour = (255, 0, 0)
            else:
                colour = (30 + 225 * colourMult, 20 + 50 * colourMult, 40 * colourMult)
        elif object.team == 0: #replace 0 with fetch for own team value /// Nevermind, keep comment just in case idea is brought back
            colour = (50, 255, 80)
        else:
            colour = (255, 20, 20)

        pos = object.position.Base
        xz = (r1 * 1.2 + pos[0] / 800 * r1, r2 * 1.2 -  + pos[2] / 800 * r2)

        if object.type == "player":
            pygame.draw.ellipse(screen, colour, (xz[0] - r1 / 20, xz[1] - r2 / 20, r1 / 10, r2 / 10))
        elif object.type == "asteroid":
            pygame.draw.ellipse(screen, colour, (xz[0] - r1 / 20, xz[1] - r2 / 20, r1 / 10, r2 / 10))
            pygame.draw.ellipse(screen, colour, (xz[0] - r1 / 10, xz[1] - r2 / 10, r1 / 5, r2 / 5), 3)

    def startLoadingAnimation():
        if (random.randint(0, 19) == 0):
            Storage.loading = 5
        elif (random.randint(0, 19) == 0):
            Storage.loading = 4
        elif (random.randint(0, 19) == 0):
            Storage.loading = 3
        elif (random.randint(0, 9) == 0):
            Storage.loading = 2
        else:
            Storage.loading = 1

    def loadingAnimation(screen:pygame.Surface):
        font = pygame.font.SysFont('Consolas', 30)
        if (Storage.loading == 1):
            match Storage.loadingCounter:
                case 0:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 1:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 2:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 3:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 4:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 5:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 6:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 7:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 8:
                    text = font.render("|█████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 9:
                    text = font.render("|██████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 10:
                    text = font.render("|███████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 11:
                    text = font.render("|██████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 12:
                    text = font.render("|████████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 13:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 14:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 15:
                    text = font.render("|███████████████████████████████████████━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 16:
                    text = font.render("|████████████████████████████████████████━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 17:
                    text = font.render("|█████████████████████████████████████████━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 18:
                    text = font.render("|██████████████████████████████████████████━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 19:
                    text = font.render("|███████████████████████████████████████████━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 20:
                    text = font.render("|█████████████████████████████████████████████━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 21:
                    text = font.render("|███████████████████████████████████████████████━━━━━━━━━━━|", False, (255, 255, 255))
                case 22:
                    text = font.render("|█████████████████████████████████████████████████━━━━━━━━━|", False, (255, 255, 255))
                case 23:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 24:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 25:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 26:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 27:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 28:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 29:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                    
            screen.blit(text, (40, 400))

            Storage.loadingCounter += 1
            if (Storage.loadingCounter >= 30):
                Storage.loadingCounter = 0
                Storage.loading = 0

        elif (Storage.loading == 2):
            match Storage.loadingCounter:
                case 0:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 1:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 2:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 15:
                    text = font.render("|█████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 16:
                    text = font.render("|██████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 17:
                    text = font.render("|███████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 18:
                    text = font.render("|██████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 19:
                    text = font.render("|████████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 20:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 21:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 22:
                    text = font.render("|███████████████████████████████████████━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 23:
                    text = font.render("|████████████████████████████████████████━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 24:
                    text = font.render("|█████████████████████████████████████████━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 25:
                    text = font.render("|██████████████████████████████████████████━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 26 | 27 | 28 | 29 | 30:
                    text = font.render("|███████████████████████████████████████████━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 31:
                    text = font.render("|█████████████████████████████████████████████━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 32:
                    text = font.render("|███████████████████████████████████████████████━━━━━━━━━━━|", False, (255, 255, 255))
                case 33:
                    text = font.render("|█████████████████████████████████████████████████━━━━━━━━━|", False, (255, 255, 255))
                case 34:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 35:
                    text = font.render("|██████████████████████████████████████████████████████━━━━|", False, (255, 255, 255))
                case 36:
                    text = font.render("|███████████████████████████████████████████████████████━━━|", False, (255, 255, 255))
                case 37 | 38 | 39:
                    text = font.render("|████████████████████████████████████████████████████████━━|", False, (255, 255, 255))
                case 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 | 64 | 65 | 66:
                    text = font.render("|█████████████████████████████████████████████████████████━|", False, (255, 255, 255))
                case 67 | 68 | 69:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                    
            screen.blit(text, (40, 400))

            Storage.loadingCounter += 1
            if (Storage.loadingCounter >= 70):
                Storage.loadingCounter = 0
                Storage.loading = 0

        elif (Storage.loading == 3):
            match Storage.loadingCounter:
                case 0:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 1:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 2:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 15:
                    text = font.render("|█████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 16:
                    text = font.render("|██████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 17:
                    text = font.render("|███████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 18:
                    text = font.render("|██████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 19:
                    text = font.render("|████████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 20:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 21:
                    text = font.render("|██████████████████████████████████████━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 22:
                    text = font.render("|███████████████████████████████████████━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 23:
                    text = font.render("|████████████████████████████████████████━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 24:
                    text = font.render("|█████████████████████████████████████████━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 25:
                    text = font.render("|██████████████████████████████████████████━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 26 | 27 | 28 | 29 | 30:
                    text = font.render("|███████████████████████████████████████████━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 31:
                    text = font.render("|█████████████████████████████████████████████━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 32:
                    text = font.render("|███████████████████████████████████████████████━━━━━━━━━━━|", False, (255, 255, 255))
                case 33:
                    text = font.render("|█████████████████████████████████████████████████━━━━━━━━━|", False, (255, 255, 255))
                case 34:
                    text = font.render("|█████████████████████████████████████████████████████━━━━━|", False, (255, 255, 255))
                case 35:
                    text = font.render("|██████████████████████████████████████████████████████━━━━|", False, (255, 255, 255))
                case 36:
                    text = font.render("|███████████████████████████████████████████████████████━━━|", False, (255, 255, 255))
                case 37 | 38 | 39:
                    text = font.render("|████████████████████████████████████████████████████████━━|", False, (255, 255, 255))
                case 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 | 64 | 65 | 66:
                    text = font.render("|█████████████████████████████████████████████████████████━|", False, (255, 255, 255))
                case 67 | 68:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                case 69 | 70 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89: 
                    font = pygame.font.SysFont('VT323', 30)
                    text = font.render("ERROR: Fatal error occured during loading!", False, (255, 255, 255))
                    
            screen.blit(text, (40, 400))

            Storage.loadingCounter += 1
            if (Storage.loadingCounter >= 90):
                Storage.loadingCounter = 0
                Storage.loading = 0

        elif (Storage.loading == 4):
            match Storage.loadingCounter:
                case 0:
                    text = font.render("|██━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 1:
                    text = font.render("|███━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 2:
                    text = font.render("|████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 3:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 4:
                    text = font.render("|███████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 5:
                    text = font.render("|████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 6:
                    text = font.render("|██████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 7:
                    text = font.render("|████████████████████████████████████████████━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 8:
                    text = font.render("|████████████████████████████████████████████████████████━━|", False, (255, 255, 255))
                case 9:
                    text = font.render("|██████████████████████████████████████████████████████━━━━|", False, (255, 255, 255))
                case 10:
                    text = font.render("|███████████████████████████████████████████████████━━━━━━━|", False, (255, 255, 255))
                case 11:
                    text = font.render("|██████████████████████████████████████████████████━━━━━━━━|", False, (255, 255, 255))
                case 12:
                    text = font.render("|██████████████████████████████████████████████████━━━━━━━━|", False, (255, 255, 255))
                case 13:
                    text = font.render("|███████████████████████████████████████████████████━━━━━━━|", False, (255, 255, 255))
                case 14:
                    text = font.render("|██████████████████████████████████████████████████████━━━━|", False, (255, 255, 255))
                case 15:
                    text = font.render("|████████████████████████████████████████████████████████━━|", False, (255, 255, 255))
                case 16:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                case 17:
                    text = font.render("|█████████████████████████████████████████████████████████━|", False, (255, 255, 255))
                case 18:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                case 19:
                    text = font.render("|██████████████████████████████████████████████████████████|", False, (255, 255, 255))
                    
            screen.blit(text, (40, 400))

            Storage.loadingCounter += 1
            if (Storage.loadingCounter >= 20):
                Storage.loadingCounter = 0
                Storage.loading = 0

        elif (Storage.loading == 5):
            match Storage.loadingCounter:
                case 0:
                    text = font.render("|████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 1:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 2:
                    text = font.render("|████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 3:
                    text = font.render("|████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 4:
                    text = font.render("|████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 5:
                    text = font.render("|████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 6:
                    text = font.render("|████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 7:
                    text = font.render("|████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 8:
                    text = font.render("|████████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 9:
                    text = font.render("|████████████████████████████████████████━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 10:
                    text = font.render("|████████████████████████████████████████████━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 11:
                    text = font.render("|█████████████████████████████████████████████████━━━━━━━━━|", False, (255, 255, 255))
                case 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24:
                    text = font.render("|██████████████████████████████████████████████████████━━━━|", False, (255, 255, 255))
                case 25:
                    text = font.render("|███████████████████████████████████████████━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 26:
                    text = font.render("|████████████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 27:
                    text = font.render("|██████████████████████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 28:
                    text = font.render("|████████━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                case 29:
                    text = font.render("|━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━|", False, (255, 255, 255))
                    
            screen.blit(text, (40, 400))

            Storage.loadingCounter += 1
            if (Storage.loadingCounter >= 30):
                Storage.loadingCounter = 0
                Storage.loading = 0
        
    def __displayMenuArea(screen:pygame.Surface, menu:Menu, area:MenuArea, x:int, y:int):
        font = pygame.font.SysFont('VT323', 30)
        if (area.type == "list"):
            for i in range(len(area.content)):
                #print(area.content)
                text = font.render(area.content[i], False, (255, 255, 255))
                screen.blit(text, (x + area.offsetX, y + 35 * i + area.offsetY)) 


    def displayMenu(screen:pygame.Surface):
        menu:Menu = MenuApi.currentMenu()
        if menu.name == "FTL":
            # Minigame
            pygame.draw.rect(screen, (0,0,0), (75, 75, 500, 500))
            pygame.draw.rect(screen, (255,255,255), (75, 75, 500, 500), 2)

            #Button
            font = pygame.font.SysFont('VT323', 30)
            if (pygame.mouse.get_pos()[0] > 225 and pygame.mouse.get_pos()[0] < 425) and (pygame.mouse.get_pos()[1] > 600 and pygame.mouse.get_pos()[1] < 700): 
                pygame.draw.rect(screen, (25,0,0), (225, 600, 200, 100))
                text = font.render("Lock", False, (150, 150, 150))
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.draw.rect(screen, (50,0,0), (225, 600, 200, 100))
                text = font.render("Lock", False, (255, 255, 255))

            screen.blit(text, (300, 640))

            pygame.draw.rect(screen, (255,255,255), (225, 600, 200, 100), 2)

            # Map
            pygame.draw.rect(screen, (0,0,0), (725, 75, 300, 650))
            pygame.draw.rect(screen, (255,255,255), (725, 75, 300, 650), 2)
        else:    
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            match menu.areaCount:
                case 1:
                    Renderer.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                case 2:
                    Renderer.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                    Renderer.__displayMenuArea(screen, menu, menu.area2, 550, 50)
                case 3:
                    Renderer.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                    Renderer.__displayMenuArea(screen, menu, menu.area2, 550, 50)
                    Renderer.__displayMenuArea(screen, menu, menu.area3, 50, 400)
                case 4:
                    Renderer.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                    Renderer.__displayMenuArea(screen, menu, menu.area2, 550, 50)
                    Renderer.__displayMenuArea(screen, menu, menu.area3, 50, 400)
                    Renderer.__displayMenuArea(screen, menu, menu.area4, 550, 400)
        
    def _areaTest(screen:pygame.Surface):

        background1 = pygame.Surface((500, 350))
        background1.fill(pygame.Color('#FF0000'))
        background2 = pygame.Surface((500, 350))
        background2.fill(pygame.Color('#00FF00'))
        background3 = pygame.Surface((500, 350))
        background3.fill(pygame.Color('#0000FF'))
        background4 = pygame.Surface((500, 350))
        background4.fill(pygame.Color('#000000'))
        screen.blit(background4, (550, 400))
        screen.blit(background3, (50, 400))
        screen.blit(background2, (550, 50))
        screen.blit(background1, (50, 50))