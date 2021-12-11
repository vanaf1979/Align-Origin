import bpy

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
    bpy.types.VIEW3D_MT_object_context_menu.prepend(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.prepend(align_origin_object_context_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(align_origin_object_context_menu)
    bpy.types.VIEW3D_MT_object.remove(align_origin_object_context_menu)