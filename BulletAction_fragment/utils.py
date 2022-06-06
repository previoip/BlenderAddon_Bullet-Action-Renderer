import imp
import bpy
from mathutils import Vector, Matrix, Euler, Quaternion
from math import radians, sin, cos, sqrt, pi 
from typing import Union
import random

# typedef
Object = bpy.types.Object

def fast_sha(seed: str) -> str:
    random.seed(seed)
    h = random.getrandbits(128)
    return "%032x" % h 

def normalize_deg(deg, mode='r'):
    if mode == 'r':
        return deg % pi
    elif mode == 'd':
        return deg % 360

def clear_objects_data(objs: list) -> None:
    """ Delete and Clear Objects from Scene-Blendfile """
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = objs
    bpy.ops.object.delete(scene_copy)

def set_object_loc_by_name(obj: Object, loc: Vector = Vector((0, 0, 0))):
    """ Sets object by name in cartesian coordinates """
    obj.location = loc
    return obj

def move_object_loc_by_name(obj: Object, loc: Vector = Vector((0, 0, 0))):
    """ Moves object by name in cartesian coordinates """
    loc = Vector(loc)
    obj.location += loc
    return obj

def move_object_along_z_normal(obj: Object, dest: float = 0.0):
    dest = Vector((0,0,dest))
    mat_inv = obj.matrix_world.copy()
    mat_inv.invert()
    obj.location += dest @ mat_inv
    return obj

def get_bbox_sizes(obj: Object):
    """ Returns target object bounding box center-of-mass and sizes """
    return [0,0,0], [0,0,0]

def pivot_object_from_point(obj: Object, pivot_loc: Vector = Vector((0, 0, 0)), pivot_normal_angle: Vector = Vector((0, 0, 0)), rotation_deg: float = .0):
    """ Rotates object along a pivot point and direction """
    pivot_loc = Vector(pivot_loc)
    pivot_normal_angle = Vector(pivot_normal_angle)

    rot_angle = radians(rotation_deg)    
    mat_rot = Matrix.Rotation(rot_angle, 4, 'Z')
    mat_trans = Matrix.Translation(pivot_loc)
    mat_trans_inv = Matrix.Translation(pivot_loc * -1)
    mat_angle = Euler(pivot_normal_angle * -1).to_matrix()
    mat_angle_inv = Euler(pivot_normal_angle).to_matrix()

    obj.location = mat_trans_inv @ obj.location @ mat_angle_inv
    obj.location = obj.location @ mat_rot    
    obj.location = mat_trans @ obj.location @ mat_angle

    return obj
