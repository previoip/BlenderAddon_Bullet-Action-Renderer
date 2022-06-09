from bpy.props import BoolProperty, IntProperty, FloatProperty, CollectionProperty, StringProperty
from bpy.types import PropertyGroup


class BulletActionScenePropertyGroup(PropertyGroup):
    addn_export_folder: StringProperty(
        name="subfolder export", 
        default="export"
        )
    addn_render_type: BoolProperty(
        name="Render as Bulletaction"
        )
    cam_incl: FloatProperty(
        name="Inclination", 
        default=57.3, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_incr: IntProperty(
        name="Increment", 
        default=8, 
        min=1, 
        max=36
        )
    cam_rot_offset: FloatProperty(
        name="Offset Angle", 
        default=0, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_dist_offset: FloatProperty(
        name="Offset Distance", 
        min=0,
        default=1, 
        max=1000
        )
    other_cam_pivot_angle: FloatProperty(
        name="Pivot Angle", 
        default=45, 
        min=-180, 
        max=180, 
        precision=2,
        subtype='ANGLE'
        )

classes = (
    BulletActionScenePropertyGroup, 
)