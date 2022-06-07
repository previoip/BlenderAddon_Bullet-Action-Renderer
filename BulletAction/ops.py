from math import radians, log2
from select import select
import bpy
from bpy.types import Operator
from . import utils
from mathutils import Vector, Euler

class BaseOps:
    OBJECTS = bpy.data.objects
    EMPTY_TARGET_NAME = "BA_EMPTY_TARGET"
    CAMERA_NAME = "BA_CAMERA"

### -----------------------

class AddEmptyTarget:
    """ Create Empty Primitive as Camera Base Target on said object """
    bl_idname = 'object.create_empty_on_selected'
    bl_label = "Create Empty Target on Selected"
    
    def execute(self, context):
        coord = Vector((0,0,0))
        rot = Euler((0,0,0))
        dim = Vector((0,0,2))
        offset = 2
        objs = context.selected_objects

        if objs and objs[0].name.startswith(self.EMPTY_TARGET_NAME) :
            objs.pop(0)

        if objs:
            coord, dim, rot = utils.get_bbox_dimensions(objs[0])
            offset = 0

        utils.clear_objects_with_prefix(self.EMPTY_TARGET_NAME)

        bpy.ops.object.empty_add(type='SINGLE_ARROW', radius=2, location=coord, rotation=rot)
        obj = bpy.context.selected_objects[0]
        utils.move_object_along_z_normal(obj, offset)
        obj.name = self.EMPTY_TARGET_NAME
        obj.empty_display_size = abs(dim.z)
        if abs(dim.z) <= 1:
            obj.empty_display_size = 1
        bpy.ops.object.select_all(action='DESELECT')
        if objs:
            objs[0].select_set(True)
        return {'FINISHED'}


class CreateCameraTarget:
    """ Create seperate camera primitive """
    bl_idname = 'object.create_camera_to_target'
    bl_label = "Create Camera to Target or Selected"
    
    def execute(self, context):

        utils.clear_objects_with_prefix(self.CAMERA_NAME)
        
        if self.OBJECTS.find(self.EMPTY_TARGET_NAME) != -1:
            obj_empty = self.OBJECTS[self.EMPTY_TARGET_NAME]
            loc, _, rot = utils.get_bbox_dimensions(obj_empty)
            bpy.ops.object.camera_add(location=loc, rotation=rot)

            obj = bpy.context.selected_objects[0]
            obj.name = self.CAMERA_NAME
            obj.data.type = 'ORTHO' # use prop options
            offset = obj_empty.empty_display_size + log2(obj_empty.empty_display_size + 1) * 8
            utils.move_object_along_z_normal(obj, offset, axis=(0,-1,0))
            obj.rotation_euler.rotate_axis('X', radians(90))
            context.scene.camera = obj

        return {'FINISHED'}

class ClearAddonObjects:
    """ Rendering operation wrapper-ish """
    bl_idname = 'object.clear_addon_objects'
    bl_label = "Deletes all addon objects in Scene"

    def execute(self, context):
        items = [self.EMPTY_TARGET_NAME, self.CAMERA_NAME]
        for item in items:
            utils.clear_objects_with_prefix(item)
        return {'FINISHED'}

class PivotCameraCW:
    """ Rendering operation wrapper-ish """
    bl_idname = 'object.pivot_camera_clockwise'
    bl_label = "Pivots Camera Clockwise"

    def execute(self, context):
        if utils.collection_has_prefix(self.OBJECTS.keys(),name=self.CAMERA_NAME) and utils.collection_has_prefix(self.OBJECTS.keys(), name=self.EMPTY_TARGET_NAME):
            obj_t = self.OBJECTS[self.CAMERA_NAME]
            obj_p = self.OBJECTS[self.EMPTY_TARGET_NAME]
            utils.pivot_object_from_target_z_axis(obj_t, obj_p, 10)
        return {'FINISHED'}


class PivotCameraCCW:
    """ Rendering operation wrapper-ish """
    bl_idname = 'object.pivot_camera_counter_clockwise'
    bl_label = "Pivots Camera Counter Clockwise"

    def execute(self, context):
        if utils.collection_has_prefix(self.OBJECTS.keys(),name=self.CAMERA_NAME) and utils.collection_has_prefix(self.OBJECTS.keys(), name=self.EMPTY_TARGET_NAME):
            obj_t = self.OBJECTS[self.CAMERA_NAME]
            obj_p = self.OBJECTS[self.EMPTY_TARGET_NAME]
            utils.pivot_object_from_target_z_axis(obj_t, obj_p, -10)
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
class ClearAddonObjects_OT_Operator(Operator, ClearAddonObjects, BaseOps): pass
class PivotCameraCCW_OT_Operator(Operator, PivotCameraCCW, BaseOps): pass
class PivotCameraCW_OT_Operator(Operator, PivotCameraCW, BaseOps): pass
class BeginRenderOnTarget_OT_Operator(Operator, BeginRenderOnTarget, BaseOps): pass



classes = (
    AddEmptyTarget_OT_Operator,
    CreateCameraTarget_OT_Operator,
    ClearAddonObjects_OT_Operator,
    PivotCameraCCW_OT_Operator,
    PivotCameraCW_OT_Operator,
    BeginRenderOnTarget_OT_Operator,
)