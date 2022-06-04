import bpy
from mathutils import Vector
from typing import Union, TypeAlias
import random

# typedef
GenericVector: TypeAlias = Union[list[float, int], tuple[float, int], Vector]

def fast_sha(seed: str) -> str:
    random.seed(string)
    h = random.getrandbits(128)
    return "%032x" % h 

def clear_object_data(obj) -> None:
    """ Delete and Clear Objects from Scene-Blendfile """
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = [item for item in list(bpy.context.scene.objects) if item.name.startswith(prefix)]
    bpy.ops.object.delete(scene_copy)

def set_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))) -> Vector:
    """ Sets object by name in cartesian coordinates, returns final position (Vector) """
    obj = bpy.data.objects[name]
    obj.location = loc
    return obj.location

def move_object_loc_by_name(name: str, loc: GenericVector = Vector((0, 0, 0))) -> Vector:
    """ Moves object by name in cartesian coordinates, returns final position (Vector) """
    obj = bpy.data.objects[name]
    obj.location = obj.location + Vector(loc)
    return obj.locationx

def rotate_object_from_pivot(name: str, pivot) -> Vector:
    """ Rotates object along a pivot point and direction, returns final position (Vector) """
    pass
