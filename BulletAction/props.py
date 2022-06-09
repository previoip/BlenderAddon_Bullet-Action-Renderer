from bpy.props import BoolProperty, IntProperty, FloatProperty, CollectionProperty, StringProperty
from bpy.types import PropertyGroup


class BulletActionScenePropertyGroup(PropertyGroup):
    addn_export_folder: StringProperty(
        name='subfolder export', 
        description = 'Addon export subfolder',
        default='export'
        )
    addn_render_type: BoolProperty(
        name='Render as Bulletaction',
        description = 'Render BulletAction thing instead of incrimental 360 view (Increment will be disabled)',
        )

    addn_render_postproc: BoolProperty(
        name='Use Internal Mask Bitmap Post-proccessing',
        description = 'Use addons script for rendering mask-map',
        )

    cam_incl: FloatProperty(
        name='Inclination', 
        description = 'Camera inclination to the normal plane of target object.',
        default=57.3, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_incr: IntProperty(
        name='Increment', 
        description = 'Camera n of increment in one render cycle (rotates 360 degrees).',
        default=8, 
        min=1, 
        max=36
        )
    cam_rot_offset: FloatProperty(
        name='Offset Angle', 
        description = 'Camera angle offset to target reference',
        default=0, 
        min=-360, 
        max=360, 
        precision=2,
        subtype='ANGLE'
        )
    cam_dist_offset: FloatProperty(
        name='Offset Distance', 
        description = 'Camera distance offset to target reference',
        min=0,
        default=1, 
        max=1000
        )
    other_cam_pivot_angle: FloatProperty(
        name='Pivot Angle', 
        description = 'Adjust camera initial position',
        default=45, 
        min=-180, 
        max=180, 
        precision=2,
        subtype='ANGLE'
        )

classes = (
    BulletActionScenePropertyGroup, 
)