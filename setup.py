import bpy
from bpy.props import PointerProperty
import os, sys


curr_dir = os.path.dirname(bpy.data.filepath)
if not curr_dir:
    curr_dir = bpy.path.abspath('//')

if not curr_dir in sys.path:
    sys.path.append(curr_dir)

from modules import utils, config

print(config.bl_info)

bl_info = {
    "name": "Render Orthos",
    "blender": (2, 80, 0),
    "category": "Object",
    'version': (0, 1, 0),
    'author': 'Previo Prakasa',
    'description': 'render otho views with '
}

# Side Pannel
class MainPanel(bpy.types.Panel):
    
    bl_idname = 'TEST_PT_Panel'
    bl_label = bl_info['name']
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        layout.label(text=bl_info['name'])

        object_selection = layout.row()
        object_selection_col = object_selection.column()
        object_selection_col.prop(scene, "objects_selection")


        box_render = layout.box()
        box_render.label(text="Render")
        box_render.operator("object.select_all").action = 'TOGGLE'


classses = [
    MainPanel,
]

def register():
    print('registering... %s' %(bl_info['name']) )
    
    bpy.types.Scene.objects_selection = PointerProperty(
        name="Select Object",
        type=bpy.types.Object,
    )
    
    for P in classses:
        bpy.utils.register_class(P)

    print('registered')

def unregister():
    print('unregistering... %s' %(bl_info['name']) )

    for P in classses:
        bpy.utils.unregister_class(P)
    del bpy.types.Scene.objects_selection

    print('unregistered')

if __name__ == "__main__":
    register()