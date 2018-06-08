# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_vertical
#
# Version history:
#   1.0 (2018.02.01) - release
#   1.1 (2018.06.08) - improve - added Y and X axis

bl_info = {
    'name': 'vertical',
    'category': 'Mesh',
    'author': 'Nikita Akimov',
    'version': (1, 1, 0),
    'blender': (2, 79, 0)
}

import bpy
import math


class Vertical(bpy.types.Operator):
    bl_idname = 'vertical.select'
    bl_label = 'Vertical: Select'
    bl_options = {'REGISTER', 'UNDO'}

    algorithm = bpy.props.IntProperty(name='algorithm', default=1)

    def execute(self, context):
        # print(context.window_manager.interface_vars.axis)
        # return
        if context.active_object:
            if context.active_object.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.object.mode_set(mode='OBJECT')
            activeobjectdata = bpy.context.active_object.data
            for polygon in activeobjectdata.polygons:
                mlx = mly = mlz = None
                if self.algorithm == 0:
                    # сравнение максимальных длин проекций ребер на оси
                    for edge in polygon.edge_keys:
                        lx = math.fabs(activeobjectdata.vertices[edge[0]].co[0] - activeobjectdata.vertices[edge[1]].co[0])
                        mlx = lx if not mlx or lx > mlx else mlx
                        ly = math.fabs(activeobjectdata.vertices[edge[0]].co[1] - activeobjectdata.vertices[edge[1]].co[1])
                        mly = ly if not mly or ly > mly else mly
                        lz = math.fabs(activeobjectdata.vertices[edge[0]].co[2] - activeobjectdata.vertices[edge[1]].co[2])
                        mlz = lz if not mlz or lz > mlz else mlz
                elif self.algorithm == 1:
                    # сравнение максимальной проекции полигона на ось Z с максимальными проекциями ребер на оси
                    z_max = z_min = None
                    for vertex_id in polygon.vertices:
                        z_min = activeobjectdata.vertices[vertex_id].co[2] if not z_min or z_min > activeobjectdata.vertices[vertex_id].co[2] else z_min
                        z_max = activeobjectdata.vertices[vertex_id].co[2] if not z_max or z_max < activeobjectdata.vertices[vertex_id].co[2] else z_max
                    mlz = math.fabs(z_max - z_min)
                    for edge in polygon.edge_keys:
                        lx = math.fabs(activeobjectdata.vertices[edge[0]].co[0] - activeobjectdata.vertices[edge[1]].co[0])
                        mlx = lx if not mlx or lx > mlx else mlx
                        ly = math.fabs(activeobjectdata.vertices[edge[0]].co[1] - activeobjectdata.vertices[edge[1]].co[1])
                        mly = ly if not mly or ly > mly else mly
                # check vertical
                if context.window_manager.interface_vars.axis == 'Z' and mlz >= mlx and mlz >= mly:
                    polygon.select = True
                elif context.window_manager.interface_vars.axis == 'X' and mlx >= mlz and mlx >= mly:
                    polygon.select = True
                elif context.window_manager.interface_vars.axis == 'Y' and mly >= mlx and mly >= mlz:
                    polygon.select = True
            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

    # раскомментировать 3 след. строчки если нужна блокировка в объектном режиме
    # @classmethod
    # def poll(cls, context):
    #     return context.active_object.mode == 'EDIT'


class InterfaceVars(bpy.types.PropertyGroup):
    axis = bpy.props.EnumProperty(
        items=[
            ('X', 'X', 'X', '', 0),
            ('Y', 'Y', 'Y', '', 1),
            ('Z', 'Z', 'Z', '', 2),
        ],
        default='Z'
    )


class VerticalPanel(bpy.types.Panel):
    bl_idname = 'vertical.panel'
    bl_label = 'Vertical'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        button = self.layout.operator('vertical.select', text='Vertical 0')
        button.algorithm = 0
        button = self.layout.operator('vertical.select', text='Vertical 1')
        button.algorithm = 1
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'axis', expand=True)


def register():
    bpy.utils.register_class(Vertical)
    bpy.utils.register_class(VerticalPanel)
    bpy.utils.register_class(InterfaceVars)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)


def unregister():
    del bpy.types.WindowManager.interface_vars
    bpy.utils.unregister_class(InterfaceVars)
    bpy.utils.unregister_class(VerticalPanel)
    bpy.utils.unregister_class(Vertical)


if __name__ == '__main__':
    register()
