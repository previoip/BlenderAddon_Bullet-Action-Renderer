import bpy
from bpy.props import PointerProperty, StringProperty, IntProperty
import os, sys, math

bl_info = {
    "name": "Render Orthos View",
    "category": "Object",
    "location": "Properties > Render > Render Orthos Addon",
    "support": "TESTING",
    "blender": (2, 80, 0),
    'version': (0, 1, 0),
    'author': 'Previo Prakasa',
    'description': 'render otho views with some degree of customizability'
}


# Makes sure its on the correct path (should there be need for testing outside of main blender file)
curr_dir = os.path.dirname(bpy.data.filepath)
if not curr_dir:
    curr_dir = bpy.path.abspath('//')

if not curr_dir in sys.path:
    sys.path.append(curr_dir)

# Modules registration
# from modules.Fragments import MainPanel, OpsCreateEmpty
from modules import utils


def delete_object_with_prefix(prefix: str):
    scene_copy = bpy.context.copy()
    scene_copy['selected_objects'] = [item for item in list(bpy.context.scene.objects) if item.name.startswith(prefix)]
    bpy.ops.object.delete(scene_copy)
        
    object_data = bpy.data.objects
    for i in object_data:
        print(i.name)
    object_data_list = [d for d in object_data if d.name.startswith(prefix)]
    for d in object_data_list:
        object_data.remove(d)
    

class AddonProperties(bpy.types.PropertyGroup):
    bl_idname = "scene.create_empty_on_selected"

    output_subpath: StringProperty(
        name="Output Subpath",
        description=":",
        default="/export",
        maxlen=1024,
        )


class CreateEmpty(bpy.types.Operator):
    bl_idname = "object.create_empty_on_selected"
    bl_label = "Create Empty Target on Selected"
    
    def execute(self, context):
        t_name = "EMPTY_CAMERA_TARGET"
        o_selected = bpy.context.selected_objects[0]
        o_loc = o_selected.location
        
        delete_object_with_prefix(t_name)
        bpy.ops.object.empty_add(type='SPHERE', location=o_loc)
        
        o_selected = bpy.context.selected_objects[0]
        o_selected.name = t_name
        return {'FINISHED'}

class CreateCameraPreview(bpy.types.Operator):
    bl_idname = "object.create_camera_on_target"
    bl_label = "Create Camera on Target"
    
    def execute(self, context):
        t_name = "EMPTY_CAMERA_TARGET"
        o_selected = bpy.context.selected_objects[0]
        o_loc = o_selected.location
        
        delete_object_with_prefix(t_name)
        bpy.ops.object.empty_add(type='SPHERE', location=o_loc)
        
        o_selected = bpy.context.selected_objects[0]
        o_selected.name = t_name
        return {'FINISHED'}

class AddonUI(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_PreviewCameraView'
    bl_label = "Render Orthos"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        layout.label(text="[Render Orthos]")

        init_layout = layout.box()
        init_layout.label(text="Initialization")
        # init_layout.operator("object.select_all").action = 'TOGGLE'
        init_layout.operator("object.create_empty_on_selected")

        render_ops_layout = layout.box()
        render_ops_layout.label(text="Render Operation")
        render_ops_layout.prop(scene.ortho_renderer_properties, "output_subpath")

classses = [
    # props
    AddonProperties,

    # ops
    CreateEmpty,
    CreateCameraPreview,

    # container
    AddonUI
]


def register():
    unregister()
    for c in classses:
        print('registering... %s' %(c.bl_idname) )
        bpy.utils.register_class(c)

    bpy.types.Scene.ortho_renderer_properties = PointerProperty(type=AddonProperties)
    
    print('registered', end="\n\n")

def unregister():

    for c in classses:
        print('unregistering... %s' %(c.bl_idname) )
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            print('\'%s\' may not yet be registered, skipping unregistration process' %(c.bl_idname) )

    print('unregistered', end="\n\n")

if __name__ == "__main__":
    register()