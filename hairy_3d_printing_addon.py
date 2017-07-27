bl_info = {
    "name": "Hairy 3D Print",
    "description": "Hairify stl file that can be printed by FDM 3D printers.",
    "author": "Shun Yu, Nigel, Zhexian",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > UI panel > Add hair",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "", #"http://wiki.blender.org/index.php/Extensions:2.6/Py/"
                #"Scripts/My_Script",
    "tracker_url": "",#"https://developer.blender.org/maniphest/task/edit/form/2/",
    "support": "COMMUNITY",
    "category": "Add Mesh"
    }

import bpy
from mathutils import Vector

class AutomaticMode(bpy.types.Operator):
    bl_idname = "object.hairfy_auto"
    bl_label = "Hairy 3D Print (Automatic Mode)"
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.

        # Get parameters of object
        object = bpy.context.object
        object_location = object.location
        object_radius = 0.5 * max(object.bound_box.data.dimensions.x, object.bound_box.data.dimensions.y)
        object_height = object.bound_box.data.dimensions.z

        # Parameters
        cylinder_radius = object_radius + 1 #50
        cylinder_thickness = 0.2
        cylinder_height = object_height #100
        cylinder_position = object_location #(0, 0, 0)


        # Create an outer cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
        cylinder_outer = bpy.context.object
        cylinder_outer.name = 'cylinder_outer'
        cylinder_outer.location = cylinder_position
         
        # Create an inner cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius,depth=cylinder_height+20)
        cylinder_inner = bpy.context.object
        cylinder_inner.name = 'cylinder_inner'
        cylinder_inner.location = cylinder_position
         
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


        bpy.ops.object.particle_system_add()
        bpy.data.particles["ParticleSettings"].type = 'HAIR'
        bpy.data.particles["ParticleSettings"].count = 3000
        bpy.data.particles["ParticleSettings"].hair_length = object_radius
        bpy.ops.object.modifier_convert(modifier="ParticleSystem 1")
        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_depth = 0.05
        bpy.ops.object.convert(target='MESH')

        ### Generate a bigger cylinder to clean the outer hairs ###
        # Create a cylinder_cleaning.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
        cylinder_cleaning = bpy.context.object
        cylinder_cleaning.name = 'cylinder_cleaning'
        cylinder_cleaning.location = cylinder_position

        # Create outer cleaning_cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+object_radius+50,depth=cylinder_height+object_radius+50)
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
        mod_bool = bpy.data.objects['Mesh'].modifiers.new('my_bool_cleaning_hair', 'BOOLEAN')
        # Set the mode of the modifier to DIFFERENCE.
        mod_bool.operation = 'DIFFERENCE'
        # Set the object to be used by the modifier.
        mod_bool.object = cylinder_outer_outer
        # The modifier_apply function only works on the active object.
        bpy.context.scene.objects.active = bpy.data.objects['Mesh']
        # Apply the modifier.
        res = bpy.ops.object.modifier_apply(modifier = 'my_bool_cleaning_hair')

        # Delete the cylinders.
        cylinder_cleaning.select = True
        bpy.ops.object.delete()
        cylinder_outer_outer.select = True
        bpy.ops.object.delete()

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

class ManualMode(bpy.types.Operator):
    bl_idname = "object.hairfy_manual"
    bl_label = "Hairy 3D Print (Manual Mode)"
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        bpy.ops.object.modifier_convert(modifier="ParticleSystem 1")
        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_depth = 0.3
        bpy.ops.object.convert(target='MESH')
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

class ManualMode_Support(bpy.types.Operator):
    bl_idname = "object.hairfy_manual_support"
    bl_label = "Hairy 3D Print (Manual Mode): add support cylinder"
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        # Get parameters of object
        object = bpy.context.object
        object_location = object.location
        object_radius = 0.5 * max(object.bound_box.data.dimensions.x, object.bound_box.data.dimensions.y)
        object_height = object.bound_box.data.dimensions.z

        # Parameters
        cylinder_radius = object_radius + 1 #50
        cylinder_thickness = 0.5
        cylinder_height = object_height #100
        cylinder_position = 0, 0, 30


        # Create an outer cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
        cylinder_outer = bpy.context.object
        cylinder_outer.name = 'cylinder_outer'
        cylinder_outer.location = cylinder_position
             
        # Create an inner cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius,depth=cylinder_height+20)
        cylinder_inner = bpy.context.object
        cylinder_inner.name = 'cylinder_inner'
        cylinder_inner.location = cylinder_position
             
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

        ### Generate a bigger cylinder to clean the outer hairs ###
        # Create a cylinder_cleaning.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+cylinder_thickness,depth=cylinder_height)
        cylinder_cleaning = bpy.context.object
        cylinder_cleaning.name = 'cylinder_cleaning'
        cylinder_cleaning.location = cylinder_position

        # Create outer cleaning_cylinder.
        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius+object_radius+50,depth=cylinder_height+object_radius+50)
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
        mod_bool = bpy.data.objects['Mesh'].modifiers.new('my_bool_cleaning_hair', 'BOOLEAN')
        # Set the mode of the modifier to DIFFERENCE.
        mod_bool.operation = 'DIFFERENCE'
        # Set the object to be used by the modifier.
        mod_bool.object = cylinder_outer_outer
        # The modifier_apply function only works on the active object.
        bpy.context.scene.objects.active = bpy.data.objects['Mesh']
        # Apply the modifier.
        res = bpy.ops.object.modifier_apply(modifier = 'my_bool_cleaning_hair')

        # Delete the cylinders.
        cylinder_cleaning.select = True
        bpy.ops.object.delete()
        cylinder_outer_outer.select = True
        bpy.ops.object.delete()

        return {'FINISHED'}            # this lets blender know the operator finished successfully.
 
    

def menu_func(self, context):
    self.layout.operator(AutomaticMode.bl_idname)
    self.layout.operator(ManualMode.bl_idname)
    self.layout.operator(ManualMode_Support.bl_idname)

def register():
    # bpy.utils.register_class(AutomaticMode)
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    # bpy.utils.unregister_class(AutomaticMode)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

