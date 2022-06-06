import imp
import bpy
from mathutils import Vector, Matrix, Euler, Quartenion
from math import radians, sin, cos, sqrt, pi
from typing import Union, TypeAlias
import random

# typedef
GenericVector: TypeAlias = Union[list[float, int], tuple[float, int], Vector]

def fast_sha(seed: str) -> str:
    random.seed(seed)
    h = random.getrandbits(128)
    return "%032x" % h 

def normalize_deg(deg, mode='r'):
    if mode == 'r':
        return deg % pi
    elif mode == 'd':
        return deg % 360


def normalize_vector(vector: GenericVector) -> Vector:
    if sum(vector) == 1:
        return vector
    return vector / sum(vector)

def clear_objects_data(objs: list) -> None:
    """ Delete and Clear Objects from Scene-Blendfile """
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = objs
    bpy.ops.object.delete(scene_copy)

def set_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))) -> Vector:
    """ Sets object by name in cartesian coordinates, returns final position (Vector) """
    obj = bpy.data.objects[name]
    obj.location = loc
    return Vector(obj.location)

def move_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))) -> Vector:
    """ Moves object by name in cartesian coordinates, returns final position (Vector) """
    loc = Vector(loc)
    obj = bpy.data.objects[name]
    obj.location += loc
    return Vector(obj.location)

def pivot_object_from_point(name: str, pivot: GenericVector = Vector((0, 0, 0)), axis: GenericVector = Vector((0, 0, 0)), angle_deg: float = .0) -> Vector:
    """ Rotates object along a pivot point and direction, returns final position (Vector) """
    obj = bpy.data.objects[name]
    loc = Vector(obj.location)
    pivot = Vector(pivot)
    angle = radians(angle_deg)    
    axis = Vector(axis)
    
    tetha = axis * angle
    
    _x, _y, _z = obj.location.copy()
    _ax, _ay, _az = Vector(obj.rotation_euler) + tetha
    _dx, _dy, _dz = loc - pivot
    _r = sqrt(sum(( _dx**2, _dy**2, _dz**2) ))
    
    mat_rot = Matrix.Rotation(angle, 4, 'Z')
    
    obj.location = loc @ mat_rot
    obj.rotation_euler =  (normalize_deg(_ax), normalize_deg(_ay), normalize_deg(_az))

    return Vector(obj.location), Vector(obj.rotation_euler)
