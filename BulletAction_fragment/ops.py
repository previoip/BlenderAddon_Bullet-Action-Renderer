import bpy
from bpy.types import Operator
from . import utils

class BaseOps:
    CAMERA_TARGET_NAME = "BA_CAM"


### -----------------------

class AddEmptyTarget:
    """ Create Empty Primitive as Base Target on said object """
    bl_idname = 'object.create_empty_on_selected'
    bl_label = "Create Empty Target on Selected"
    
    def execute(self, context):
        utils.move_object_loc_by_name('Cube', (0,1,0))
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