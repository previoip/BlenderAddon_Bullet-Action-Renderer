import bpy
from bpy.types import Operator
from . import utils
from mathutils import Vector, Euler

class BaseOps:
    OBJECTS = bpy.data.objects
    CAMERA_TARGET_NAME = "BA_CAM_TARGET"

### -----------------------

class AddEmptyTarget:
    """ Create Empty Primitive as Camera Base Target on said object """
    bl_idname = 'object.create_empty_on_selected'
    bl_label = "Create Empty Target on Selected"
    
    def execute(self, context):
        coord = Vector((0,0,0))
        rot = Euler((0,0,0))
        offset = 2
        objs = bpy.context.selected_objects

        if objs and objs[0].name.startswith(self.CAMERA_TARGET_NAME) :
            objs.pop(0)

        if objs:
            coord = objs[0].location.copy()
            rot = objs[0].rotation_euler.copy()

        if utils.collection_has_item(self.OBJECTS.keys(), self.CAMERA_TARGET_NAME):
            obj_ls = [i for i in self.OBJECTS if i.name.startswith(self.CAMERA_TARGET_NAME)]
            for obj in obj_ls:
                self.OBJECTS.remove(obj, do_unlink=True)

        bpy.ops.object.empty_add(type='SINGLE_ARROW', radius=2, location=coord, rotation=rot)
        obj = bpy.context.selected_objects[0]
        utils.move_object_along_z_normal(obj, offset)
        obj.name = self.CAMERA_TARGET_NAME
        bpy.ops.object.select_all(action='DESELECT')
        if objs:
            objs[0].select_set(True)
        return {'FINISHED'}


class CreateCameraTarget:
    """ Create seperate camera primitive """
    bl_idname = 'object.create_camera_to_target'
    bl_label = "Create Camera to Target or Selected"
    
    def execute(self, context):
        return {'FINISHED'}


class BeginRenderOnTarget:
    """ Rendering operation wrapper-ish """
    bl_idname = 'render.render_bullet_action_on_target_or_selected'
    bl_label = "Render Bullet Action on Target or Selected"

    def execute(self, context):
        return {'FINISHED'}


### -----------------------

class AddEmptyTarget_OT_Operator(Operator, AddEmptyTarget, BaseOps): pass
class CreateCameraTarget_OT_Operator(Operator, CreateCameraTarget, BaseOps): pass
class BeginRenderOnTarget_OT_Operator(Operator, BeginRenderOnTarget, BaseOps): pass

classes = (
    AddEmptyTarget_OT_Operator,
    CreateCameraTarget_OT_Operator,
    BeginRenderOnTarget_OT_Operator,
)