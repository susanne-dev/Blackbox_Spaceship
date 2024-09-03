import math
import numpy as np
import pygame

from storage import Storage, RotationObject
from simulation import Simulation
from utility import Utility
from ui import Renderer

class MenuArea:
    def __init__(self, type:str, content = None, offsetX:int = 0, offsetY:int = 0) -> None:
        self.type = type
        self.content = content
        self.offsetX = offsetX
        self.offsetY = offsetY

class Menu:
    def __init__(self, name:str, areaCount:int, area1:MenuArea, area2:MenuArea = None, area3:MenuArea = None, area4:MenuArea = None) -> None:
        
        self.name:str = name
        self.areaCount:int = areaCount

        match areaCount:
            case 1:
                self.area1:MenuArea = area1
            case 2:
                self.area1:MenuArea = area1
                self.area2:MenuArea = area2
            case 3:
                self.area1:MenuArea = area1
                self.area2:MenuArea = area2
                self.area3:MenuArea = area3
            case 4:
                self.area1:MenuArea = area1
                self.area2:MenuArea = area2
                self.area3:MenuArea = area3
                self.area4:MenuArea = area4

class MenuApi:
    menus = [
        Menu("Index", 1, MenuArea("list", ["[0] Index", "[1] Piloting", "[2] Guns", "[3] Systems", "[4] Engineering", "[5] Shield", "[6] FTL"], 100, 100)),

        Menu("Piloting", 2, MenuArea("list"), MenuArea("list", ["Commands:", "- speed -100% to 100%", "- pitch|yaw|roll -180 to 180"])),

        Menu("Guns", 2, MenuArea("list", ["[0] Piloting", "[1] Guns", "[2] Systems"]), MenuArea("list", ["[0] Piloting", "[1] Guns", "[2] Systems"])),

        Menu("Systems", 1, MenuArea("list")),

        Menu("Engineering", 1, MenuArea("list")),

        Menu("Shield", 1, MenuArea("list")),

        Menu("FTL", 1, MenuArea("draw"))
    ]

    def index(name:str) -> int:
        for i in range(len(MenuApi.menus)):
            if (MenuApi.menus[i].name == name):
                return i
            
        return -1
    
    def currentMenu() -> Menu:
        return MenuApi.menus[MenuApi.index(Storage.activeMenu)]

    def displayMenu(screen: pygame.surface):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        menu:Menu = MenuApi.currentMenu()
        
        match Storage.activeMenu:
            case "Index":
                MenuApi.displayMenuOld(screen)
            case "Piloting":
                relativeGoal = Utility.mapToRelative(Storage.shipObject.position, Storage.Ship.goal)
                relativeVelocity = Utility.mapToRelative(Storage.shipObject.position, Storage.shipObject.velocity + Storage.shipObject.position.Base)
                pitch = np.arctan(relativeGoal[1] / relativeGoal[2])
                yaw = np.arctan(relativeGoal[0] / relativeGoal[2])
                if relativeGoal[2] < 0:
                    Renderer.displayGoalDirectionIndicator(screen, (200, 200), 100, 10, pitch, -yaw, True)
                else:
                    Renderer.displayGoalDirectionIndicator(screen, (200, 200), 100, 10, -pitch, yaw)
                """pitch = np.arctan2(relativeGoal[2], np.sqrt(relativeGoal[0]**2 + relativeGoal[1]**2))
                yaw = np.arctan2(relativeGoal[1], relativeGoal[0])"""

                menu.area1.content = [
                                        "",
                                        "Thrust: " + str(Storage.Ship.thrust) + "%",
                                        "Velocity:",
                                        "   X: " + str(round(relativeVelocity[0], 2)),
                                        "   Y: " + str(round(relativeVelocity[1], 2)),
                                        "   Z: " + str(round(relativeVelocity[2], 2)),
                                        "",
                                        "Destination:",
                                        "   X: " + str(round(relativeGoal[0], 2)),
                                        "   Y: " + str(round(relativeGoal[1], 2)),
                                        "   Z: " + str(round(relativeGoal[2], 2)),
                                        "   Distance: " + str(round(np.linalg.norm(relativeGoal), 2))
                                      ]
            case "Guns":
                pass
            case "Systems":
                Renderer.displayRadar(screen, (800, 500), 400)
            case "Engineering":
                pass
            case "Shield":
                pass
            case "FTL":
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
            case _:
                pass

    def __displayMenuArea(screen:pygame.Surface, menu:Menu, area:MenuArea, x:int, y:int):
        font = pygame.font.SysFont('VT323', 30)
        if (area.type == "list"):
            for i in range(len(area.content)):
                #print(area.content)
                text = font.render(area.content[i], False, (255, 255, 255))
                screen.blit(text, (x + area.offsetX, y + 35 * i + area.offsetY))


    def displayMenuOld(screen:pygame.Surface):
        menu:Menu = MenuApi.currentMenu()
    
        match menu.areaCount:
            case 1:
                MenuApi.__displayMenuArea(screen, menu, menu.area1, 50, 50)
            case 2:
                MenuApi.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                MenuApi.__displayMenuArea(screen, menu, menu.area2, 550, 50)
            case 3:
                MenuApi.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                MenuApi.__displayMenuArea(screen, menu, menu.area2, 550, 50)
                MenuApi.__displayMenuArea(screen, menu, menu.area3, 50, 400)
            case 4:
                MenuApi.__displayMenuArea(screen, menu, menu.area1, 50, 50)
                MenuApi.__displayMenuArea(screen, menu, menu.area2, 550, 50)
                MenuApi.__displayMenuArea(screen, menu, menu.area3, 50, 400)
                MenuApi.__displayMenuArea(screen, menu, menu.area4, 550, 400)