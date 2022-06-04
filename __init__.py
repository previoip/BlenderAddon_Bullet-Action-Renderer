ID_DEV = True

bl_info = {
    "name": "Render Orthos View",
    'description': 'render 360 degree bullet-action views with some degree of customizability.',
    "category": "Object",
    "location": "Properties > Render > Render Orthos Addon",
    "support": "TESTING",
    "blender": (2, 80, 0),
    'version': (0, 1, 1),
    'author': 'Previo Prakasa'
}

import bpy, addon_utils



def dev_init():
    import os, sys
    curr_dir = bpy.path.abspath('//')
    curr_dir = os.path.abspath(os.path.join(curr_dir, '..'))
    if not curr_dir in sys.path:
        sys.path.append(curr_dir)

if ID_DEV:
    dev_init()

# import atexit
# from bpy.app.handlers import persistent
from bpy.props import BoolProperty, EnumProperty, PointerProperty, CollectionProperty, StringProperty
from bpy.types import AddonPreferences, PropertyGroup, Operator
import os, sys, math
# from . import addon_ui
import BulletAction_fragment

class BulletActionAScene(PropertyGroup):
    # tool: PointerProperty(type=BulletAction_fragment.props)
    # tool: PointerProperty(type=curve_tools.props.AnimAideTool)
    pass


classes = \
    BulletAction_fragment.classes + \
    (BulletActionAScene, )

    # addon_ui.classes + \

# @persistent
# def load_post_handler(scene):
#     print('init')



def register():
    if ID_DEV:
        unregister()
    
    for cls in classes:
        print('registering:', cls)
        bpy.utils.register_class(cls)
    bpy.types.Scene.bulletActionAddon = PointerProperty(type=BulletActionAScene)
    # preferences = bpy.context.preferences

def unregister():
    for cls in reversed(classes):
        print('unregistering:', cls)
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as e:
            print(e)
    try:
        del bpy.types.Scene.bulletActionAddon
    except AttributeError:
        pass

if __name__ == "__main__":
    register()