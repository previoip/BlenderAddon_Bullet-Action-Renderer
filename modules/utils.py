from typing import Dict, Set, Union
from string import ascii_uppercase, hexdigits

import bpy

import random

def hashIDFromString(string: str):
    # fast hashing
    random.seed(string)
    h = random.getrandbits(128)
    return "%032x" % h


def clear_object_with_prefix(prefix: str):
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = [item for item in list(bpy.context.scene.objects) if item.name.startswith(prefix)]
    bpy.ops.object.delete(scene_copy)
        
    object_data = bpy.data.objects
    for i in object_data:
        print(i.name)
    object_data_list = [d for d in object_data if d.name.startswith(prefix)]
    for d in object_data_list:
        camera_data.remove(d)
    