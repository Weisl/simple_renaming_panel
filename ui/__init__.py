import bpy

from .info_messages import RENAMING_MESSAGES, WarningError_MESSAGES, INFO_MESSAGES
from .renaming_panels import VIEW3D_PT_tools_renaming_panel, VIEW3D_PT_tools_type_suffix, VIEW3D_OT_SetVariable, \
    VIEW3D_OT_RenamingPopupOperator, OBJECT_MT_suffix_prefix_presets, AddPresetRenamingPresets
from .renaming_panels import panel_func
from .renaming_popup import VIEW3D_PT_renaming_popup, VIEW3D_PT_info_popup, VIEW3D_PT_error_popup
from .renaming_variables import RENAMING_MT_variableMenu, VIEW3D_OT_inputVariables
from .ui_helpers import PREFERENCES_OT_open_addon

classes = (
    RENAMING_MT_variableMenu,
    VIEW3D_OT_inputVariables,
    VIEW3D_PT_error_popup,
    VIEW3D_PT_info_popup,
    VIEW3D_PT_renaming_popup,
    OBJECT_MT_suffix_prefix_presets,
    AddPresetRenamingPresets,
    VIEW3D_PT_tools_renaming_panel,
    VIEW3D_PT_tools_type_suffix,
    VIEW3D_OT_SetVariable,
    VIEW3D_OT_RenamingPopupOperator,
    PREFERENCES_OT_open_addon,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_PT_tools_type_suffix.prepend(panel_func)

    id_store = bpy.types.Scene

    id_store.renaming_messages = RENAMING_MESSAGES()
    id_store.renaming_error_messages = WarningError_MESSAGES()
    id_store.renaming_info_messages = INFO_MESSAGES()


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    id_store = bpy.types.Scene
    del id_store.renaming_messages
    del id_store.renaming_error_messages
    del id_store.renaming_info_messages
