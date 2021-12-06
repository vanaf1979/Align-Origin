# ----------------------------------------------------------------------
# Align Origin
# ----------------------------------------------------------------------
# Package             Align Origin
# Version             0.1.0
# Description         Align origin to top, center or bottom of mesh
# Author              Stephan Nijman <vanaf1979@gmail.com>
# Author URI          https://since1979.dev
# Copyright           2021 Stephan Nijman
# Plugin repo         https://github.com/vanaf1979/align-origin
# Requires at least   3.0.0
# License:            GPL v2 or later
# License URI         http://www.gnu.org/licenses/gpl-2.0.txt
# ----------------------------------------------------------------------


import bpy
import mathutils


# ----------------------------------------------------------------------
# REGISTER THIS ADDON
# ----------------------------------------------------------------------
bl_info = {
    "name" : "ALIGN ORIGIN",
    "author" : "Stephan Nijman",
    "description" : "Align origin to top, center or bottom of mesh.",
    "blender" : (3, 0, 0),
    "version" : (0, 1, 0),
    "location" : "3DView",
    "warning" : "",
    "category" : "Object"
}



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

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        old_curs_loc = mathutils.Vector(bpy.context.scene.cursor.location)

        if self.location == 'bottom':
            new_z = active.location.z - (active.dimensions.z / 2)
        elif self.location == 'top':
            new_z = active.location.z + (active.dimensions.z / 2)
        else:
            new_z = active.location.z

        context.scene.cursor.location = mathutils.Vector((active.location.x,active.location.y,new_z))

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
    


# ----------------------------------------------------------------------
# REGISTER SUBMENU
# ----------------------------------------------------------------------
def register():
    bpy.utils.register_class(ST_OT_Origin_To_Base)
    bpy.utils.register_class(ST_MT_Align_Origin)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.prepend(align_origin_object_context_menu)

def unregister():
    bpy.utils.unregister_class(ST_OT_Origin_To_Base)
    bpy.utils.unregister_class(ST_MT_Align_Origin)
    bpy.types.VIEW3D_MT_object_context_menu.remove(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.remove(align_origin_object_context_menu)
    
    
if __name__ == "__main__":
    register()