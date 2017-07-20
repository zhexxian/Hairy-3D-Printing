import bpy

object = bpy.context.object
object_radius = 0.5 * max(object.bound_box.data.dimensions.x, object.bound_box.data.dimensions.y)

bpy.ops.object.particle_system_add()
bpy.data.particles["ParticleSettings"].type = 'HAIR'
bpy.data.particles["ParticleSettings"].count = 3000
bpy.data.particles["ParticleSettings"].hair_length = object_radius
bpy.ops.object.modifier_convert(modifier="ParticleSystem 1")
bpy.ops.object.convert(target='CURVE')
bpy.context.object.data.fill_mode = 'FULL'
bpy.context.object.data.bevel_depth = 0.05
bpy.ops.object.convert(target='MESH')
