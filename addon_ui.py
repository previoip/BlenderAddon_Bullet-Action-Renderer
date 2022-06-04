import bpy

from bpy.types import Panel

class BulletActionUI(Panel):
    bl_idname = 'BULLETACTION_PT_panel_layout'
    bl_label = 'BulletAction'

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="My Select Panel")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Initialize Addon")

        row_1 = box.row()
        row_1.operator("")

classes = (
    BulletActionUI,
)
