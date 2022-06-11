from math import radians, degrees, log2, pi
import os
import bpy
from bpy.types import Operator
from mathutils import Vector, Euler
from . import utils

class BaseOps:
    EMPTY_TARGET_NAME = "BA_EMPTY_TARGET"
    CAMERA_NAME = "BA_CAMERA"

### -----------------------

class AddEmptyTarget:
    """ Create Empty Primitive as Camera Base Target on said object """
    bl_idname = 'object.create_empty_on_selected'
    bl_label = "Create Empty Target on Selected"
    
    def execute(self, context):
        scene = context.scene
        addon_prop = scene.bulletActionAddon_settings

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
            addon_prop.priv_t_obj_name = objs[0].name

        addon_prop.priv_t_obj_dimensions = dim
        return {'FINISHED'}


class CreateCameraTarget:
    """ Create seperate camera primitive """
    bl_idname = 'object.create_camera_to_target'
    bl_label = "Create Camera to Target or Selected"
    def execute(self, context):
        scene = context.scene
        addon_prop = scene.bulletActionAddon_settings
        objects = scene.objects
        utils.clear_objects_with_prefix(self.CAMERA_NAME)
        
        if utils.collection_has_prefix(objects.keys(), self.EMPTY_TARGET_NAME):
            incl = addon_prop.cam_incl
            offset_dist = addon_prop.cam_dist_offset
            # offset_rot = addon_prop.cam_rot_offset
            incl = addon_prop.cam_incl
            dim = Vector(addon_prop.priv_t_obj_dimensions)

            obj_empty = objects[self.EMPTY_TARGET_NAME]
            if addon_prop.cam_dist_offset_auto :
                offset_dist = obj_empty.empty_display_size + log2(obj_empty.empty_display_size + 1) * 8
            else:
                offset_dist = addon_prop.cam_dist_offset
    
            loc, _, rot = utils.get_bbox_dimensions(obj_empty)
            bpy.ops.object.camera_add(location=loc, rotation=rot)

            obj = context.selected_objects[0]
            obj.name = self.CAMERA_NAME
            obj.data.type = addon_prop.cam_type_enum
            obj.data.show_sensor = True
            obj.data.show_limits = True

            dim_max, _ = utils.get_extrema_from_vector(dim)
            perim = utils.radius_from_origin(dim/2, loc)

            obj.data.clip_start = max(.0001, offset_dist - perim * addon_prop.cam_dist_clip_multi)
            obj.data.clip_end = max(.0001, offset_dist + perim * addon_prop.cam_dist_clip_multi)

            viewport_x, viewport_y = context.scene.render.resolution_y, context.scene.render.resolution_x
            if viewport_y > viewport_x:
                viewport_ratio = viewport_y / viewport_x
            elif viewport_x > viewport_y:
                viewport_ratio = viewport_x / viewport_y
            else:
                viewport_ratio = 1

            if addon_prop.cam_type_enum == 'ORTHO' and addon_prop.cam_scale_auto:
                obj.data.ortho_scale = perim * viewport_ratio + dim_max

            utils.move_object_along_z_normal(obj, offset_dist, axis=(0,-1,0))
            obj.rotation_euler.rotate_axis('X', radians(90))
            utils.pivot_object_from_target_local_axis(obj, obj_empty, incl * -1, axis_str='X', return_to_original_pos=True)

            context.scene.camera = obj

        return {'FINISHED'}


class ClearAddonObjects:
    bl_idname = 'object.clear_addon_objects'
    bl_label = "Deletes all addon objects in Scene"

    def execute(self, context):
        items = [self.EMPTY_TARGET_NAME, self.CAMERA_NAME]
        for item in items:
            utils.clear_objects_with_prefix(item)
        return {'FINISHED'}

class PivotCameraCW:
    bl_idname = 'object.pivot_camera_clockwise'
    bl_label = "Pivots Camera Clockwise"

    def execute(self, context):
        scene = context.scene
        objects = scene.objects
        addon_prop = scene.bulletActionAddon_settings
        pivot_angle_incr = addon_prop.other_cam_pivot_angle
        if pivot_angle_incr == 0:
            return {'FINISHED'}
        if utils.collection_has_prefix(objects.keys(),name=self.CAMERA_NAME) and utils.collection_has_prefix(objects.keys(), name=self.EMPTY_TARGET_NAME):
            obj_t = objects[self.CAMERA_NAME]
            obj_p = objects[self.EMPTY_TARGET_NAME]
            utils.pivot_object_from_target_local_axis(obj_t, obj_p, pivot_angle_incr)
        return {'FINISHED'}


class PivotCameraCCW:
    bl_idname = 'object.pivot_camera_counter_clockwise'
    bl_label = "Pivots Camera Counter Clockwise"

    def execute(self, context):
        scene = context.scene
        objects = scene.objects
        addon_prop = scene.bulletActionAddon_settings
        pivot_angle_incr = addon_prop.other_cam_pivot_angle
        if pivot_angle_incr == 0:
            return {'FINISHED'}
        if utils.collection_has_prefix(objects.keys(),name=self.CAMERA_NAME) and utils.collection_has_prefix(objects.keys(), name=self.EMPTY_TARGET_NAME):
            obj_t = objects[self.CAMERA_NAME]
            obj_p = objects[self.EMPTY_TARGET_NAME]
            utils.pivot_object_from_target_local_axis(obj_t, obj_p, pivot_angle_incr * -1)
        return {'FINISHED'}


class PivotCameraReset:
    bl_idname = 'object.pivot_camera_reset'
    bl_label = "Reset Pivot Rotation"

    def execute(self, context):
        scene = context.scene
        objects = scene.objects
        if utils.collection_has_prefix(objects.keys(),name=self.CAMERA_NAME) and utils.collection_has_prefix(objects.keys(), name=self.EMPTY_TARGET_NAME):
            obj_t = objects[self.CAMERA_NAME]
            obj_p = objects[self.EMPTY_TARGET_NAME]
            utils.pivot_object_from_target_local_axis(obj_t, obj_p, degrees(obj_p.rotation_euler.z) * -1)
        return {'FINISHED'}


class BeginRenderOnTarget:
    """ Rendering operation wrapper-ish """
    bl_idname = 'render.begin_render'
    bl_label = "Render Bullet Action on Target or Selected"

    def execute(self, context):
        scene = context.scene
        # this script asserts export file format as bitmap only.
        if scene.render.image_settings.file_format not in ['PNG', 'BMP', 'JPEG', 'JPEG2000', 'TARGA']:
            return {'CANCELLED'}
        addon_prop = scene.bulletActionAddon_settings
        objects = scene.objects
        startframe = scene.frame_start 
        stopframe = scene.frame_end 
        # nframe = stopframe - startframe
        incr_n = addon_prop.cam_incr
        incr_rot = 2 * pi / incr_n
        frame_skip = 1
        if addon_prop.addn_render_useframeskip:
            frame_skip = addon_prop.addn_render_frameskip

        camera = objects[self.CAMERA_NAME]
        pivot = objects[self.EMPTY_TARGET_NAME]
        fp = scene.render.filepath
        previously_selected = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        target_action = ""
        if utils.collection_has_prefix(objects.keys(), addon_prop.priv_t_obj_name):
            target_object = objects[addon_prop.priv_t_obj_name]
            target_object.select_set(True)
            target_action = target_object.animation_data.action.name if target_object.animation_data is not None and target_object.animation_data.action is not None else target_object.name
            bpy.ops.object.select_all(action='DESELECT')
        if target_action:
            fp = os.path.join(fp, target_action)
            utils.mkdir(fp)
        for i in range(incr_n):
            if not addon_prop.addn_render_isanimated:
                for frame in range(startframe, stopframe, frame_skip):
                    context.scene.frame_set(frame)
                    filename = f'{target_action}_f{frame:04}_d{int(degrees(i*incr_rot)):03}'
                    exportpath = os.path.join(fp, f'view_{int(degrees(i*incr_rot)):03}')
                    utils.mkdir(exportpath)
                    utils.render_to_filepath(context=context, target_filepath=exportpath, target_filename=filename)
            else:
                frame = context.scene.frame_current
                filename = f'{target_action}_f{frame:04}_d{int(degrees(i*incr_rot)):03}'
                exportpath = os.path.join(fp, f'view_{int(degrees(i*incr_rot)):03}')
                utils.mkdir(exportpath)
                utils.render_to_filepath(context=context, target_filepath=exportpath, target_filename=filename)
            utils.pivot_object_from_target_local_axis(camera, pivot, incr_rot)

        if previously_selected:
            for o in previously_selected:
                o.select_set(state=True)
        context.view_layer.objects.active = previously_selected[0]

        return {'FINISHED'}


class TestRenderOnTarget:
    """ Rendering operation wrapper-ish """
    bl_idname = 'render.test_render'
    bl_label = "Render Bullet Action on Target or Selected"

    def execute(self, context):
        scene = context.scene
        objects = scene.objects
        addon_prop = scene.bulletActionAddon_settings
        incr_n = addon_prop.cam_incr
        incr_rot = 2 * pi / incr_n
        for i in range(incr_n):
            pass
            # rotates, set file output name,renders
        # reset position
        return {'FINISHED'}

### -----------------------

class AddEmptyTarget_OT_Operator(Operator, AddEmptyTarget, BaseOps): pass
class CreateCameraTarget_OT_Operator(Operator, CreateCameraTarget, BaseOps): pass
class ClearAddonObjects_OT_Operator(Operator, ClearAddonObjects, BaseOps): pass
class PivotCameraCCW_OT_Operator(Operator, PivotCameraCCW, BaseOps): pass
class PivotCameraCW_OT_Operator(Operator, PivotCameraCW, BaseOps): pass
class PivotCameraReset_OT_Operator(Operator, PivotCameraReset, BaseOps): pass
class BeginRenderOnTarget_OT_Operator(Operator, BeginRenderOnTarget, BaseOps): pass
class TestRenderOnTarget_OT_Operator(Operator, TestRenderOnTarget, BaseOps): pass

classes = (
    AddEmptyTarget_OT_Operator,
    CreateCameraTarget_OT_Operator,
    ClearAddonObjects_OT_Operator,
    PivotCameraCCW_OT_Operator,
    PivotCameraCW_OT_Operator,
    PivotCameraReset_OT_Operator,
    TestRenderOnTarget_OT_Operator,
    BeginRenderOnTarget_OT_Operator,
)