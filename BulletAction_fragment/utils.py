import imp
import bpy
from mathutils import Vector, Matrix, Euler, Quaternion
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


def normalize_vector(vector: GenericVector):
    if sum(vector) == 1:
        return vector
    return vector / sum(vector)

def clear_objects_data(objs: list) -> None:
    """ Delete and Clear Objects from Scene-Blendfile """
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = objs
    bpy.ops.object.delete(scene_copy)

def set_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))):
    """ Sets object by name in cartesian coordinates, returns final position (Vector) """
    obj = bpy.data.objects[name]
    obj.location = loc
    return obj

def move_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))):
    """ Moves object by name in cartesian coordinates, returns final position (Vector) """
    loc = Vector(loc)
    obj = bpy.data.objects[name]
    obj.location += loc
    return obj

def pivot_object_from_point(name: str, pivot_loc: GenericVector = Vector((0, 0, 0)), pivot_angle: GenericVector = Vector((0, 0, 0)), rotation_deg: float = .0):
    """ Rotates object along a pivot point and direction, returns final position (Vector) """
    obj = bpy.data.objects[name]
    pivot_loc = Vector(pivot_loc)
    pivot_angle = Vector(pivot_angle)
    
    rot_angle = radians(rotation_deg)    
    mat_rot = Matrix.Rotation(rot_angle, 4, 'Z')
    mat_trans = Matrix.Translation(pivot_loc)
    mat_trans_inv = Matrix.Translation(pivot_loc * -1)
    mat_angle = Euler(pivot_angle * -1).to_matrix()
    mat_angle_inv = Euler(pivot_angle).to_matrix()

    obj.location = mat_trans_inv @ obj.location @ mat_angle_inv
    obj.location = obj.location @ mat_rot    
    obj.location = mat_trans @ obj.location @ mat_angle

    return obj
