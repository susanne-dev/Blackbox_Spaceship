import pygame
import math
import numpy as np
import re

from storage import Storage
from ui import Renderer
from menus import MenuApi
from simulation import Simulation

class InputHandler:
    validKeys = ["-", "_", "/", "(", ")", "[", "]", "{", "}", "%"]

    def keyPress(event:pygame.event.Event):
            if (Storage.loading > 0):
                return
            
            # Check if the key pressed is a letter, space, number, or accepted special
            if (event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == ' ' or event.unicode in InputHandler.validKeys):
                if (Storage.commandIndex > 0):
                    Storage.commands[0] = Storage.commands[Storage.commandIndex]
                    Storage.commandIndex = 0
                Storage.commands[0] += event.unicode
            # Check if the key pressed is backspace
            elif (event.key == pygame.K_BACKSPACE):
                if (Storage.commandIndex > 0):
                    Storage.commands[0] = Storage.commands[Storage.commandIndex]
                    Storage.commandIndex = 0
                Storage.commands[0] = Storage.commands[0][:-1]
            # Check if the key pressed is return
            elif (event.key == pygame.K_RETURN):
                if (Storage.commandIndex > 0):
                    Storage.commands[0] = Storage.commands[Storage.commandIndex]
                    Storage.commandIndex = 0
                InputHandler.command()

            elif (event.key == pygame.K_UP):
                if (Storage.commandIndex < 5):
                    if (not Storage.commands[Storage.commandIndex + 1] == ""):
                        Storage.commandIndex += 1
            elif (event.key == pygame.K_DOWN):
                if (Storage.commandIndex > 0):
                    Storage.commandIndex -= 1
        
    def command():

        try:
            Storage.lastMessage = "> " + Storage.commands[0]
            command = Storage.commands[0].split()

            match command[0]:
                case "load" | "reboot":
                    Renderer.startLoadingAnimation()
                case "load1":
                    Storage.loading = 1
                case "load2":
                    Storage.loading = 2
                case "load3":
                    Storage.loading = 3
                case "load4":
                    Storage.loading = 4
                case "load5":
                    Storage.loading = 5

                case "test":
                    match command[1]:
                        case "1":
                            Storage.Ship.goal = [1000, 0, 0]
                        case "2":
                            Storage.Ship.goal = [-1000, 0, 0]
                        case "3":
                            Storage.Ship.goal = [0, 1000, 0]
                        case "4":
                            Storage.Ship.goal = [0, -1000, 0]
                        case "5":
                            Storage.Ship.goal = [0, 0, 1000]
                        case "6":
                            Storage.Ship.goal = [0, 0, -1000]
                
                case "goto":
                    if (command[1].isnumeric()):
                        if (int(command[1]) > len(MenuApi.menus)):
                            Storage.lastMessage = "Error: Menu not found."
                        else:
                            #Renderer.startLoadingAnimation()
                            if (not Storage.loading == 3):
                                Storage.activeMenu = MenuApi.menus[int(command[1])].name

                    elif (MenuApi.index(command[1]) == -1):
                        Storage.lastMessage = "Error: Menu not found."
                    else:
                        #Renderer.startLoadingAnimation()
                        if (not Storage.loading == 3):
                            Storage.activeMenu = command[1]
                case _:
                    if (Storage.activeMenu == "Piloting"):
                        match(command[0]):
                            case "thrust":
                                match = re.match(r"(-?\d+)%?", command[1])
                                if match:
                                    speed = int(match.group(1))
                                    if (speed >= -100 and speed <= 100):
                                        Storage.Ship.thrust = speed
                                    else:
                                        Storage.lastMessage = "Error: Value out of range."
                                else:
                                    Storage.lastMessage = "Error: Invalid percent."

                            case "pitch" | "yaw" |"roll":
                                if command[1].isdecimal() or (command[1][1:].isdecimal() and command[1][0] == "-"):
                                    try:
                                        angle = int(command[1]) # to int
                                        if angle > 180 or angle < -180:
                                            Storage.lastMessage = "Error: Unknown angle."
                                        else:
                                            if (command[0] == "pitch"):
                                                Storage.shipObject.rotation[0] = angle
                                            elif (command[0] == "yaw"):
                                                Storage.shipObject.rotation[1] = angle
                                            elif (command[0] == "roll"):
                                                Storage.shipObject.rotation[2] = angle

                                    except ValueError:
                                        Storage.lastMessage = "Error: Unknown angle."
                                else:
                                    Storage.lastMessage = "Error: Unknown angle."
                            case _:
                                Storage.lastMessage = "Error: Unknown command."
                            

                    elif (Storage.activeMenu == "FTL"):
                        match(command[0]):
                            
                            case _:
                                Storage.lastMessage = "Error: Unknown command."

                    else:
                        Storage.lastMessage = "Error: Unknown command."
        except Exception as e:
            Storage.lastMessage = str(e)

        # End function with this
        Storage.commands[5] = Storage.commands[4]
        Storage.commands[4] = Storage.commands[3]
        Storage.commands[3] = Storage.commands[2]
        Storage.commands[2] = Storage.commands[1]
        Storage.commands[1] = Storage.commands[0]
        Storage.commands[0] = ""