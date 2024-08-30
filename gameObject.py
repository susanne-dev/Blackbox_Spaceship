import numpy as np
from typing import Union

class RotationObject:
    def __init__(self, pos: Union[np.ndarray, list, tuple]) -> None:
        self.Base: np.ndarray = np.array(pos)
        self.Pitch: np.ndarray = self.Base + np.array([-1, 0, 0])
        self.Yaw: np.ndarray = self.Base + np.array([0, 1, 0])
        self.Roll: np.ndarray = self.Base + np.array([0, 0, -1])

    def __copy__(self):
        return RotationObject(self.Base) # Add pitch yaw and roll to copy

    def __repr__(self) -> str:
        return (f"RotationObject(Base={self.Base}, "
                f"Pitch={self.Pitch}, Yaw={self.Yaw}, Roll={self.Roll})")
    
    def __add__(self, pos: Union[np.ndarray, list, tuple]) -> 'RotationObject':
        pos = np.array(pos)  # Convert pos to numpy array
        
        # Ensure pos has the correct shape
        if pos.shape != (3,):
            raise ValueError("Position must be a 3-dimensional vector")
        
        # Initialize a new RotationObject with the updated base position
        newRotationObject = RotationObject((0, 0, 0))
        newRotationObject.Base = self.Base + pos
        newRotationObject.Pitch = self.Pitch + pos
        newRotationObject.Yaw = self.Yaw + pos
        newRotationObject.Roll = self.Roll + pos
        
        return newRotationObject
    
    def rotate_around_axis(self, axis_name: str, theta: float):
        """
        Rotate the points of a RotationObject around a specified axis.

        self: RotationObject, the object containing the points
        axis_name: str, the name of the axis ('pitch', 'yaw', or 'roll')
        theta: float, the angle of rotation in radians
        """
        base = self.Base

        if axis_name == 'pitch':
            axis = self.Pitch - base
            self.Yaw = self.rotate_point_around_line(self.Yaw, base, axis, theta)
            self.Roll = self.rotate_point_around_line(self.Roll, base, axis, theta)
        elif axis_name == 'yaw':
            axis = self.Yaw - base
            self.Pitch = self.rotate_point_around_line(self.Pitch, base, axis, theta)
            self.Roll = self.rotate_point_around_line(self.Roll, base, axis, theta)
        elif axis_name == 'roll':
            axis = self.Roll - base
            self.Pitch = self.rotate_point_around_line(self.Pitch, base, axis, theta)
            self.Yaw = self.rotate_point_around_line(self.Yaw, base, axis, theta)
        else:
            raise ValueError("Invalid axis name. Use 'pitch', 'yaw', or 'roll'.")

    def rotate_point_around_line(self, point, base, axis, theta):
        """
        Rotate a point around a line defined by another point and the base.

        point: np.array, the point to rotate
        base: np.array, the point on the line (base point)
        axis: np.array, the direction of the line
        theta: float, the angle of rotation in radians
        """
        # Translate so the base point is at the origin
        point_translated = point - base
        
        # Normalize the axis vector
        axis = axis / np.linalg.norm(axis)
        
        # Compute the components of the rotation
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        # Rodrigues' rotation formula
        rotated_point = (point_translated * cos_theta +
                        np.cross(axis, point_translated) * sin_theta +
                        axis * np.dot(axis, point_translated) * (1 - cos_theta))
        
        # Translate the point back
        return rotated_point + base

class GameObject:
    position: RotationObject
    health: int
    type: str
    team: int

    rotation: Union[np.ndarray, list]
    velocity: Union[np.ndarray, list]
    dampeners: bool

    def __init__(self, position: RotationObject, health = 20, type = "asteroid", team = -1, rotation = [0, 0, 0], velocity = (0, 0, 0), dampeners = True) -> None:
        self.position = position
        self.health = health
        self.type = type
        self.team = team
        self.rotation = np.array(rotation, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)
        self.dampeners = np.array(dampeners)

    def __copy__(self):
        return GameObject(self.position.__copy__(), self.health, self.type, self.team, self.rotation.copy(), self.velocity.copy(), self.dampeners)