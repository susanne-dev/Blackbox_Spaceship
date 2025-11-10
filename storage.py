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

    class PowerDist:
        min = 0
        max = 10
        available = max
        values = [0,0,0]

        def add(index: int, action: str):
            indexes = list(range(0, len(Storage.PowerDist.values)))
            indexes.remove(index)
            if action == "+" and Storage.PowerDist.available > Storage.PowerDist.min and Storage.PowerDist.values[index] < Storage.PowerDist.max:
                Storage.PowerDist.values[index] += 1
                Storage.PowerDist.available -= 1
            elif action == "-" and Storage.PowerDist.values[index] > Storage.PowerDist.min:
                Storage.PowerDist.values[index] -= 1
                Storage.PowerDist.available += 1

        def balance():
            partValue = int(Storage.PowerDist.max // len(Storage.PowerDist.values))
            Storage.PowerDist.values = [partValue] * len(Storage.PowerDist.values)
            Storage.PowerDist.available -= partValue * len(Storage.PowerDist.values)
