# todo: troubleshoot key capture unstability, if not easy use captor 
# -Issues
#   -panel should be in 3dview/toolshelf
#   -key stroke capture work only one in 2-3 key presses
#   -need icon

#3 Panel class for the Property Window
class OBJECT_PT_ShortcutOrganizerPropertyPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ShortcutOrganizerPropertyPanel"
    bl_label = "Shortcut Organizer"
-   bl_space_type = 'VIEW_3D'
-   bl_region_type = 'UI'
+   bl_space_type = 'PROPERTIES'
+   bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Press key to assign")
        layout.operator("object.shortcut_organizer_popup", text="Open Shortcut Popup")
        layout.operator("object.assign_key", text="Assign")  # Add Assign button
