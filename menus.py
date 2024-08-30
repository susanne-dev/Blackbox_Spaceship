import math
import numpy as np

from storage import Storage, RotationObject
from simulation import Simulation
from utility import Utility

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

    def update():
        menu:Menu = MenuApi.currentMenu()
        
        match Storage.activeMenu:
            case "Index":
                return
            case "Piloting":
                relativeGoal = Utility.mapToRelative(Storage.shipObject.position, Storage.Ship.goal)
                relativeVelocity = Utility.mapToRelative(Storage.shipObject.position, Storage.shipObject.velocity + Storage.shipObject.position.Base)
                pitch = np.arctan2(relativeGoal[2], np.sqrt(relativeGoal[0]**2 + relativeGoal[1]**2))
                yaw = np.arctan2(relativeGoal[1], relativeGoal[0])

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
