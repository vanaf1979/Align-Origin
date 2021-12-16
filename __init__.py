import bpy
import mathutils


bl_info = {
    "name" : "Align Origin",
    "author" : "Stephan Nijman",
    "description" : "A collection of blender utilities",
    "blender" : (3, 0, 0),
    "version" : (0, 2, 1),
    "location" : "3DView",
    "warning" : "",
    "category" : "Generic"
}


# ----------------------------------------------------------------------
# ALIGN ORIGIN TO TOP, CENTER OR BOTTOM OF MESH
# ----------------------------------------------------------------------
class ST_OT_Origin_To_Base(bpy.types.Operator):
    """Align origin to mesh"""
    bl_label = "Align Origin to mesh"
    bl_idname = 'object.align_origin_to_mesh'
    bl_options = {'REGISTER','UNDO'}

    location: bpy.props.StringProperty(
        default = 'bottom',
        options={'HIDDEN'}
    )

    offset: bpy.props.FloatVectorProperty(
        default=[0.0,0.0,0.0],
        name='offset: ',
        subtype='XYZ'
    )
    
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
            
        newX = active.location.x + self.offset[0]
        newY = active.location.y + self.offset[1]
        newZ = new_z + self.offset[2]

        context.scene.cursor.location = mathutils.Vector((newX,newY,newZ))

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        context.scene.cursor.location = old_curs_loc

        return {'FINISHED'}


# ----------------------------------------------------------------------
# CREATE THE 3DVIEW OBJECT CONTEXT SUBMENU
# ----------------------------------------------------------------------
class ST_MT_Align_Origin(bpy.types.Menu):
    bl_label = "Align Origin"
    bl_idname = "OBJECT_MT_align_origin"

    def draw(self, context):
        curs_bt = self.layout.operator('object.align_origin_to_mesh', text='Origin to top')
        curs_bt.location = 'top'
        curs_bt = self.layout.operator('object.align_origin_to_mesh', text='Origin to center')
        curs_bt.location = 'center'
        curs_bt = self.layout.operator('object.align_origin_to_mesh', text='Origin to bottom')
        curs_bt.location = 'bottom'


# ----------------------------------------------------------------------
# ADD SUBMENU TO 3DVIEW OBJECT CONTEXT MENU
# ----------------------------------------------------------------------
def align_origin_object_context_menu(self, context):
    
    if context.object is not None and context.object.type in {'MESH', 'CURVE'}:
        self.layout.separator()
        self.layout.menu(ST_MT_Align_Origin.bl_idname)


class AlignOriginsPreferences(bpy.types.AddonPreferences):
    """Align origins addon preferences"""
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label("Align origin preference text")
        
        
        
class AlignOriginsPreferences(bpy.types.AddonPreferences):
    
    def draw(self, context):
        layout = self.layout
        layout.label("Align origin preference text")


# ----------------------------------------------------------------------
# REGISTER SUBMENU
# ----------------------------------------------------------------------
def register():
    bpy.utils.register_class(ST_OT_Origin_To_Base)
    bpy.utils.register_class(ST_MT_Align_Origin)
    bpy.utils.register_class(AlignOriginsPreferences)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.prepend(align_origin_object_context_menu)

def unregister():
    bpy.utils.unregister_class(ST_OT_Origin_To_Base)
    bpy.utils.unregister_class(ST_MT_Align_Origin)
    bpy.utils.unregister_class(AlignOriginsPreferences)
    bpy.types.VIEW3D_MT_object_context_menu.remove(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.remove(align_origin_object_context_menu)
    

if __name__ == "__main__":
    register()