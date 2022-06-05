import imp
import bpy
from mathutils import Vector, Matrix, Euler, Quartenion
from math import radians, sin, cos
from typing import Union, TypeAlias
import random

# typedef
GenericVector: TypeAlias = Union[list[float, int], tuple[float, int], Vector]

def fast_sha(seed: str) -> str:
    random.seed(seed)
    h = random.getrandbits(128)
    return "%032x" % h 

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
    _x, _y, _z = list(obj.location)
    _ax, _ay, _az = list(obj.rotation_euler)
    _r = sqrt(sum(( (pivot[0] - _x)**2, (pivot[1] - _y)**2, (pivot[2] - _z)**2) ))
    angle_deg = radians(angle_deg)    
    axis = Vector(axis)

    _ax, _ay, _az = _ax+angle_deg*axis[0], _ay+angle_deg*axis[1], _az+angle_deg*axis[2]    
    _x = _r * cos(_ax) + pivot[0]
    _y = _r * sin(_ay) + pivot[1]
    _z = _r * cos(_az) + pivot[2]
    
    obj.location = (_x, _y, _z)
    obj.rotation_euler = (_ax, _ay, _az)

    return Vector(obj.location), Vector(obj.rotation_euler)
