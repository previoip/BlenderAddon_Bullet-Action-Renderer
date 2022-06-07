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

        box_1 = layout.box()
        box_2 = layout.box()

        box_1.label(text="Initialize Addon")
        row_1 = box_1.row()
        row_1.operator("object.create_empty_on_selected", text='Init Target')
        row_1.operator("object.create_camera_to_target", text='Preview Camera')

        box_2.label(text="Render")
        row_2 = box_2.row()
        row_2.operator("render.render_bullet_action_on_target_or_selected", text='Begin Render')




class BULLETACTION_PT_panel_layout(Panel, BULLETACTION_layout):
    bl_idname = 'VIEW3D_PT_panel_layout'
    bl_category = 'BulletAction'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'


classes = (
    BULLETACTION_PT_panel_layout,
)
