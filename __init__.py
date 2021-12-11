bl_info = {
    "name" : "Align Origin",
    "author" : "Stephan Nijman",
    "description" : "Align origin to mesh",
    "blender" : (3, 0, 0),
    "version" : (0, 2, 1),
    "location" : "3DView",
    "warning" : "",
    "category" : "Generic"
}

#from . import addon_updater_ops
from . import auto_load

auto_load.init()

def register():
    auto_load.register()
    #addon_updater_ops.register(bl_info)

def unregister():
    auto_load.unregister()
