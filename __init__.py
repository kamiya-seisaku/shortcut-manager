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

# #1 Popup Window Operator
class ShortcutOrganizerPopupOperator(bpy.types.Operator):
    # bl_idname = "object.shortcut_organizer_popup"
    bl_idname = "wm.myop"
    bl_label = "Shortcut Organizer Dialog"
    
    key_stroke: bpy.props.StringProperty()

    text = bpy.props.StringProperty(name= "Enter Name", default= "")
    scale = bpy.props.FloatVectorProperty(name= "Scale:", default= (1,1,1))
    
    @classmethod
    def poll(cls, context):
        # Always active
        return True

    def modal(self, context, event):
        if event.type == 'ESC':  # Use ESC to exit key capture mode
            print("Key capture cancelled")
            self.report({'INFO'}, "Key capture cancelled")
            return {'CANCELLED'}

        if event.value == 'PRESS' and event.type not in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'TIMER', 'TIMER_REPORT', 'TIMER_REGION', 'NONE'}:
            # This will capture any key press except for mouse movement and timer events
            modifiers = []
            if event.shift:
                modifiers.append('Shift' if event.shift else '')
            if event.ctrl:
                modifiers.append('Ctrl' if event.ctrl else '')
            if event.alt:
                modifiers.append('Alt' if event.alt else '')
            if event.oskey:
                modifiers.append('Cmd' if event.oskey else '')

            # Filter out empty strings
            modifiers = [mod for mod in modifiers if mod]

            # Capture regular keys and ignore the modifier keys themselves
            if event.type not in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'LEFT_CTRL', 'RIGHT_CTRL', 'LEFT_ALT', 'RIGHT_ALT', 'OSKEY'}:
                # Join the modifiers with '+' and add the key itself
                self.key_stroke = ' + '.join(modifiers + [event.type])
                print("Key captured:", self.key_stroke)
                self.report({'INFO'}, f"Key captured: {self.key_stroke}")
                # Here you would handle the assignment of the captured key to the button's functionality
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # Initialize the key_stroke variable
        self.key_stroke = ""
        # Add this operator to the window manager to start capturing key events
        context.window_manager.modal_handler_add(self)
        # Tell Blender to open a dialog window for this operator
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # self.report({'INFO'}, "Popup Opened")
        return {'FINISHED'}

#2 Assign Key Operator
class AssignKeyOperator(bpy.types.Operator):
    bl_idname = "object.assign_key"
    bl_label = "Assign Key"

    def execute(self, context):
        # Your code to assign the key stroke
        return {'FINISHED'}

#3 Panel class (3D Tool shelf)
class ShortcutOrganizerPanel(bpy.types.Panel):
    # From Blender Python Tutorial : An Introduction to Scripting [how to learn python for beginners] https://www.youtube.com/watch?v=cyt0O7saU4Q&list=PLFtLHTf5bnym_wk4DcYIMq1DkjqB7kDb-
    bl_label = "Shortcut Organizer"
    bl_idname = "VIEW3D_PT_ShortcutOrganizer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ShortcutOrganizer"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Press key to assign")
        #todo layout.operator("object.shortcut_organizer_popup", text="Open Shortcut Popup")
        layout.operator("object.assign_key", text="Assign")  # Add Assign button

#4 Context menu to add Popup
def add_context_menu(self, context):
    self.layout.operator('wm.myop')

#5 Reload Addon Operator
class ReloadAddonOperator(bpy.types.Operator):
    bl_idname = "object.reload_addon"
    bl_label = "Reload Addon"

    def execute(self, context):
        bpy.ops.preferences.addon_disable(module="blender-shortcut-organizer")
        bpy.ops.preferences.addon_enable(module="blender-shortcut-organizer")
        return {'FINISHED'}

# Registration/Unregistration

# all classes to be regietered/unregisterd in this file
classes = [ShortcutOrganizerPanel, ReloadAddonOperator, AssignKeyOperator, ShortcutOrganizerPopupOperator]

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
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    for menu_type in context_menu_types:
        getattr(bpy.types, menu_type, None).remove(add_context_menu) if getattr(bpy.types, menu_type, None) is not None else None

if __name__ == "__main__":
    register()
