import time
import random

from gameObject import GameObject, RotationObject

class Storage:
    cursorFrame = 0
    lastMessage = ""
    commands = ["", "", "", "", "", ""] #0: current    1-5: memory
    commandIndex = 0

    loading = 0 # 0: None    1: Normal    2: Long    3: Long + Failure    4-5: Easter eggs
    loadingCounter = 0

    activeMenu = "Index" # main(?), Index, Piloting, Guns, Systems

    class Simulation:
        objects = [
            GameObject(RotationObject((200, 0, 200))),
            GameObject(RotationObject((200, 200, 0))),
            GameObject(RotationObject((100, 0, 0))),
            GameObject(RotationObject((-100, 0, 0))),
            GameObject(RotationObject((0, 0, 100))),
            GameObject(RotationObject((0, 0, -100)))
        ]
        class EventTimers:
            asteroids: int = 0

            def start():
                if Storage.Simulation.EventTimers.asteroids == 0:
                    Storage.Simulation.EventTimers.asteroids = time.time() + random.randint(30, 50)
                    #Storage.Simulation.EventTimers.asteroids = time.time() + random.randint(10, 20)

            def stop():
                Storage.Simulation.EventTimers.asteroids = 0

    shipObject = GameObject(RotationObject((0, 0, 0)), 500, "player", 0, (0,0,0), (0,0,0))
    class Ship:
        goal = []
        thrust = 0.0    # Percent
        maxThrust = 5.0 # m/s

    class FTLMenu:
        completed = 0
        stage = 1 # 1 for move horizontal 2 for move vertical
        mark = [0, 0]
        horizontal = 0 #0 to 100
        vertical = 0 #0 to 100
