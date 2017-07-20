import bpy
from mathutils import Vector
'''
import bpy
import bmesh
from bmesh.types import BMFace

obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

for geom in bm.select_history:
    if isinstance(geom, BMFace):
        print(geom.index)
        bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value":(0, 0, 30)}
)

bmesh.update_edit_mesh(me, True)

'''

# Get parameters of object
object = bpy.context.object
object_location = object.location
object_radius = 0.5 * max(object.bound_box.data.dimensions.x, object.bound_box.data.dimensions.y)
object_height = object.bound_box.data.dimensions.z

# Parameters
cylinder_radius = object_radius * 2 #50
cylinder_thickness = 0.05
cylinder_height = object_height #100
cyliner_position = object_location #(0, 0, 0)

'''
# Create a cone
#bpy.ops.mesh.primitive_cone_add(radius1=cylinder_radius-5, radius2=0, depth=cylinder_height)
#cone = bpy.context.object
#cone.name = 'cone'
#cone.location = cyliner_position
'''

# Create an outer cylinder.
bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
cylinder_outer = bpy.context.object
cylinder_outer.name = 'cylinder_outer'
cylinder_outer.location = cyliner_position
 
# Create an inner cylinder.
bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius,depth=cylinder_height+20)
cylinder_inner = bpy.context.object
cylinder_inner.name = 'cylinder_inner'
cylinder_inner.location = cyliner_position
 
# Create a boolean modifier named 'my_bool_mod' for the cube.
mod_bool = cylinder_outer.modifiers.new('my_bool_mod', 'BOOLEAN')
# Set the mode of the modifier to DIFFERENCE.
mod_bool.operation = 'DIFFERENCE'
# Set the object to be used by the modifier.
mod_bool.object = cylinder_inner  
 
# The modifier_apply function only works on the active object.
bpy.context.scene.objects.active = cylinder_outer
 
# Apply the modifier.
res = bpy.ops.object.modifier_apply(modifier = 'my_bool_mod')
 
# Delete the cylinder.
cylinder_inner.select = True
bpy.ops.object.delete()
