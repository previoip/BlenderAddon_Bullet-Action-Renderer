bl_info = {
    'name': 'BulletAction Render Toolkit',
    'description': 'render 360 degree bullet-action views with some degree of customizability.',
    'category': 'Render',
    'location': 'View3D > Properties > Render',
    'support': 'COMMUNITY',
    'blender': (2, 80, 0),
    'version': (0, 2, 1),
    'author': 'Previo Prakasa'
}

import bpy

# run as script
load_from_script_tab = __name__ == '__main__'

if load_from_script_tab:
    import os, sys
    curr_dir = bpy.path.abspath('//')
    curr_dir = os.path.abspath(os.path.join(curr_dir, '..'))
    if not curr_dir in sys.path:
        sys.path.append(curr_dir)

from bpy.props import PointerProperty
from bpy.types import PropertyGroup
import BulletAction


classes = \
    () + \
    BulletAction.classes 


def register():
    if load_from_script_tab:
        unregister()

    for cls in classes:
        print('registering:', cls)
        bpy.utils.register_class(cls)

    bpy.types.Scene.bulletActionAddon_settings = PointerProperty(type=BulletAction.props.BulletActionScenePropertyGroup)

def unregister():
    for cls in classes:
        print('unregistering:', cls)
        try:
            bpy.utils.unregister_class(cls)
        except (RuntimeError, AttributeError) as e:
            print(e)
    try:
        del bpy.types.Scene.bulletActionAddon_settings
    except AttributeError as e:
        print(e)

if load_from_script_tab:
    register()