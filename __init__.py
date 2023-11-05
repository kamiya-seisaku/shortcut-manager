# todo: troubleshoot key capture unstability, if not easy use captor 
# -Issues
#   -panel should be in 3dview/toolshelf
#   -key stroke capture work only one in 2-3 key presses
#   -need icon
bl_info = {
"name": "Blender Shortcut Organizer",
"author": "kkay",
"version": (1, 0),
"blender": (3, 6, 0),
"location": "View3D > Tool Shelf > Shortcut Organizer",
"description": "Simplifies the management of shortcuts in Blender",
"warning": "",
"doc_url": "",
"category": "3D View",
}

import bpy

#1 Popup Window Operator
class ShortcutOrganizerPopupOperator(bpy.types.Operator):
bl_idname = "object.shortcut_organizer_popup"
bl_label = "Shortcut Organizer Popup"
key_stroke = bpy.props.StringProperty()

@classmethod
def poll(cls, context):
# Always active
return True

def modal(self, context, event):
if event.type == 'ESC':  # Cancel
    return {'CANCELLED'}
elif event.type == 'RET':  # Confirm
    return {'FINISHED'}

# if event.value == 'PRESS':
#     if self.key_stroke == "Press key to assign.  Type F11 to finish.":
#         self.key_stroke = ""
#     self.key_stroke += event.type
#     print("User pressed:", event.type)
# else:  # Capture any other key
#     pass
#     # self.report({'INFO'}, "Captured key: " + str(event.type))
#     # return {'RUNNING_MODAL'}
return {'PASS_THROUGH'}

def invoke(self, context, event):
context.window_manager.modal_handler_add(self)  # Add this line to initiate the modal operation
self.key_stroke = "Press key to assign.  Type F11 to finish."
return context.window_manager.invoke_props_dialog(self)

def draw(self, context):
self.layout.label(text=f"key: {self.key_stroke}")  # Display proposed keys
# layout.operator("object.reload_addon", text="Reload Addon")
self.layout.operator("object.assign_key", text="Assign")  # Add Assign button

def execute(self, context):
self.report({'INFO'}, "Popup Opened")
return {'FINISHED'}

#2 Assign Key Operator
class AssignKeyOperator(bpy.types.Operator):
bl_idname = "object.assign_key"
bl_label = "Assign Key"

def execute(self, context):
# Your code to assign the key stroke
return {'FINISHED'}

# Not used to be deleted #3 Main Class for the Addon
# class ShortcutOrganizer(bpy.types.Operator):
#     # bl_idname = "object.shortcut_organizer"
#     # bl_label = "Shortcut Organizer"
#     bl_idname = "object.shortcut_organizer"
#     bl_label = "Shortcut Organizer"

#     def draw(self, context):
#         layout = self.layout
#         pass

#     # Todo: Functionality implementations

#4 Panel class for the Property Window
class OBJECT_PT_ShortcutOrganizerPropertyPanel(bpy.types.Panel):
bl_idname = "OBJECT_PT_ShortcutOrganizerPropertyPanel"
bl_label = "Shortcut Organizer"
bl_space_type = 'PROPERTIES'
bl_region_type = 'WINDOW'
bl_context = "object"

def draw(self, context):
layout = self.layout
layout.label(text="Press key to assign")
layout.operator("object.reload_addon", text="Reload Addon")
layout.operator("object.assign_key", text="Assign")  # Add Assign button

#5 Context menu to add Popup
def add_context_menu(self, context):
self.layout.operator('object.shortcut_organizer_popup')

#6 Reload Addon Operator
class ReloadAddonOperator(bpy.types.Operator):
bl_idname = "object.reload_addon"
bl_label = "Reload Addon"

def execute(self, context):
bpy.ops.preferences.addon_disable(module="blender-shortcut-organizer")
bpy.ops.preferences.addon_enable(module="blender-shortcut-organizer")
return {'FINISHED'}

# Registration/Unregistration

# all classes to be regietered/unregisterd in this file
classes = [OBJECT_PT_ShortcutOrganizerPropertyPanel, ReloadAddonOperator, AssignKeyOperator, ShortcutOrganizerPopupOperator]

# all bpy.types which end with '_context_menu'
context_menu_types = [menu for menu in dir(bpy.types) if menu.endswith('_context_menu')]

def register():
bpy.types.Scene.debug_mode = bpy.props.BoolProperty(name="Debug Mode")

# register all classes in this file
for cls in classes:
bpy.utils.register_class(cls)

# for all bpy.types which end with '_context_menu'
# add context menu for this addon
for menu_type in context_menu_types:
getattr(bpy.types, menu_type, None).append(add_context_menu) if getattr(bpy.types, menu_type, None) is not None else None

def unregister():
# unregister all classes in this file
for cls in reversed(classes):
bpy.utils.unregister_class(cls)
for menu_type in context_menu_types:
getattr(bpy.types, menu_type, None).remove(add_context_menu) if getattr(bpy.types, menu_type, None) is not None else None

if __name__ == "__main__":
register()
