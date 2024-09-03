import random
import math
from typing import Union, Tuple
import numpy as np
import time

from storage import Storage, RotationObject
from gameObject import GameObject, RotationObject
from utility import Utility
from events import EventHandler

#////////////////////////////
# TODO: Add inertia dampeners
#////////////////////////////
            
class Simulation:
    def run(tick: int):

        Simulation.eventTimers()

        if tick == 10:
            for object in Storage.Simulation.objects:
                if Utility.distance(Storage.shipObject.position.Base, object.position.Base) > 4000:
                    Storage.Simulation.objects.remove(object)

            #Storage.Simulation.objects = sorted(Storage.Simulation.objects, key=lambda x: Utility.distance(Storage.shipObject.position.Base, x.position.Base), reverse=True)
            Storage.Simulation.objects = sorted(
                Storage.Simulation.objects,
                key=lambda x: Utility.mapToRelative(Storage.shipObject.position, x.position.Base)[2],
                reverse=True
            )

        # Upon spawn call StartArea()
        for asteroid in Storage.Simulation.objects:
            asteroid.position = Simulation.moveObject(asteroid.position, asteroid.velocity)
            if Utility.distance(Storage.shipObject.position.Base, asteroid.position.Base) <= 150:
                #Storage.Ship.thrust = 0
                Storage.shipObject.velocity = [0, 0, 0]

                if not EventHandler.crashEvent(asteroid):
                    backWards = (Storage.shipObject.position.Base - asteroid.position.Base) / np.linalg.norm(Storage.shipObject.position.Base - asteroid.position.Base)
                    Storage.shipObject.position = Storage.shipObject.position + backWards * 50

                
        Simulation.setShipVelocity(Storage.shipObject)
        Storage.shipObject.position = Simulation.moveObject(Storage.shipObject.position, Storage.shipObject.velocity)
        Simulation.turnShip(Storage.shipObject)
            
    def startArea():
        Storage.Simulation.objects.clear()
        # Set goal
        goalDistance = random.randint(20000, 30000)
        goalAngle = (math.radians(random.randint(0, 359)), math.radians(random.randint(0, 359)))
    
        x = goalDistance * math.sin(goalAngle[0]) * math.cos(goalAngle[1])
        y = goalDistance * math.sin(goalAngle[0]) * math.sin(goalAngle[1])
        z = goalDistance * math.cos(goalAngle[0])

        Storage.Ship.goal = [x, y, z]

        Storage.Ship.goal = [0, 0, 100]

    def setShipVelocity(ship: GameObject) -> None:
        relVelocity = Utility.mapToRelative(ship.position, ship.velocity + ship.position.Base)

        # Apply inertia dampeners
        if relVelocity[0] >= 0.1:
            relVelocity[0] -= 0.05
        elif relVelocity[0] <= -0.1:
            relVelocity[0] += 0.05
        else:
            relVelocity[0] = 0


        if relVelocity[1] >= 0.1:
            relVelocity[1] -= 0.05
        elif relVelocity[1] <= -0.1:
            relVelocity[1] += 0.05
        else:
            relVelocity[1] = 0

        if relVelocity[2] >= Storage.Ship.thrust / 100 * Storage.Ship.maxThrust + 0.2:
            relVelocity[2] -= 0.2
        elif relVelocity[2] <= Storage.Ship.thrust / 100 * Storage.Ship.maxThrust - 0.2:
            relVelocity[2] += 0.2
        else:
            relVelocity[2] = Storage.Ship.thrust / 100 * Storage.Ship.maxThrust

        ship.velocity = Utility.mapToGlobal(ship.position, relVelocity) - ship.position.Base
    
    def moveObject(object: RotationObject, velocity) -> RotationObject:

        object = object + velocity

        return object
    
    def turnShip(ship: GameObject) -> None:
        # Adjust pitch
        if ship.rotation[0] > 0:
            if ship.rotation[0] > 20:
                increment = 5
            elif ship.rotation[0] > 10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("pitch", np.radians(increment))
            ship.rotation[0] -= increment
        elif ship.rotation[0] < 0:
            if ship.rotation[0] < -20:
                increment = 5
            elif ship.rotation[0] < -10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("pitch", np.radians(-increment))
            ship.rotation[0] += increment

        # Adjust yaw
        if ship.rotation[1] > 0:
            if ship.rotation[1] > 20:
                increment = 5
            elif ship.rotation[1] > 10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("yaw", np.radians(increment))
            ship.rotation[1] -= increment
        elif ship.rotation[1] < 0:
            if ship.rotation[1] < -20:
                increment = 5
            elif ship.rotation[1] < -10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("yaw", np.radians(-increment))
            ship.rotation[1] += increment

        # A Adjust roll
        if ship.rotation[2] > 0:
            if ship.rotation[2] > 20:
                increment = 5
            elif ship.rotation[2] > 10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("roll", np.radians(increment))
            ship.rotation[2] -= increment
        elif ship.rotation[2] < 0:
            if ship.rotation[2] < -20:
                increment = 5
            elif ship.rotation[2] < -10:
                increment = 2
            else:
                increment = 1
            ship.position.rotate_around_axis("roll", np.radians(-increment))
            ship.rotation[2] += increment

    def eventTimers():
        Storage.Simulation.EventTimers.start()
        currentTime = time.time()
        if currentTime - Storage.Simulation.EventTimers.asteroids >= 0:
            print("Asteroid cluster incomming")
            Storage.Simulation.EventTimers.asteroids = 0
            velNorm = np.linalg.norm(Storage.shipObject.velocity)
            if velNorm > 0.1:
                clusterCentre = Storage.shipObject.velocity / velNorm * 1000 + Storage.shipObject.position.Base
                Simulation.asteroidCluster(clusterCentre, random.randint(5, 20), 400, 300, 0)
                Simulation.asteroidCluster(clusterCentre, random.randint(1, 3), 300, 0, 0)

    def asteroidCluster(pos: Union[np.ndarray, list, tuple], count: int, maxDist: int, minDist: int = 0, maxSpeed: float = 0) -> None:
        for i in range(count):
            generate = True
            asteroid = (0, 0, 0)
            while generate:
                asteroid = np.array((random.randint(-maxDist, maxDist), random.randint(-maxDist, maxDist), random.randint(-maxDist, maxDist))) + np.array(pos)
                if Utility.distance(pos, asteroid) < maxDist and Utility.distance(pos, asteroid) > minDist:
                    generate = False

            print(asteroid)

            Storage.Simulation.objects.append(GameObject(RotationObject(asteroid), 10, "asteroid", -1, [0, 0, 0], [random.randint(-maxSpeed * 10, maxSpeed * 10) / 10, random.randint(-maxSpeed * 10, maxSpeed * 10) / 10, random.randint(-maxSpeed * 10, maxSpeed * 10) / 10]))