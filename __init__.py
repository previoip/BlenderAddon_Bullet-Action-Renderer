IF_DEV = True

bl_info = {
    "name": "BulletAction or 360 view rendering util idk",
    'description': 'render 360 degree bullet-action views with some degree of customizability. mainly for autogenerating sprites from 3D assets',
    "category": "Object",
    "location": "Properties > Render > Render Orthos Addon",
    "support": "TESTING",
    "blender": (2, 80, 0),
    'version': (0, 1, 1),
    'author': 'Previo Prakasa'
}

from email.policy import default
from unicodedata import name
import bpy

def dev_init():
    import os, sys
    curr_dir = bpy.path.abspath('//')
    curr_dir = os.path.abspath(os.path.join(curr_dir, '..'))
    if not curr_dir in sys.path:
        sys.path.append(curr_dir)

if IF_DEV:
    dev_init()

from bpy.props import PointerProperty, BoolProperty, IntProperty, FloatProperty, CollectionProperty, StringProperty
from bpy.types import PropertyGroup
import BulletAction


class BulletActionScenePropertyGroup(PropertyGroup):
    addn_export_folder: StringProperty(
        name="subfolder export", 
        default="export"
        )
    addn_render_type: BoolProperty(
        name="Render as Bulletaction"
        )
    cam_incl: FloatProperty(
        name="Inclination", 
        default=57.3, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_incr: IntProperty(
        name="Increment", 
        default=8, 
        min=1, 
        max=36
        )
    cam_rot_offset: FloatProperty(
        name="Offset Angle", 
        default=0, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_dist_offset: FloatProperty(
        name="Offset Distance", 
        min=0,
        default=1, 
        max=1000
        )
    other_cam_pivot_angle: FloatProperty(
        name="Pivot Angle", 
        default=45, 
        min=-180, 
        max=180, 
        precision=2,
        subtype='ANGLE'
        )


classes = \
    (BulletActionScenePropertyGroup, ) + \
    BulletAction.classes 


def register():
    if IF_DEV:
        unregister()
    
    for cls in classes:
        print('registering:', cls)
        bpy.utils.register_class(cls)

    bpy.types.Scene.bulletActionAddon_settings = PointerProperty(type=BulletActionScenePropertyGroup)

def unregister():
    for cls in classes:
        print('unregistering:', cls)
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as e:
            print(e)
    try:
        del bpy.types.Scene.bulletActionAddon_settings
    except AttributeError as e:
        print(e)

if __name__ == "__main__":
    register()