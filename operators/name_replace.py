import bpy

from .renaming_operators import getAllVertexGroups, getAllAttributes, getAllBones, getAllModifiers, getAllUvMaps, \
    getAllColorAttributes, getAllParticleNames, getAllParticleSettingsNames, getAllDataNames, getAllShapeKeys
from .renaming_operators import switch_to_edit_mode, numerate_entity_name
from ..operators.renaming_utilities import get_renaming_list, call_renaming_popup, call_error_popup
from ..variable_replacer.variable_replacer import VariableReplacer


class VIEW3D_OT_replace_name(bpy.types.Operator):
    bl_idname = "renaming.name_replace"
    bl_label = "Replace Names"
    bl_description = "replaces the names of the objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scene = context.scene

        replaceName = scene.renaming_new_name
        renaming_list, switch_edit_mode, errMsg = get_renaming_list(context)

        if errMsg is not None:
            error_msg = scene.renaming_error_messages
            error_msg.add_message(errMsg)
            call_error_popup(context)
            return {'CANCELLED'}

        old_mode = context.mode

        # settings for numerating the new name
        msg = scene.renaming_messages

        vertexGroupNameList = []
        particleSettingsList = []
        particleList = []
        uvmapsList = []
        dataList = []
        attributeList = []
        colorAttributeList = []
        shapeKeyNamesList = []
        modifierNamesList = []
        boneList = []

        if context.scene.renaming_object_types == 'VERTEXGROUPS':
            vertexGroupNameList = getAllVertexGroups()
        if scene.renaming_object_types == 'PARTICLESYSTEM':
            particleList = getAllParticleNames()
        if scene.renaming_object_types == 'PARTICLESETTINGS':
            particleSettingsList = getAllParticleSettingsNames()
        if context.scene.renaming_object_types == 'UVMAPS':
            uvmapsList = getAllUvMaps()
        if context.scene.renaming_object_types == 'COLORATTRIBUTES':
            colorAttributeList = getAllColorAttributes()
        if context.scene.renaming_object_types == 'ATTRIBUTES':
            attributeList = getAllAttributes()
        if scene.renaming_object_types == 'SHAPEKEYS':
            shapeKeyNamesList = getAllShapeKeys()
        if scene.renaming_object_types == 'MODIFIERS':
            modifierNamesList = getAllModifiers()
        if scene.renaming_object_types == 'BONE':
            boneList = getAllBones(old_mode)
        if scene.renaming_object_types == 'DATA':
            dataList = getAllDataNames()

        VariableReplacer.reset()

        if len(str(replaceName)) > 0:  # New name != empty
            if len(renaming_list) > 0:  # List of objects to rename != empty
                for entity in renaming_list:
                    if entity is not None:

                        replaceName = VariableReplacer.replaceInputString(context, scene.renaming_new_name, entity)

                        oldName = entity.name
                        new_name = ''

                        if not scene.renaming_use_enumerate:
                            entity.name = replaceName
                            msg.add_message(oldName, entity.name)

                        else:  # if scene.renaming_use_enumerate == True

                            if scene.renaming_object_types == 'OBJECT':
                                new_name = numerate_entity_name(context, replaceName, bpy.data.objects, entity.name)

                            elif scene.renaming_object_types == 'MATERIAL':
                                new_name = numerate_entity_name(context, replaceName, bpy.data.materials, entity.name)

                            elif scene.renaming_object_types == 'IMAGE':
                                new_name = numerate_entity_name(context, replaceName, bpy.data.images, entity.name)

                            elif scene.renaming_object_types == 'DATA':
                                new_name, dataList = numerate_entity_name(context, replaceName, dataList, entity.name,
                                                                          return_type_list=True)

                            elif scene.renaming_object_types == 'BONE':
                                new_name, boneList = numerate_entity_name(context, replaceName, boneList, entity.name,
                                                                          return_type_list=True)

                            elif scene.renaming_object_types == 'COLLECTION':
                                new_name = numerate_entity_name(context, replaceName, bpy.data.collections, entity.name)

                            elif scene.renaming_object_types == 'ACTIONS':
                                new_name = numerate_entity_name(context, replaceName, bpy.data.actions, entity.name)

                            elif scene.renaming_object_types == 'SHAPEKEYS':
                                new_name, shapeKeyNamesList = numerate_entity_name(context, replaceName,
                                                                                   shapeKeyNamesList, entity.name,
                                                                                   return_type_list=True)
                            elif scene.renaming_object_types == 'MODIFIERS':
                                new_name, modifierNamesList = numerate_entity_name(context, replaceName,
                                                                                   modifierNamesList, entity.name,
                                                                                   return_type_list=True)
                            elif context.scene.renaming_object_types == 'VERTEXGROUPS':
                                new_name, vertexGroupNameList = numerate_entity_name(context, replaceName,
                                                                                     vertexGroupNameList, entity.name,
                                                                                     return_type_list=True)

                            elif context.scene.renaming_object_types == 'PARTICLESYSTEM':
                                new_name, particleList = numerate_entity_name(context, replaceName,
                                                                              particleList, entity.name,
                                                                              return_type_list=True)

                            elif context.scene.renaming_object_types == 'PARTICLESETTINGS':
                                new_name, particleSettingsList = numerate_entity_name(context, replaceName,
                                                                                      particleSettingsList, entity.name,
                                                                                      return_type_list=True)



                            elif context.scene.renaming_object_types == 'UVMAPS':
                                new_name, uvmapsList = numerate_entity_name(context, replaceName,
                                                                            uvmapsList, entity.name,
                                                                            return_type_list=True)

                            elif context.scene.renaming_object_types == 'ATTRIBUTES':
                                new_name, attributeList = numerate_entity_name(context, replaceName,
                                                                               attributeList, entity.name,
                                                                               return_type_list=True)
                            elif context.scene.renaming_object_types == 'COLORATTRIBUTES':
                                new_name, colorAttributeList = numerate_entity_name(context, replaceName,
                                                                                    colorAttributeList, entity.name,
                                                                                    return_type_list=True)

                            try:
                                entity.name = new_name
                                msg.add_message(oldName, entity.name)
                            except AttributeError:
                                print("Attribute {} is read only".format(new_name))


        else:  # len(str(replaceName)) <= 0
            msg.add_message(None, None, "Insert a valid string to replace names")

        call_renaming_popup(context)
        if switch_edit_mode:
            switch_to_edit_mode(context)
        return {'FINISHED'}
