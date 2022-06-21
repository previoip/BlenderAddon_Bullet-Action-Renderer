import os
import bpy
from mathutils import Vector, Matrix, Euler
from math import sqrt, pi 
import random

# typedef
Object = bpy.types.Object

def fast_sha(seed: str, l=128) -> str:
    random.seed(seed)
    h = random.getrandbits(l)
    return "%032x" % h 

def pad_str(string: str, t='NUM', l=6):
    len_string=len(string)
    if len_string >= l:
        return string
    if t == 'STR':
        return string + " "*(l-len_string)
    elif t == 'NUM':
        return "0"*(l-len_string) + str(string)
def normalize_deg(deg, mode='r'):
    if mode == 'r':
        return deg % pi
    elif mode == 'd':
        return deg % 360

def collection_has_prefix(collection, name: str):
    for item in collection:
        if item.startswith(name):
            return True
    return False

def clear_objects_data(objs: list) -> None:
    """ Delete and Clear Objects from Scene-Blendfile """
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = objs
    bpy.ops.object.delete(scene_copy)

def clear_objects_with_prefix(name: str):
    if collection_has_prefix(bpy.data.objects.keys(), name):
        obj_ls = [i for i in bpy.data.objects if i.name.startswith(name)]
        for obj in obj_ls:
            bpy.data.objects.remove(obj, do_unlink=True)

def set_object_loc(obj: Object, loc: Vector = Vector((0, 0, 0))):
    """ Sets object by name in cartesian coordinates """
    obj.location = loc
    return obj

def move_object_loc(obj: Object, loc: Vector = Vector((0, 0, 0))):
    """ Moves object by name in cartesian coordinates """
    loc = Vector(loc)
    obj.location += loc
    return obj

def move_object_along_z_normal(obj: Object, dest: float = 0.0, axis=(0,0,1)):
    axis = Vector(axis)
    dest = axis * dest
    mat_inv = obj.matrix_world.copy()
    mat_inv.invert()
    obj.location += dest @ mat_inv
    return obj

def get_bbox_dimensions(obj: Object):
    """ Returns target object bounding box center-of-mass and dimension """
    rot = obj.rotation_euler.copy()
    dim = obj.dimensions.to_3d()
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    x, y, z = [ [ c[i] for c in corners ] for i in range(3) ]
    fcenter = lambda x: ( max(x) + min(x) ) / 2
    center = [ fcenter(axis) for axis in [x,y,z] ]
    return Vector(center), dim, rot

def pivot_object_from_point(obj: Object, pivot_loc: Vector = Vector((0, 0, 0)), pivot_normal_angle: Vector = Vector((0, 0, 0)), angle: float = .0):
    """ Rotates object along a pivot point and direction, broken and doesnt work """
    pivot_loc = Vector(pivot_loc)
    pivot_normal_angle = Vector(pivot_normal_angle)

    # rotation_rad = radians(rotation_deg)    
    mat_rot = Matrix.Rotation(angle, 4, 'Z')
    mat_angle = Euler(pivot_normal_angle * -1).to_matrix()
    mat_angle_inv = Euler(pivot_normal_angle).to_matrix()

    obj.location -= pivot_loc
    obj.location = obj.location @ mat_angle_inv
    obj.location = obj.location @ mat_rot    
    obj.location = obj.location @ mat_angle
    obj.location += pivot_loc

    return obj


def pivot_object_from_target_local_axis(obj, obj_pivot, angle = .0, axis_str: str ='Z', return_to_original_pos: bool = False):    
    """ Rotates object along a z axis of pivot object and angle increment """
    if angle == 0:
        return obj
    # save selected objecs data to be retirned after function call
    previously_selected = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    # set target (obj) as obj's parent (obj_pivot)
    obj.select_set(state=True)
    obj_pivot.select_set(state=True)
    bpy.context.view_layer.objects.active = obj_pivot
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    # fancy transformation to parent obj (obj_pivot)
    obj_pivot.rotation_euler.rotate_axis(axis_str, angle)

    # unparent everything
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')

    # return everything to initial conditions
    if return_to_original_pos:
        obj_pivot.rotation_euler.rotate_axis(axis_str, angle * -1)
    if previously_selected:
        for o in previously_selected:
            o.select_set(state=True)
        bpy.context.view_layer.objects.active = previously_selected[0]
    return obj


def get_extrema_from_vector(vec: Vector):
    if vec.x >= vec.y and vec.x >= vec.z:
        mag = vec.x
        ax = 'X'
    elif vec.y >= vec.x and vec.y >= vec.z:
        mag = vec.y
        ax = 'Y'
    elif vec.z >= vec.x and vec.z >= vec.y:
        mag = vec.z
        ax = 'Z'
    else:
        mag = max(vec)
        ax = None
    return mag, ax

def is_empty_vector(vec: Vector):
    epsilon = 1e-3
    return vec.x <= epsilon  and vec.y <= epsilon  and vec.z <= epsilon

def radius_from_origin(vec: Vector, ref_point: Vector = Vector((0,0,0))):
    if is_empty_vector(vec - ref_point):
        return 0
    vec = vec - ref_point
    return sqrt(vec.x**2 + vec.y**2 + vec.z**2)

def render_to_filepath(context, target_filepath, target_filename):
    curr_filepath = str(context.scene.render.filepath)
    target_filepath = os.path.join(target_filepath, target_filename)
    context.scene.render.filepath = target_filepath
    print(target_filepath, target_filename)
    bpy.ops.render.render(write_still=True)
    context.scene.render.filepath = curr_filepath
    return 

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)