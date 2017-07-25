### Generate a bigger cylinder to clean the outer hairs ###
# Create a cylinder_cleaning.
bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
cylinder_cleaning = bpy.context.object
cylinder_cleaning.name = 'cylinder_cleaning'
cylinder_cleaning.location = cylinder_position

# Create outer cleaning_cylinder.
bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+object_radius+10,depth=cylinder_height+object_radius+10)
cylinder_outer_outer = bpy.context.object
cylinder_outer_outer.name = 'cylinder_outer_outer'
cylinder_outer_outer.location = cylinder_position
# Create a boolean modifier
mod_bool = cylinder_outer_outer.modifiers.new('my_bool_cleaning', 'BOOLEAN')
# Set the mode of the modifier to DIFFERENCE.
mod_bool.operation = 'DIFFERENCE'
# Set the object to be used by the modifier.
mod_bool.object = cylinder_cleaning  
# The modifier_apply function only works on the active object.
bpy.context.scene.objects.active = cylinder_outer_outer
# Apply the modifier.
res = bpy.ops.object.modifier_apply(modifier = 'my_bool_cleaning')


### Clean the hair ###
# Assume that the hair is named 'hair'
# Create a boolean modifier
mod_bool = bpy.data.objects['hair'].modifiers.new('my_bool_cleaning_hair', 'BOOLEAN')
# Set the mode of the modifier to DIFFERENCE.
mod_bool.operation = 'DIFFERENCE'
# Set the object to be used by the modifier.
mod_bool.object = cylinder_outer_outer
# The modifier_apply function only works on the active object.
bpy.context.scene.objects.active = bpy.data.objects['hair']
# Apply the modifier.
res = bpy.ops.object.modifier_apply(modifier = 'my_bool_cleaning_hair')

# Delete the cylinders.
cylinder_cleaning.select = True
bpy.ops.object.delete()
cylinder_outer_outer.select = True
bpy.ops.object.delete()
#########################################################
