import numpy as np
import math
from typing import Tuple

from gameObject import GameObject, RotationObject

class Utility:
    def distance(p1: np.ndarray, p2: np.ndarray) -> float:
        distX = p2[0] - p1[0]
        distY = p2[1] - p1[1]
        distZ = p2[2] - p1[2]

        return math.sqrt(distX * distX + distY * distY + distZ * distZ)
    
    def angle(p1, p2) -> Tuple[float, float]:
        try:
            dist = Utility.distance(p1, p2)
            
            theta = math.acos((p2[2] - p1[2]) / dist)
            phi = math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))

            return theta, phi
        
        except ValueError as e:
            print(f"ValueError: {e}")
            return 0.0, 0.0
        except Exception as e:
            print(f"Unkown error: {e}")
            return 0.0, 0.0
        
    def mapToRelative(rotation_object: RotationObject, pos2: np.ndarray) -> np.ndarray:
        """
        Map a global coordinate (pos2) to a coordinate relative to the RotationObject's local system.

        :param rotation_object: RotationObject containing Base, Pitch, Yaw, and Roll.
        :param pos2: The position to map to the local coordinate system of the RotationObject.
        :return: A numpy array representing the position in the RotationObject's local coordinate system.
        """
        # Calculate the global vector from the RotationObject's Base to pos2
        global_vector = pos2 - rotation_object.Base
        
        # Get the local axes of the RotationObject
        # To get local x, y, z directions in global coordinates
        local_x = rotation_object.Base - rotation_object.Pitch
        local_y = rotation_object.Yaw - rotation_object.Base
        local_z = rotation_object.Base - rotation_object.Roll

        # Normalize local directions
        local_x = local_x / np.linalg.norm(local_x)
        local_y = local_y / np.linalg.norm(local_y)
        local_z = local_z / np.linalg.norm(local_z)

        # Calculate the dot products to project the global vector onto the local axes
        relative_x = np.dot(global_vector, local_x)
        relative_y = np.dot(global_vector, local_y)
        relative_z = np.dot(global_vector, local_z)

        return np.array([relative_x, relative_y, relative_z])
    
    def mapToGlobal(rotation_object: RotationObject, local_pos: np.ndarray) -> np.ndarray:
        """
        Map a coordinate from the RotationObject's local coordinate system to the global coordinate system.
        :param rotation_object: RotationObject containing Base, Pitch, Yaw, and Roll.
        :param local_pos: The position in the RotationObject's local coordinate system.
        :return: A numpy array representing the position in the global coordinate system.
        """
        # Get the local axes of the RotationObject
        local_x = rotation_object.Base - rotation_object.Pitch
        local_y = rotation_object.Yaw - rotation_object.Base
        local_z = rotation_object.Base - rotation_object.Roll
        
        # Normalize local directions
        local_x = local_x / np.linalg.norm(local_x)
        local_y = local_y / np.linalg.norm(local_y)
        local_z = local_z / np.linalg.norm(local_z)
        
        # Reconstruct the global position from the local coordinates
        global_vector = (
            local_x * local_pos[0] +
            local_y * local_pos[1] +
            local_z * local_pos[2]
        )
        
        # Add the Base position to get the global coordinates
        global_pos = rotation_object.Base + global_vector
        
        return global_pos
