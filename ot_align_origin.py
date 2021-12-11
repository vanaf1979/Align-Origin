import bpy

# ----------------------------------------------------------------------
# ALIGN ORIGIN TO TOP, CENTER OR BOTTOM OF MESH
# ----------------------------------------------------------------------
class ST_OT_Origin_To_Base(bpy.types.Operator):
    """Align origin to mesh"""
    bl_label = "Align Origin to mesh"
    bl_idname = 'object.align_origin_to_mesh'

    location: bpy.props.StringProperty(default = 'bottom')
    
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type in {'MESH', 'CURVE'}
    
    
    def execute(self, context):

        active = context.object

        if context.object is None or context.object.type not in {'MESH', 'CURVE'}:
            self.report({'ERROR'}, "No object selected")
            return {'FINISHED'}

        old_curs_loc = mathutils.Vector(bpy.context.scene.cursor.location)

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        
        matrix_world = active.matrix_world
        vertex_coordinates = [ matrix_world @ v.co for v in active.data.vertices ]
        
        if self.location == 'bottom':
            new_z = min( [ co.z for co in vertex_coordinates ] ) 
            
        elif self.location == 'top':
            new_z = max( [ co.z for co in vertex_coordinates ] ) 
            
        else:
            min_z = min( [ co.z for co in vertex_coordinates ] ) 
            max_z = max( [ co.z for co in vertex_coordinates ] )
            new_z = max_z + (min_z-max_z) / 2
            

        context.scene.cursor.location = mathutils.Vector((active.location.x,active.location.y,new_z))

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        context.scene.cursor.location = old_curs_loc

        return {'FINISHED'}