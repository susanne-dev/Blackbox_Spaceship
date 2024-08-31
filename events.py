from gameObject import GameObject, RotationObject
from storage import Storage
from utility import Utility
from sounds import SoundPlayer

# For communications with other clients and events
# Server -> Clients 
# OR
# Client -> Server -> Clients

#class MessageHandler:
    #runClient() read messages from server and update values. Run this every frame if client
    #sendToClients() send messages to clients. Run this every frame if server

class EventHandler:
    def crashEvent(object: GameObject) -> bool:
        speedDiff = Utility.distance(Storage.shipObject.velocity, object.velocity)
        EventHandler.damageEvent(Storage.shipObject, speedDiff * 3)
        EventHandler.damageEvent(object, speedDiff * 3)

        print(object.health)
        
        SoundPlayer.Effects.Crash()

        if object.health <= 0:
            Storage.Simulation.objects.remove(object)
            return True
        return False

    def damageEvent(object: GameObject, damage: int) -> bool:
        object.health -= damage
        #TODO: damage random system

        return False
