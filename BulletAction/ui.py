import bpy
from . import support
from bpy.types import Panel

class BULLETACTION_layout:
    bl_label = 'Bullet-Action Render Toolkit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        # layout.label(text="My Select Panel")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        addon_prop = scene.bulletActionAddon_settings

        box = layout.box()

        box.label(text="Initialize Addon")

        col = box.column(align=True)
        col.prop(addon_prop, 'cam_incl', slider=False)
        col.prop(addon_prop, 'cam_incr', slider=False)
        col.prop(addon_prop, 'cam_rot_offset', slider=False)
        col.prop(addon_prop, 'cam_dist_offset', slider=False)

        row = box.row(align=True)
        row.operator("object.create_empty_on_selected", text='Init Target')
        row.operator("object.create_camera_to_target", text='Spawn Camera')
        row = box.row()
        row.operator("object.clear_addon_objects", text='Clear Addon Objects')

        
        box = layout.box()
        box.label(text="Adjustments")
        
        row = box.row(align=True)


        row.label(text="Pivot Angle")
        row.prop(addon_prop, 'other_cam_pivot_angle', text='')
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("object.pivot_camera_clockwise", text='+')
        row.operator("object.pivot_camera_counter_clockwise", text='-')
        col.operator("object.pivot_camera_reset", text='Reset')

        box = layout.box()
        box.label(text="Render util")
        row = box.row()
        row.prop(addon_prop, 'addn_export_folder')
        row = box.row()
        row.operator("render.render_bullet_action_on_target_or_selected", text='Begin Render')




class BULLETACTION_PT_panel_layout(Panel, BULLETACTION_layout):
    bl_idname = 'VIEW3D_PT_panel_layout'
    bl_category = 'BulletAction'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'


classes = (
    BULLETACTION_PT_panel_layout,
)
