relative_path_to_mcell = "mcell"
#relative_path_to_mcell = "/../mcell_git/src/linux/mcell"

"""
# This section of code was used (from the command line) to copy this addon to the Blender addons area. Now the makefile performs that task.
install_to = "2.75"


# From within Blender: import cellblender.test_suite.cellblender_test_suite
if __name__ == "__main__":
  # Simple method to "install" a new version with "python test_suite/cellblender_test_suite.py" assuming "test_suite" directory exists in target location.
  import os
  print ( "MAIN with __file__ = " + __file__ )
  print ( " Installing into Blender " + install_to )
  os.system ( "cp ./" + __file__ + " ~/.config/blender/" + install_to + "/scripts/addons/" + __file__ )
  print ( "Copied files" )
  exit(0)
"""


bl_info = {
  "version": "0.1",
  "name": "CellBlender Test Suite",
  'author': 'Bob',
  "location": "Properties > Scene",
  "category": "Cell Modeling"
  }


##################
#  Support Code  #
##################

import sys
import os
import os.path
import hashlib
import bpy
import math
import random
import mathutils
from bpy.props import *

import cellblender

from bpy.app.handlers import persistent


active_frame_change_handler = None


test_groups = []
max_test_groups = 30   # Needed to define a BoolVectorProperty to show and hide each group (32 is max!?!?!)
next_test_group_num = 0    # The index number of the next group to be added


def register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num ):
    found = -1
    for gnum in range(len(test_groups)):
        g = test_groups[gnum]
        if g["group_name"] == group_name:
            found = gnum

    if found < 0:
        test_groups.append ( { "group_index":next_test_group_num, "group_name":group_name, "group_tests":[] } )
        found = len(test_groups) - 1
        next_test_group_num += 1
        if next_test_group_num >= max_test_groups:
            print ( "================================================================================================" )
            print ( "Too many test groups defined. Increase the number of 'show_group_#' entries and max_test_groups." )
            print ( "================================================================================================" )
            bpy.ops.wm.quit_blender()

    test_num = 1 + len(test_groups[found]["group_tests"])
    test_groups[found]["group_tests"].append ( { "test_name":str(test_num)+". "+test_name, "operator_name":operator_name } )
    
    return next_test_group_num
    

def run_method_changed(self, context):
    print ( "Run method changed" )
    """
    app = context.scene.cellblender_test_suite
    mcell = context.scene.mcell
    scripting_list = mcell.scripting.scripting_list
    if len(scripting_list) > 0:
        scripting = scripting_list[mcell.scripting.active_scripting_index]
    """
    return



class CellBlenderTestPropertyGroup(bpy.types.PropertyGroup):

    # Properties needed by the testing application itself

    show_setup = bpy.props.BoolProperty(name="ShowSetUp", default=True)
    path_to_mcell = bpy.props.StringProperty(name="Path to MCell", default="")
    path_to_blend = bpy.props.StringProperty(name="Path to Blend", default="")
    path_to_mdl = bpy.props.StringProperty(name="Path to MDL", default="")
    exit_on_error = bpy.props.BoolProperty(name="Exit on Error", default=True)
    run_mcell = bpy.props.BoolProperty(name="Run MCell", default=True)

    run_with_queue = bpy.props.BoolProperty(name="Run with Queue", default=True)
    submit_host = bpy.props.StringProperty(name="Submit Host", default="")

    run_method_enum = [
        ('NONE',         "None",    ""),
        ('SWEEP_QUEUE',  "MCell Local", ""),
        ('SWEEP_SGE',    "MCell SGE", ""),
        ('QUEUE',        "Queue",    ""),
        ('COMMAND',      "Command",  "")]
    run_method = bpy.props.EnumProperty(
        items=run_method_enum, name="Run Method",
        default='SWEEP_QUEUE',
        description="Choose a run method",
        update=run_method_changed)

    update_soure_file = bpy.props.BoolProperty(name="Update Source", default=False)
    source_file_to_update = bpy.props.StringProperty(name="Source File to Update", default="")
    stress_test_level = bpy.props.IntProperty(name="Stress Test Level", default=100)

    test_status = bpy.props.StringProperty(name="TestStatus", default="?")

    
    # Properties needed for the dynamically created test case groups

    show_group = BoolVectorProperty ( size=max_test_groups ) # Used for showing and hiding each panel - can only hold 32 elements!!!!!

    groups_real = bpy.props.BoolProperty(default=False)
    # Start with all defaulted to "True" so they can be changed to "False" making them real ID properties!!!
    show_group_0 = bpy.props.BoolProperty(default=True)
    show_group_1 = bpy.props.BoolProperty(default=True)
    show_group_2 = bpy.props.BoolProperty(default=True)
    show_group_3 = bpy.props.BoolProperty(default=True)
    show_group_4 = bpy.props.BoolProperty(default=True)
    show_group_5 = bpy.props.BoolProperty(default=True)
    show_group_6 = bpy.props.BoolProperty(default=True)
    show_group_7 = bpy.props.BoolProperty(default=True)
    show_group_8 = bpy.props.BoolProperty(default=True)
    show_group_9 = bpy.props.BoolProperty(default=True)
    show_group_10 = bpy.props.BoolProperty(default=True)
    show_group_11 = bpy.props.BoolProperty(default=True)
    show_group_12 = bpy.props.BoolProperty(default=True)
    show_group_13 = bpy.props.BoolProperty(default=True)
    show_group_14 = bpy.props.BoolProperty(default=True)
    show_group_15 = bpy.props.BoolProperty(default=True)
    show_group_16 = bpy.props.BoolProperty(default=True)
    show_group_17 = bpy.props.BoolProperty(default=True)
    show_group_18 = bpy.props.BoolProperty(default=True)
    show_group_19 = bpy.props.BoolProperty(default=True)
    show_group_20 = bpy.props.BoolProperty(default=True)
    show_group_21 = bpy.props.BoolProperty(default=True)
    show_group_22 = bpy.props.BoolProperty(default=True)
    show_group_23 = bpy.props.BoolProperty(default=True)
    show_group_24 = bpy.props.BoolProperty(default=True)
    show_group_25 = bpy.props.BoolProperty(default=True)
    show_group_26 = bpy.props.BoolProperty(default=True)
    show_group_27 = bpy.props.BoolProperty(default=True)
    show_group_28 = bpy.props.BoolProperty(default=True)
    show_group_29 = bpy.props.BoolProperty(default=True)
    show_group_30 = bpy.props.BoolProperty(default=True)

    def make_real ( self ):
      if not self.groups_real:
        self.show_group_0 = False
        self.show_group_1 = False
        self.show_group_2 = False
        self.show_group_3 = False
        self.show_group_4 = False
        self.show_group_5 = False
        self.show_group_6 = False
        self.show_group_7 = False
        self.show_group_8 = False
        self.show_group_9 = False
        self.show_group_10 = False
        self.show_group_11 = False
        self.show_group_12 = False
        self.show_group_13 = False
        self.show_group_14 = False
        self.show_group_15 = False
        self.show_group_16 = False
        self.show_group_17 = False
        self.show_group_18 = False
        self.show_group_19 = False
        self.show_group_20 = False
        self.show_group_21 = False
        self.show_group_22 = False
        self.show_group_23 = False
        self.show_group_24 = False
        self.show_group_25 = False
        self.show_group_26 = False
        self.show_group_27 = False
        self.show_group_28 = False
        self.show_group_29 = False
        self.show_group_30 = False
        self.groups_real = True


class CellBlenderTestSuitePanel(bpy.types.Panel):
    bl_label = "CellBlender Test Suite"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    def draw(self, context):
        app = context.scene.cellblender_test_suite

        box = self.layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'
        if not app.show_setup:
            row.prop(app, "show_setup", icon='TRIA_RIGHT', text="Setup Panel", emboss=False)
        else:
            row.prop(app, "show_setup", icon='TRIA_DOWN', text="Setup Panel", emboss=False)

            row = box.row()
            row.operator("cellblender_test.set_mcell_path", text="Set Path to MCell Binary", icon='FILESEL')
            row = box.row()
            row.prop ( app, "path_to_mcell" )
            row = box.row()
            row.prop ( app, "submit_host" )

            # Problems getting this to work ... use current directory for now
            #row = box.row()
            #row.operator("cellblender_test.set_blend_path", text="Set Path to Blend files", icon='FILESEL')
            #row = box.row()
            #row.prop ( app, "path_to_blend" )


        row = self.layout.row()
        row.operator ( "cellblender_test.load_home_file" )
        row.operator ( "cellblender_test.save_home_file" )

        row = self.layout.row()
        if app.test_status == "?":
          row.label( icon='QUESTION',  text="?" )
        elif app.test_status == "P":
          row.label( icon='FILE_TICK', text="Pass" )
        elif app.test_status == "F":
          row.label( icon='ERROR',     text="Fail" )
        row.prop(app, "exit_on_error")
        row.prop(app, "run_mcell")
        row.prop(app, "run_method",    text="")
        # row.prop(app, "run_with_queue")
        row.prop(app, "update_soure_file")
        if app.update_soure_file:
            row = self.layout.row()
            col = row.column()
            col.prop ( app, "source_file_to_update" )
            col = row.column()
            col.operator("cellblender_test.set_source_file", text="", icon='FILESEL')

        for group_num in range(next_test_group_num):
            # print ( "Drawing Group " + str(group_num) )
            group = test_groups[group_num]

            box = self.layout.box()
            row = box.row(align=True)
            row.alignment = 'LEFT'

            gi = group['group_index']

            # print ( "Group Index = " + str(gi) + ", app[gi] = " + str(app["show_group_"+str(gi)]) )
            
            if not app["show_group_"+str(gi)]:
                row.prop(app, "show_group_"+str(gi), icon='TRIA_RIGHT', text=group['group_name'], emboss=False)
            else:
                row.prop(app, "show_group_"+str(gi), icon='TRIA_DOWN', text=group['group_name'], emboss=False)
                if group['group_name'] == "Stress Tests":
                    row = box.row()
                    row.prop(app, "stress_test_level")
                test_list = group['group_tests']
                for test in test_list:
                    row = box.row()
                    row.operator(test['operator_name'], text=test['test_name'])


class LoadHomeOp(bpy.types.Operator):
    bl_idname = "cellblender_test.load_home_file"
    bl_label = "Load Startup"

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):
        context.scene.cellblender_test_suite.test_status = "?"
        context.scene.cellblender_test_suite.groups_real = False
        bpy.ops.wm.read_homefile()
        return { 'FINISHED' }


class SaveHomeOp(bpy.types.Operator):
    bl_idname = "cellblender_test.save_home_file"
    bl_label = "Save Startup"

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):
        if context.scene.cellblender_test_suite.test_status == "?":
            bpy.ops.wm.save_homefile()
        else:
            self.report({'ERROR'}, "Warning: CellBlender is enabled. Use File menu to over-ride.")
        return { 'FINISHED' }


class SetMCellBinary(bpy.types.Operator):
    bl_idname = "cellblender_test.set_mcell_path"
    bl_label = "Set MCell Binary"
    bl_description = ("Set MCell Binary. If needed, download at mcell.org/download.html")
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        app = context.scene.cellblender_test_suite
        app.path_to_mcell = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SetBlendPath(bpy.types.Operator):
    bl_idname = "cellblender_test.set_blend_path"
    bl_label = "Set Path to Blend File"
    bl_description = ("Set Path to the Blend File created for each test.")
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        app = context.scene.cellblender_test_suite
        app.path_to_blend = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SetSourceFile(bpy.types.Operator):
    bl_idname = "cellblender_test.set_source_file"
    bl_label = "Set Source File"
    bl_description = ("Set Source File. Select a file for updating hash results. Be sure results are correct first!!")
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        app = context.scene.cellblender_test_suite
        app.source_file_to_update = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



class CellBlender_Model:

    old_type = None
    context = None
    scn = None
    mcell = None
    path_to_blend = None

    def __init__(self, cb_context, model_name=None):
        banner_text = "Initializing CellBlender Model"
        if model_name != None:
            banner_text = "Initializing CellBlender Model: \"" + str(model_name) + "\""
        print ( "\n##############################################################################################################" )
        print ( "##############################################################################################################" )
        print ( "## " + banner_text )
        print ( "##############################################################################################################" )
        print ( "##############################################################################################################\n" )
        # bpy.ops.wm.read_homefile()
        self.old_type = None
        self.context = cb_context
        self.setup_cb_defaults ( self.context )
        self.context.scene.cellblender_test_suite.test_status = "?"


    def using_id_params(self):
        ps = bpy.context.scene.mcell.parameter_system
        new_id = False
        if 'active_elist' in dir(ps):
            new_id = True

        #print ( "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
        #if new_id:
        #    print ( "Running with new ID parameters" )
        #else:
        #    print ( "Running with old RNA parameters" )
        #print ( "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n" )

        return new_id


    def get_scene(self):
        return self.scn

    def get_mcell(self):
        return self.mcell


    def set_view_3d(self):
        area = bpy.context.area
        if area == None:
            self.old_type = 'VIEW_3D'
        else:
            self.old_type = area.type
        area.type = 'VIEW_3D'
      
    def set_view_back(self):
        area = bpy.context.area
        area.type = self.old_type

    def save_blend_file( self, context ):
        app = context.scene.cellblender_test_suite
        wm = context.window_manager

        if len(app.path_to_blend) > 0:
            self.path_to_blend = app.path_to_blend
        else:
            self.path_to_blend = os.getcwd() + os.sep + "Test.blend"

        bpy.ops.wm.save_as_mainfile(filepath=self.path_to_blend, check_existing=False)


    def get_scene(self):
        return bpy.data.scenes['Scene']

    def select_none(self):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            obj.select = False

    def delete_all_objects(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)

    def reload_cellblender(self, scn):
        print ( "Disabling CellBlender Application" )
        bpy.ops.wm.addon_disable(module='cellblender')

        print ( "Delete MCell RNA properties if needed" )
        # del bpy.types.Scene.mcell
        if scn.get ( 'mcell' ):
            print ( "Deleting MCell RNA properties" )
            del scn['mcell']

        print ( "Enabling CellBlender Application" )
        bpy.ops.wm.addon_enable(module='cellblender')


    def setup_mcell(self, scn):
        mcell = scn.mcell
        app = bpy.context.scene.cellblender_test_suite

        print ( "Initializing CellBlender Application" )
        bpy.ops.mcell.init_cellblender()

        print ( "Setting Preferences" )
        if len(app.path_to_mcell) > 0:
            mcell.cellblender_preferences.mcell_binary = app.path_to_mcell
        else:
            mcell.cellblender_preferences.mcell_binary = os.getcwd() + relative_path_to_mcell

        mcell.run_simulation.sge_host_name = app.submit_host

        mcell.cellblender_preferences.mcell_binary_valid = True
        mcell.cellblender_preferences.show_sim_runner_options = True
        mcell.run_simulation.simulation_run_control = app.run_method
        
        return mcell

    def decouple_export_and_run ( self, context, val=True ):
        context.scene.mcell.cellblender_preferences.decouple_export_run = val

    def setup_cb_defaults ( self, context ):

        self.save_blend_file( context )
        scn = self.get_scene()
        self.set_view_3d()
        self.delete_all_objects()
        self.reload_cellblender(scn)
        mcell = self.setup_mcell(scn)

        print ( "Snapping Cursor to Center" )
        bpy.ops.view3d.snap_cursor_to_center()
        print ( "Done Snapping Cursor to Center" )
        
        print ( "#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#" )
        print ( "#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#" )
        print ( "#-#-#-#-#-#-# For compatibility with old defaults:  #-#-#-#-#-#" )
        print ( "#-#-#-#-#-#-#   export parameters as numeric values #-#-#-#-#-#" )
        print ( "#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#" )
        print ( "#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#" )
        mcell.parameter_system.export_as_expressions = False

        self.scn = scn
        self.mcell = mcell

    def set_draw_type_for_object ( self, name="", draw_type="WIRE" ):
        if name in bpy.data.objects:
            bpy.data.objects[name].draw_type = draw_type


    def create_object_from_mesh ( self, name="ObjectFromMesh", draw_type="WIRE", x=0, y=0, z=0, vertex_list=None, face_list=None ):

        print ( "===> Creating an object from " + str(len(vertex_list)) + " vertices and " + str(len(face_list)) + " faces." )
        vertices = []
        for point in vertex_list:
            vertices.append ( mathutils.Vector((point.x+x,point.y+y,point.z+z)) )
        faces = []
        for face_element in face_list:
            faces.append ( face_element.verts )

        new_mesh = bpy.data.meshes.new ( name + "_mesh" )
        new_mesh.from_pydata ( vertices, [], faces )
        new_mesh.update()
        new_obj = bpy.data.objects.new ( name, new_mesh )

        self.scn.objects.link ( new_obj )
        bpy.ops.object.select_all ( action = "DESELECT" )
        new_obj.select = True
        self.scn.objects.active = new_obj

        # Add the newly added object to the model objects list

        self.mcell.cellblender_main_panel.objects_select = True
        bpy.ops.mcell.model_objects_add()
        bpy.ops.object.mode_set ( mode="OBJECT" )
        bpy.data.objects[name].draw_type = draw_type
        print ( "Done Adding " + name + " as a Blender Object" )


    def add_active_object_to_model ( self, name="Cell", draw_type="WIRE" ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )
        bpy.data.objects[name].select = True

        # Make the object active and add it to the model objects list

        self.scn.objects.active = bpy.data.objects[name]

        self.mcell.cellblender_main_panel.objects_select = True
        bpy.ops.mcell.model_objects_add()
        bpy.data.objects[name].draw_type = draw_type
        print ( "Done Adding " + name )


    # The old add_cube_to_model used Blender's primitive_cube_add function which varied between versions.
    # This produced varying MDL which could not be easily checked against a precomputed SHA1.
    # So this old version was replaced, but it's kept here to show how Blender's primitives can be used.
    def old_add_cube_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, size=1 ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )
        bpy.ops.mesh.primitive_cube_add ( location=(x,y,z), radius=size)
        self.scn.objects.active.name = name

        # Add the newly added object to the model objects list

        self.mcell.cellblender_main_panel.objects_select = True
        bpy.ops.mcell.model_objects_add()
        bpy.data.objects[name].draw_type = draw_type
        print ( "Done Adding " + name )


    # This version of add_cube_to_model produces repeatable results across Blender versions.
    def add_cube_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, size=1 ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )

        cube = plf_object

        cube.points = [
            point ( -1.0, -1.0, -1.0 ),
            point ( -1.0, -1.0, 1.0 ),
            point ( -1.0, 1.0, -1.0 ),
            point ( -1.0, 1.0, 1.0 ),
            point ( 1.0, -1.0, -1.0 ),
            point ( 1.0, -1.0, 1.0 ),
            point ( 1.0, 1.0, -1.0 ),
            point ( 1.0, 1.0, 1.0 )
          ]

        cube.faces = [
            face ( 3, 0, 1 ),
            face ( 7, 2, 3 ),
            face ( 5, 6, 7 ),
            face ( 1, 4, 5 ),
            face ( 2, 4, 0 ),
            face ( 7, 1, 5 ),
            face ( 3, 2, 0 ),
            face ( 7, 6, 2 ),
            face ( 5, 4, 6 ),
            face ( 1, 0, 4 ),
            face ( 2, 6, 4 ),
            face ( 7, 3, 1 )
          ]

        for p in cube.points:
            p.x = p.x * size
            p.y = p.y * size
            p.z = p.z * size

        self.create_object_from_mesh ( name=name, draw_type=draw_type, x=x, y=y, z=z, vertex_list=cube.points, face_list=cube.faces )

        print ( "Done Adding " + name )




    # This version of add_torus_to_model produces repeatable result across Blender versions.
    # This version is hard-coded to: major_segments=20,minor_segments=10,major_radius=0.1,minor_radius=0.03
    def add_fixed_torus_to_model ( self, name="Torus", draw_type="WIRE" ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )

        torus = plf_object

        torus_points = [
            [0.13,0,0],[0.1243,0,0.01763],[0.1093,0,0.02853],[0.09073,0,0.02853],[0.07573,0,0.01763],[0.07,0,3.674e-18],
            [0.07573,0,-0.01763],[0.09073,0,-0.02853],[0.1093,0,-0.02853],[0.1243,0,-0.01763],[0.1236,0.04017,0],
            [0.1182,0.0384,0.01763],[0.1039,0.03377,0.02853],[0.08629,0.02804,0.02853],[0.07202,0.0234,0.01763],[0.06657,0.02163,3.674e-18],
            [0.07202,0.0234,-0.01763],[0.08629,0.02804,-0.02853],[0.1039,0.03377,-0.02853],[0.1182,0.0384,-0.01763],
            [0.1052,0.07641,0],[0.1005,0.07304,0.01763],[0.0884,0.06423,0.02853],[0.0734,0.05333,0.02853],[0.06127,0.04451,0.01763],
            [0.05663,0.04114,3.674e-18],[0.06127,0.04451,-0.01763],[0.0734,0.05333,-0.02853],[0.0884,0.06423,-0.02853],
            [0.1005,0.07304,-0.01763],[0.07641,0.1052,0],[0.07304,0.1005,0.01763],[0.06423,0.0884,0.02853],[0.05333,0.0734,0.02853],
            [0.04451,0.06127,0.01763],[0.04114,0.05663,3.674e-18],[0.04451,0.06127,-0.01763],[0.05333,0.0734,-0.02853],
            [0.06423,0.0884,-0.02853],[0.07304,0.1005,-0.01763],[0.04017,0.1236,0],[0.0384,0.1182,0.01763],[0.03377,0.1039,0.02853],
            [0.02804,0.08629,0.02853],[0.0234,0.07202,0.01763],[0.02163,0.06657,3.674e-18],[0.0234,0.07202,-0.01763],
            [0.02804,0.08629,-0.02853],[0.03377,0.1039,-0.02853],[0.0384,0.1182,-0.01763],[7.451e-09,0.13,0],[1.118e-08,0.1243,0.01763],
            [1.118e-08,0.1093,0.02853],[7.451e-09,0.09073,0.02853],[3.725e-09,0.07573,0.01763],[3.725e-09,0.07,3.674e-18],
            [3.725e-09,0.07573,-0.01763],[7.451e-09,0.09073,-0.02853],[1.118e-08,0.1093,-0.02853],[1.118e-08,0.1243,-0.01763],
            [-0.04017,0.1236,0],[-0.0384,0.1182,0.01763],[-0.03377,0.1039,0.02853],[-0.02804,0.08629,0.02853],[-0.0234,0.07202,0.01763],
            [-0.02163,0.06657,3.674e-18],[-0.0234,0.07202,-0.01763],[-0.02804,0.08629,-0.02853],[-0.03377,0.1039,-0.02853],
            [-0.0384,0.1182,-0.01763],[-0.07641,0.1052,0],[-0.07304,0.1005,0.01763],[-0.06423,0.0884,0.02853],[-0.05333,0.0734,0.02853],
            [-0.04451,0.06127,0.01763],[-0.04114,0.05663,3.674e-18],[-0.04451,0.06127,-0.01763],[-0.05333,0.0734,-0.02853],
            [-0.06423,0.0884,-0.02853],[-0.07304,0.1005,-0.01763],[-0.1052,0.07641,0],[-0.1005,0.07304,0.01763],[-0.0884,0.06423,0.02853],
            [-0.0734,0.05333,0.02853],[-0.06127,0.04451,0.01763],[-0.05663,0.04114,3.674e-18],[-0.06127,0.04451,-0.01763],
            [-0.0734,0.05333,-0.02853],[-0.0884,0.06423,-0.02853],[-0.1005,0.07304,-0.01763],[-0.1236,0.04017,0],
            [-0.1182,0.0384,0.01763],[-0.1039,0.03377,0.02853],[-0.08629,0.02804,0.02853],[-0.07202,0.0234,0.01763],
            [-0.06657,0.02163,3.674e-18],[-0.07202,0.0234,-0.01763],[-0.08629,0.02804,-0.02853],[-0.1039,0.03377,-0.02853],
            [-0.1182,0.0384,-0.01763],[-0.13,1.136e-08,0],[-0.1243,1.086e-08,0.01763],[-0.1093,9.553e-09,0.02853],
            [-0.09073,7.932e-09,0.02853],[-0.07573,6.62e-09,0.01763],[-0.07,6.12e-09,3.674e-18],[-0.07573,6.62e-09,-0.01763],
            [-0.09073,7.932e-09,-0.02853],[-0.1093,9.553e-09,-0.02853],[-0.1243,1.086e-08,-0.01763],[-0.1236,-0.04017,0],
            [-0.1182,-0.0384,0.01763],[-0.1039,-0.03377,0.02853],[-0.08629,-0.02804,0.02853],[-0.07202,-0.0234,0.01763],
            [-0.06657,-0.02163,3.674e-18],[-0.07202,-0.0234,-0.01763],[-0.08629,-0.02804,-0.02853],[-0.1039,-0.03377,-0.02853],
            [-0.1182,-0.0384,-0.01763],[-0.1052,-0.07641,0],[-0.1005,-0.07304,0.01763],[-0.0884,-0.06423,0.02853],
            [-0.0734,-0.05333,0.02853],[-0.06127,-0.04451,0.01763],[-0.05663,-0.04114,3.674e-18],[-0.06127,-0.04451,-0.01763],
            [-0.0734,-0.05333,-0.02853],[-0.0884,-0.06423,-0.02853],[-0.1005,-0.07304,-0.01763],[-0.07641,-0.1052,0],
            [-0.07304,-0.1005,0.01763],[-0.06423,-0.0884,0.02853],[-0.05333,-0.0734,0.02853],[-0.04451,-0.06127,0.01763],
            [-0.04114,-0.05663,3.674e-18],[-0.04451,-0.06127,-0.01763],[-0.05333,-0.0734,-0.02853],[-0.06423,-0.0884,-0.02853],
            [-0.07304,-0.1005,-0.01763],[-0.04017,-0.1236,0],[-0.0384,-0.1182,0.01763],[-0.03377,-0.1039,0.02853],
            [-0.02804,-0.08629,0.02853],[-0.0234,-0.07202,0.01763],[-0.02163,-0.06657,3.674e-18],[-0.0234,-0.07202,-0.01763],
            [-0.02804,-0.08629,-0.02853],[-0.03377,-0.1039,-0.02853],[-0.0384,-0.1182,-0.01763],[7.451e-09,-0.13,0],
            [1.118e-08,-0.1243,0.01763],[1.118e-08,-0.1093,0.02853],[7.451e-09,-0.09073,0.02853],[3.725e-09,-0.07573,0.01763],
            [3.725e-09,-0.07,3.674e-18],[3.725e-09,-0.07573,-0.01763],[7.451e-09,-0.09073,-0.02853],[1.118e-08,-0.1093,-0.02853],
            [1.118e-08,-0.1243,-0.01763],[0.04017,-0.1236,0],[0.0384,-0.1182,0.01763],[0.03377,-0.1039,0.02853],[0.02804,-0.08629,0.02853],
            [0.0234,-0.07202,0.01763],[0.02163,-0.06657,3.674e-18],[0.0234,-0.07202,-0.01763],[0.02804,-0.08629,-0.02853],
            [0.03377,-0.1039,-0.02853],[0.0384,-0.1182,-0.01763],[0.07641,-0.1052,0],[0.07304,-0.1005,0.01763],[0.06423,-0.0884,0.02853],
            [0.05333,-0.0734,0.02853],[0.04451,-0.06127,0.01763],[0.04114,-0.05663,3.674e-18],[0.04451,-0.06127,-0.01763],
            [0.05333,-0.0734,-0.02853],[0.06423,-0.0884,-0.02853],[0.07304,-0.1005,-0.01763],[0.1052,-0.07641,0],
            [0.1005,-0.07304,0.01763],[0.0884,-0.06423,0.02853],[0.0734,-0.05333,0.02853],[0.06127,-0.04451,0.01763],
            [0.05663,-0.04114,3.674e-18],[0.06127,-0.04451,-0.01763],[0.0734,-0.05333,-0.02853],[0.0884,-0.06423,-0.02853],
            [0.1005,-0.07304,-0.01763],[0.1236,-0.04017,0],[0.1182,-0.0384,0.01763],[0.1039,-0.03377,0.02853],[0.08629,-0.02804,0.02853],
            [0.07202,-0.0234,0.01763],[0.06657,-0.02163,3.674e-18],[0.07202,-0.0234,-0.01763],[0.08629,-0.02804,-0.02853],
            [0.1039,-0.03377,-0.02853],[0.1182,-0.0384,-0.01763]
          ]

        torus_faces = [
            [10,1,0],[1,12,2],[2,13,3],[13,4,3],[4,15,5],[15,6,5],[16,7,6],[17,8,7],[18,9,8],[9,10,0],[10,21,11],
            [21,12,11],[12,23,13],[13,24,14],[24,15,14],[15,26,16],[26,17,16],[27,18,17],[18,29,19],[29,10,19],[30,21,20],
            [31,22,21],[32,23,22],[33,24,23],[34,25,24],[25,36,26],[36,27,26],[27,38,28],[38,29,28],[29,30,20],[30,41,31],
            [41,32,31],[42,33,32],[43,34,33],[44,35,34],[45,36,35],[46,37,36],[47,38,37],[48,39,38],[49,30,39],[40,51,41],
            [41,52,42],[52,43,42],[53,44,43],[44,55,45],[55,46,45],[46,57,47],[57,48,47],[58,49,48],[59,40,49],[50,61,51],
            [61,52,51],[62,53,52],[63,54,53],[64,55,54],[65,56,55],[56,67,57],[57,68,58],[68,59,58],[59,60,50],[70,61,60],
            [61,72,62],[72,63,62],[63,74,64],[74,65,64],[75,66,65],[76,67,66],[77,68,67],[78,69,68],[79,60,69],[80,71,70],
            [81,72,71],[82,73,72],[73,84,74],[84,75,74],[85,76,75],[86,77,76],[77,88,78],[88,79,78],[89,70,79],[80,91,81],
            [91,82,81],[92,83,82],[83,94,84],[94,85,84],[95,86,85],[96,87,86],[97,88,87],[98,89,88],[99,80,89],[90,101,91],
            [101,92,91],[102,93,92],[103,94,93],[104,95,94],[105,96,95],[96,107,97],[97,108,98],[98,109,99],[109,90,99],
            [110,101,100],[111,102,101],[112,103,102],[113,104,103],[114,105,104],[115,106,105],[106,117,107],[107,118,108],
            [108,119,109],[109,110,100],[120,111,110],[111,122,112],[122,113,112],[123,114,113],[124,115,114],[125,116,115],
            [126,117,116],[117,128,118],[128,119,118],[129,110,119],[120,131,121],[121,132,122],[122,133,123],[133,124,123],
            [134,125,124],[135,126,125],[136,127,126],[137,128,127],[138,129,128],[139,120,129],[140,131,130],[141,132,131],
            [142,133,132],[143,134,133],[144,135,134],[145,136,135],[136,147,137],[147,138,137],[148,139,138],[149,130,139],
            [150,141,140],[141,152,142],[142,153,143],[143,154,144],[154,145,144],[155,146,145],[156,147,146],[157,148,147],
            [158,149,148],[159,140,149],[160,151,150],[161,152,151],[162,153,152],[153,164,154],[164,155,154],[165,156,155],
            [166,157,156],[167,158,157],[158,169,159],[159,160,150],[170,161,160],[171,162,161],[162,173,163],[173,164,163],
            [164,175,165],[175,166,165],[176,167,166],[177,168,167],[178,169,168],[179,160,169],[180,171,170],[181,172,171],
            [172,183,173],[183,174,173],[174,185,175],[185,176,175],[186,177,176],[187,178,177],[178,189,179],[189,170,179],
            [190,181,180],[191,182,181],[182,193,183],[193,184,183],[194,185,184],[195,186,185],[186,197,187],[197,188,187],
            [188,199,189],[199,180,189],[0,191,190],[191,2,192],[192,3,193],[3,194,193],[4,195,194],[5,196,195],[6,197,196],
            [7,198,197],[8,199,198],[199,0,190],[10,11,1],[1,11,12],[2,12,13],[13,14,4],[4,14,15],[15,16,6],[16,17,7],
            [17,18,8],[18,19,9],[9,19,10],[10,20,21],[21,22,12],[12,22,23],[13,23,24],[24,25,15],[15,25,26],[26,27,17],
            [27,28,18],[18,28,29],[29,20,10],[30,31,21],[31,32,22],[32,33,23],[33,34,24],[34,35,25],[25,35,36],[36,37,27],
            [27,37,38],[38,39,29],[29,39,30],[30,40,41],[41,42,32],[42,43,33],[43,44,34],[44,45,35],[45,46,36],[46,47,37],
            [47,48,38],[48,49,39],[49,40,30],[40,50,51],[41,51,52],[52,53,43],[53,54,44],[44,54,55],[55,56,46],[46,56,57],
            [57,58,48],[58,59,49],[59,50,40],[50,60,61],[61,62,52],[62,63,53],[63,64,54],[64,65,55],[65,66,56],[56,66,67],
            [57,67,68],[68,69,59],[59,69,60],[70,71,61],[61,71,72],[72,73,63],[63,73,74],[74,75,65],[75,76,66],[76,77,67],
            [77,78,68],[78,79,69],[79,70,60],[80,81,71],[81,82,72],[82,83,73],[73,83,84],[84,85,75],[85,86,76],[86,87,77],
            [77,87,88],[88,89,79],[89,80,70],[80,90,91],[91,92,82],[92,93,83],[83,93,94],[94,95,85],[95,96,86],[96,97,87],
            [97,98,88],[98,99,89],[99,90,80],[90,100,101],[101,102,92],[102,103,93],[103,104,94],[104,105,95],[105,106,96],
            [96,106,107],[97,107,108],[98,108,109],[109,100,90],[110,111,101],[111,112,102],[112,113,103],[113,114,104],
            [114,115,105],[115,116,106],[106,116,117],[107,117,118],[108,118,119],[109,119,110],[120,121,111],[111,121,122],
            [122,123,113],[123,124,114],[124,125,115],[125,126,116],[126,127,117],[117,127,128],[128,129,119],[129,120,110],
            [120,130,131],[121,131,132],[122,132,133],[133,134,124],[134,135,125],[135,136,126],[136,137,127],[137,138,128],
            [138,139,129],[139,130,120],[140,141,131],[141,142,132],[142,143,133],[143,144,134],[144,145,135],[145,146,136],
            [136,146,147],[147,148,138],[148,149,139],[149,140,130],[150,151,141],[141,151,152],[142,152,153],[143,153,154],
            [154,155,145],[155,156,146],[156,157,147],[157,158,148],[158,159,149],[159,150,140],[160,161,151],[161,162,152],
            [162,163,153],[153,163,164],[164,165,155],[165,166,156],[166,167,157],[167,168,158],[158,168,169],[159,169,160],
            [170,171,161],[171,172,162],[162,172,173],[173,174,164],[164,174,175],[175,176,166],[176,177,167],[177,178,168],
            [178,179,169],[179,170,160],[180,181,171],[181,182,172],[172,182,183],[183,184,174],[174,184,185],[185,186,176],
            [186,187,177],[187,188,178],[178,188,189],[189,180,170],[190,191,181],[191,192,182],[182,192,193],[193,194,184],
            [194,195,185],[195,196,186],[186,196,197],[197,198,188],[188,198,199],[199,190,180],[0,1,191],[191,1,2],
            [192,2,3],[3,4,194],[4,5,195],[5,6,196],[6,7,197],[7,8,198],[8,9,199],[199,9,0]
          ]

        torus.points = []
        for p in torus_points:
          torus.points.append ( point ( p[0], p[1], p[2] ) )

        torus.faces = []
        for f in torus_faces:
          torus.faces.append ( face ( f[0], f[1], f[2] ) )

        self.create_object_from_mesh ( name=name, draw_type=draw_type, x=0, y=0, z=0, vertex_list=torus.points, face_list=torus.faces )

        print ( "Done Adding " + name )




    # The old add_icosphere_to_model used Blender's primitive_ico_sphere_add function which varied between versions.
    # This produced varying MDL which could not be easily checked against a precomputed SHA1.
    # So this old version was replaced, but it's kept here to show how Blender's primitives can be used.
    def old_add_icosphere_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, size=1, subdiv=2 ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )
        bpy.ops.mesh.primitive_ico_sphere_add ( subdivisions=subdiv, size=size, location=(x, y, z) )
        self.scn.objects.active.name = name

        # Add the newly added object to the model objects list

        self.mcell.cellblender_main_panel.objects_select = True
        bpy.ops.mcell.model_objects_add()
        bpy.data.objects[name].draw_type = draw_type
        print ( "Done Adding " + name )


    # This version of add_icosphere_to_model produces repeatable results across Blender versions.
    def add_icosphere_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, size=1, subdiv=2 ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """
        print ( "Adding " + name )

        ico = IcoSphere ( subdiv-1, scale_x=size, scale_y=size, scale_z=size )
        self.create_object_from_mesh ( name=name, draw_type=draw_type, x=x, y=y, z=z, vertex_list=ico.points, face_list=ico.faces )

        self.scn.objects.active.name = name

        # Add the newly added object to the model objects list

        self.mcell.cellblender_main_panel.objects_select = True
        bpy.ops.mcell.model_objects_add()
        bpy.data.objects[name].draw_type = draw_type
        print ( "Done Adding " + name )



    def add_capsule_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, sigma=0, subdiv=2, radius=1, cyl_len=2, subdivide_sides=True ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """

        capsule = Capsule(subdiv,radius,cyl_len,subdivide_sides)
        
        capsule.dither_points ( sigma, sigma, sigma )

        #print ( "Writing capsule.plf" )
        #capsule.dump_as_plf ( "capsule.plf" )

        self.create_object_from_mesh ( name=name, draw_type=draw_type, x=x, y=y, z=z, vertex_list=capsule.points, face_list=capsule.faces )


    def add_shaped_cylinder_to_model ( self, name="Cell", draw_type="WIRE", x=0, y=0, z=0, sigma=0, numsect=10, z_profile=[ (-2,0.5), (-1.8,0.1), (0,0.1), (0.2,0.5), (2,0.8) ] ):
        """ draw_type is one of: WIRE, TEXTURED, SOLID, BOUNDS """

        capsule = ShapedCylinder ( numsect, z_profile )
        
        capsule.dither_points ( sigma, sigma, sigma )

        self.create_object_from_mesh ( name=name, draw_type=draw_type, x=x, y=y, z=z, vertex_list=capsule.points, face_list=capsule.faces )



    def add_label_to_model ( self, name="Label", text="Text", x=0, y=0, z=0, size=1, rx=0, ry=0, rz=0 ):
        #print ( "Adding " + text )

        bpy.ops.object.text_add ( location=(x,y,z), rotation=(rx,ry,rz), radius=size )
        tobj = bpy.context.active_object
        tobj.data.body = text

        #print ( "Done Adding " + text )




    def add_parameter_to_model ( self, name="a", expr="0.0", units="", desc="" ):
        """ Add a parameter to the model """
        #print ( "Test Suite Adding Parameter " + name + " = " + expr )
        ps = self.mcell.parameter_system
        if self.using_id_params():
            ps.add_general_parameter_and_update ( self.context, name=name, expr=expr, units=units, desc=desc )
        else:
            ps.new_parameter ( name, pp=False, new_expr=expr, new_units=units, new_desc=desc )
        #print ( "Test Suite Done Adding Parameter " + name )
        #return ps.general_parameter_list[ps.active_par_index]




    def parameter_system_op_add ( self ):
        """ Add a parameter to the model """
        #print ( "Test Suite Parameter Operator: add begin" )
        bpy.ops.mcell.add_parameter()
        #print ( "Test Suite Parameter Operator: add done " )


    def parameter_system_op_remove ( self ):
        """ Remove the active parameter to the model """
        #print ( "Test Suite Parameter Operator: remove begin" )
        bpy.ops.mcell.remove_parameter()
        #print ( "Test Suite Parameter Operator: remove done " )


    def parameter_system_op_set_active ( self, index ):
        """ Set the active parameter for the model """
        #print ( "Test Suite Parameter Operator: set active " + str(index) + " begin" )
        self.mcell.parameter_system.active_par_index = index
        #print ( "Test Suite Parameter Operator: active done " )


    def parameter_system_index_of_name ( self, name ):
        """ Return the first index of the name in the general parameter list """

        #print ( "Test Suite Parameter Index of Name: " + str(name) + " begin" )
        if self.using_id_params():
            gpl = self.mcell.parameter_system.general_parameter_list
            index = 0
            for gp in gpl:
                if gp['name'] == name:
                    return index
                index += 1
        else:
            gpl = self.mcell.parameter_system.general_parameter_list
            gpls = self.mcell.parameter_system.general_parameter_sort_list
            index = 0
            for gp in gpls:
                if gp['name'] == name:
                    return index
                index += 1
        return -1


    def parameter_system_op_get_active ( self ):
        """ Set the active parameter for the model """
        #print ( "Test Suite Parameter Operator: get active" )
        return self.mcell.parameter_system.active_par_index


    def parameter_system_prop_name ( self, name ):
        """ Change active parameter name """
        #print ( "Test Suite Parameter Property: name = " + str(name) )
        if self.using_id_params():
            self.mcell.parameter_system.active_name = name
        else:
            ps = self.mcell.parameter_system
            ps.general_parameter_list[ps.active_par_index].par_name = name
        #print ( "Test Suite Parameter Property: name done " )

    def parameter_system_prop_expr ( self, expr ):
        """ Change active parameter expression """
        #print ( "Test Suite Parameter Property: expr = " + str(expr) )
        if self.using_id_params():
            self.mcell.parameter_system.active_expr = expr
        else:
            ps = self.mcell.parameter_system
            ps.general_parameter_list[ps.active_par_index].expr = expr
        #print ( "Test Suite Parameter Property: expr done " )

    def parameter_system_prop_units ( self, units ):
        """ Change active parameter units """
        #print ( "Test Suite Parameter Property: units = " + str(units) )
        if self.using_id_params():
            self.mcell.parameter_system.active_units = units
        else:
            ps = self.mcell.parameter_system
            ps.general_parameter_list[ps.active_par_index].units = units
        #print ( "Test Suite Parameter Property: units done " )

    def parameter_system_prop_desc ( self, desc ):
        """ Change active parameter desc """
        #print ( "Test Suite Parameter Property: desc = " + str(desc) )
        if self.using_id_params():
            self.mcell.parameter_system.active_desc = desc
        else:
            ps = self.mcell.parameter_system
            ps.general_parameter_list[ps.active_par_index].descr = desc
        #print ( "Test Suite Parameter Property: desc done " )




    def add_molecule_species_to_model ( self, name="A", mol_type="3D", diff_const_expr="0.0", custom_time_step="" ):
        """ Add a molecule species """
        print ( "Adding Molecule Species " + name )
        self.mcell.cellblender_main_panel.molecule_select = True
        bpy.ops.mcell.molecule_add()
        mol_index = self.mcell.molecules.active_mol_index
        self.mcell.molecules.molecule_list[mol_index].name = name
        self.mcell.molecules.molecule_list[mol_index].type = mol_type
        self.mcell.molecules.molecule_list[mol_index].diffusion_constant.set_expr(diff_const_expr)
        self.mcell.molecules.molecule_list[mol_index].custom_time_step.set_expr(custom_time_step)
        print ( "Done Adding Molecule " + name + " = " + str(self.mcell.molecules.molecule_list[mol_index].name) )
        return self.mcell.molecules.molecule_list[mol_index]


    def get_molecule_species_by_name ( self, name ):
        """ Get a molecule species """
        print ( "Getting Molecule Species " + name )
        return self.mcell.molecules.molecule_list.get(name)


    def add_molecule_release_site_to_model ( self, name=None, mol="a", shape="SPHERICAL", obj_expr="", orient="'", q_expr="100", q_type='NUMBER_TO_RELEASE', d="0", x="0", y="0", z="0", pattern=None ):
        """ Add a molecule release site """
        """ shape is one of: 'CUBIC', 'SPHERICAL', 'SPHERICAL_SHELL', 'OBJECT' """
        """ q_type is one of: 'NUMBER_TO_RELEASE', 'GAUSSIAN_RELEASE_NUMBER', 'DENSITY' """
        if name == None:
            name = "rel_" + mol

        print ( "Releasing Molecules at " + name )
        self.mcell.cellblender_main_panel.placement_select = True
        bpy.ops.mcell.release_site_add()
        rel_index = self.mcell.release_sites.active_release_index
        self.mcell.release_sites.mol_release_list[rel_index].name = name
        self.mcell.release_sites.mol_release_list[rel_index].molecule = mol
        self.mcell.release_sites.mol_release_list[rel_index].shape = shape
        self.mcell.release_sites.mol_release_list[rel_index].object_expr = obj_expr
        self.mcell.release_sites.mol_release_list[rel_index].orient = orient
        self.mcell.release_sites.mol_release_list[rel_index].quantity_type = q_type
        self.mcell.release_sites.mol_release_list[rel_index].quantity.set_expr(q_expr)
        self.mcell.release_sites.mol_release_list[rel_index].diameter.set_expr(d)
        self.mcell.release_sites.mol_release_list[rel_index].location_x.set_expr(x)
        self.mcell.release_sites.mol_release_list[rel_index].location_y.set_expr(y)
        self.mcell.release_sites.mol_release_list[rel_index].location_z.set_expr(z)
        if pattern != None:
            self.mcell.release_sites.mol_release_list[rel_index].pattern = pattern
        print ( "Done Releasing Molecule " + name )
        return self.mcell.release_sites.mol_release_list[rel_index]



    def add_release_pattern_to_model ( self, name="time_pattern", delay="0", release_interval="", train_duration="", train_interval="", num_trains="1" ):
        """ Add a release time pattern """
        print ( "Adding a Release Time Pattern " + name + " " + delay + " " + release_interval )
        bpy.ops.mcell.release_pattern_add()
        pat_index = self.mcell.release_patterns.active_release_pattern_index
        self.mcell.release_patterns.release_pattern_list[pat_index].name = name
        self.mcell.release_patterns.release_pattern_list[pat_index].delay.set_expr ( delay )
        self.mcell.release_patterns.release_pattern_list[pat_index].release_interval.set_expr ( release_interval )
        self.mcell.release_patterns.release_pattern_list[pat_index].train_duration.set_expr ( train_duration )
        self.mcell.release_patterns.release_pattern_list[pat_index].train_interval.set_expr ( train_interval )
        self.mcell.release_patterns.release_pattern_list[pat_index].number_of_trains.set_expr ( num_trains )
        print ( "Done Adding Release Time Pattern " + name + " " + delay + " " + release_interval )
        return self.mcell.release_patterns.release_pattern_list[pat_index]



    def add_reaction_to_model ( self, name="", rin="", rtype="irreversible", rout="", fwd_rate="0", bkwd_rate="" ):
        """ Add a reaction """
        print ( "Adding Reaction " + rin + " " + rtype + " " + rout )
        self.mcell.cellblender_main_panel.reaction_select = True
        bpy.ops.mcell.reaction_add()
        rxn_index = self.mcell.reactions.active_rxn_index
        self.mcell.reactions.reaction_list[rxn_index].rxn_name = name
        self.mcell.reactions.reaction_list[rxn_index].reactants = rin
        self.mcell.reactions.reaction_list[rxn_index].products = rout
        self.mcell.reactions.reaction_list[rxn_index].type = rtype
        self.mcell.reactions.reaction_list[rxn_index].fwd_rate.set_expr(fwd_rate)
        self.mcell.reactions.reaction_list[rxn_index].bkwd_rate.set_expr(bkwd_rate)
        print ( "Done Adding Reaction " + rin + " " + rtype + " " + rout )
        return self.mcell.reactions.reaction_list[rxn_index]


    def add_count_output_to_model ( self, name=None, mol_name=None, rxn_name=None, object_name=None, region_name=None, count_location="World" ):
        """ Add a reaction output """
        # count_location may be "World", "Object", or "Region"

        self.mcell.cellblender_main_panel.graph_select = True
        bpy.ops.mcell.rxn_output_add()
        rxn_index = self.mcell.rxn_output.active_rxn_output_index
        rxn = self.mcell.rxn_output.rxn_output_list[rxn_index]

        if (mol_name != None) and (rxn_name == None):
            # This is a Molecule Count Output Definition
            print ( "Adding Count Output for Molecule " + mol_name )
            rxn.rxn_or_mol = "Molecule"
        elif (mol_name == None) and (rxn_name != None):
            # This is a Reaction Count Output Definition
            print ( "Adding Count Output for Reaction " + rxn_name )
            rxn.rxn_or_mol = "Reaction"
        else:
            print ( "Warning: Count output should be either Molecule or Reaction ... returning None." )
            return None


        if name == None:
            rxn.name = ""
        else:
            rxn.name = name

        if mol_name == None:
            rxn.molecule_name = ""
        else:
            rxn.molecule_name = mol_name

        if rxn_name == None:
            rxn.reaction_name = ""
        else:
            rxn.reaction_name = rxn_name

        if object_name == None:
            rxn.object_name = ""
        else:
            rxn.object_name = object_name

        if region_name == None:
            rxn.region_name = ""
        else:
            rxn.region_name = region_name

        rxn.count_location = count_location
        print ( "Done Adding Output Count for Molecule/Reaction" )
        return self.mcell.rxn_output.rxn_output_list[rxn_index]


        """
        All names that aren't listed are defaulted to "".
        All count_locations that don't appear are "World" (same as 0).
        count_location enum meaning
          World = 0
          Object = 1
          Region = 2
        rxn_or_mol enum meaning
          Reaction = 0
          Molecule = 1
          
        
        >>> rxo = C.scene.mcell.rxn_output
        >>> rxl = rxo.rxn_output_list
        >>> ### The following output only shows values that differ from defaults (typical Blender behavior)
        >>> for rxi in rxl:
        ...     print (str(rxi.name))
        ...     for item in rxi.items():
        ...         print ( "  " + str(item) )
        ... 
        Count a in World
          ('name', 'Count a in World')
          ('status', '')
          ('molecule_name', 'a')
          ('reaction_name', '')
          ('object_name', '')
          ('region_name', '')
          ('count_location', 0)
          ('rxn_or_mol', 1)
        Count b in World
          ('name', 'Count b in World')
          ('status', '')
          ('molecule_name', 'b')
          ('reaction_name', '')
          ('object_name', '')
          ('region_name', '')
          ('count_location', 0)
          ('rxn_or_mol', 1)
        Count c in World
          ('name', 'Count c in World')
          ('status', '')
          ('molecule_name', 'c')
          ('reaction_name', '')
          ('object_name', '')
          ('region_name', '')
          ('count_location', 0)
          ('rxn_or_mol', 1)
        Count d in World
          ('name', 'Count d in World')
          ('status', '')
          ('molecule_name', 'd')
          ('reaction_name', '')
          ('object_name', '')
          ('region_name', '')
          ('count_location', 0)
          ('rxn_or_mol', 1)
        Count ab_c in World
          ('name', 'Count ab_c in World')
          ('status', '')
          ('rxn_or_mol', 0)
          ('reaction_name', 'ab_c')
        Count at1_at1 in World
          ('name', 'Count at1_at1 in World')
          ('status', '')
          ('rxn_or_mol', 0)
          ('reaction_name', 'at1_at1')
        Count ct1_ct1 in World
          ('name', 'Count ct1_ct1 in World')
          ('status', '')
          ('rxn_or_mol', 0)
          ('reaction_name', 'ct1_ct1')
        Count t1 in/on Organelle_1[top]
          ('name', 'Count t1 in/on Organelle_1[top]')
          ('status', '')
          ('rxn_or_mol', 1)
          ('reaction_name', 'ct2_dt2')
          ('molecule_name', 't1')
          ('count_location', 2)
          ('object_name', 'Organelle_1')
          ('region_name', 'top')
        Count c in/on Organelle_2
          ('name', 'Count c in/on Organelle_2')
          ('status', '')
          ('molecule_name', 'c')
          ('count_location', 1)
          ('object_name', 'Organelle_2')

        >>> 
        """


        """
        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[0].molecule_name = 't'
        mcell.rxn_output.rxn_output_list[0].count_location = 'Object'
        mcell.rxn_output.rxn_output_list[0].object_name = 'ti'
        """


    def set_partitions ( self, include_partitions=True, auto=False, show=False, xs=None, xe=None, xd=None, ys=None, ye=None, yd=None, zs=None, ze=None, zd=None ):

        self.mcell.partitions.include = include_partitions

        if auto:
            bpy.ops.mcell.auto_generate_boundaries()

        if show:
            bpy.ops.mcell.create_partitions_object()
        else:
            bpy.ops.mcell.remove_partitions_object()
        
        if xs != None: self.mcell.partitions.x_start = xs
        if xe != None: self.mcell.partitions.x_end   = xe
        if xd != None: self.mcell.partitions.x_step  = xd
        
        if ys != None: self.mcell.partitions.y_start = ys
        if ye != None: self.mcell.partitions.y_end   = ye
        if yd != None: self.mcell.partitions.y_step  = yd
        
        if zs != None: self.mcell.partitions.z_start = zs
        if ze != None: self.mcell.partitions.z_end   = ze
        if zd != None: self.mcell.partitions.z_step  = zd


    def set_visualization ( self, enable_visualization=True, export_all=True, all_iterations=True, start=0, end=1, step=1 ):
        """ Setting visualization parameters """
        print ( "Setting visualization parameters" )
        self.mcell.cellblender_main_panel.mol_viz_select = True
        self.mcell.mol_viz.mol_viz_enable = enable_visualization
        self.mcell.viz_output.export_all = export_all
        self.mcell.viz_output.all_iterations = all_iterations

        self.mcell.viz_output.start.set_expr ( str(start) )
        self.mcell.viz_output.end.set_expr ( str(end) )
        self.mcell.viz_output.step.set_expr ( str(step) )

        print ( "Done setting visualization parameters" )
        return self.mcell.viz_output


    def add_surface_class_to_model ( self, surf_class_name ):
        """ Add a surface class """
        print ( "Adding Surface class  " + surf_class_name )
        self.mcell.cellblender_main_panel.surf_classes_select = True
        bpy.ops.mcell.surface_class_add()
        surf_index = self.mcell.surface_classes.active_surf_class_index
        self.mcell.surface_classes.surf_class_list[surf_index].name = surf_class_name
        print ( "Done Adding Surface Class " + surf_class_name )
        return self.mcell.surface_classes.surf_class_list[surf_index]


    def add_property_to_surface_class ( self, mol_name, sc_orient=";", sc_type="REFLECTIVE", sc_clamp_val_str='' ):
        """ Add a property to a surface class """
        print ( "Adding Surface class property " + sc_orient + " " + sc_type + " " + sc_clamp_val_str )
        self.mcell.cellblender_main_panel.surf_classes_select = True
        bpy.ops.mcell.surf_class_props_add()
        surf_index = self.mcell.surface_classes.active_surf_class_index
        prop_index = self.mcell.surface_classes.surf_class_list[surf_index].active_surf_class_props_index
        self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].affected_mols = 'SINGLE'
        self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].molecule = mol_name
        self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].surf_class_orient = sc_orient
        self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].surf_class_type = sc_type
        #self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].clamp_value_str = sc_clamp_val_str
        self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index].clamp_value.set_expr ( sc_clamp_val_str )


        print ( "Done Adding Surface Class Property " + sc_orient + " " + sc_type + " " + sc_clamp_val_str )
        return self.mcell.surface_classes.surf_class_list[surf_index].surf_class_props_list[prop_index]


    def assign_surface_class_to_region ( self, surf_class_name, obj_name, reg_name="" ):
        """ Assigning a surface class to a Region """
        print ( "Assigning a surface class to Region " + surf_class_name )
        self.mcell.cellblender_main_panel.surf_regions_select = True
        bpy.ops.mcell.mod_surf_regions_add()
        surf_index = self.mcell.mod_surf_regions.active_mod_surf_regions_index
        self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index].surf_class_name = surf_class_name
        self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index].object_name = obj_name
        if reg_name == 'ALL':
          self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index].region_selection = 'ALL'
        else:
          self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index].region_name = reg_name
          self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index].region_selection = 'SEL'

        print ( "Done Adding Surface Class to Region " + surf_class_name )
        return self.mcell.mod_surf_regions.mod_surf_regions_list[surf_index]


    def add_surface_region_to_model_object_by_normal ( self, obj_name, surf_name, nx=0, ny=0, nz=0, min_dot_prod=0.5 ):

        print ("Selected Object = " + str(self.context.object) )
        # bpy.ops.object.mode_set ( mode="EDIT" )

        # Start in Object mode for selecting
        bpy.ops.object.mode_set ( mode="OBJECT" )

        # Face Select Mode:
        msm = self.context.scene.tool_settings.mesh_select_mode[0:3]
        self.context.scene.tool_settings.mesh_select_mode = (False, False, True)

        # Deselect everything
        bpy.ops.object.select_all ( action='DESELECT')
        c = bpy.data.objects[obj_name]
        c.select = False

        # Select just the top faces (normals up)
        mesh = c.data

        bpy.ops.object.mode_set(mode='OBJECT')
        
        for p in mesh.polygons:
          if (nx == 0) and (ny == 0) and (nz == 0):
            # No normal means add all surfaces
            p.select = True
          else:
            n = p.normal
            dp = (n.x * nx) + (n.y * ny) + (n.z * nz)
            if dp > min_dot_prod:
              # This appears to be a triangle in the top face
              #print ( "Normal " + str (n) + " matches with " + str(dp) )
              p.select = True
            else:
              #print ( "Normal " + str (n) + " differs with " + str(dp) )
              p.select = False

        bpy.ops.object.mode_set(mode='EDIT')

        # Add a new region

        bpy.ops.mcell.region_add()
        bpy.data.objects[obj_name].mcell.regions.region_list[0].name = surf_name

        # Assign the currently selected faces to this region
        bpy.ops.mcell.region_faces_assign()

        # Restore the selection settings
        self.context.scene.tool_settings.mesh_select_mode = msm
        bpy.ops.object.mode_set(mode='OBJECT')


    def add_surface_region_to_model_all_faces ( self, obj_name, surf_name ):
        self.add_surface_region_to_model_object_by_normal ( obj_name, surf_name )


    def all_non_queue_processes_finished ( self ):
        print ( "Checking if all non-queue processes are done..." )
        plist = self.mcell.run_simulation.processes_list
        all_done = False
        if len(plist) <= 0:
            all_done = True
        else:
            all_done = True
            for p in plist:
                # Convert the process list string into a process id
                pid_str = p.name.split(':')[1].split(',')[0].strip()
                print ( "Checking if Process " + pid_str + " is done." )
                if os.path.exists ( "/proc/" + pid_str ):
                    all_done = False
        return all_done


    def all_queue_processes_finished ( self ):
        print ( "Checking if all processes are done..." )
        mcell = self.mcell
        processes_list = mcell.run_simulation.processes_list
        active_index = mcell.run_simulation.active_process_index
        ap = processes_list[active_index]
        pid = int(ap.name.split(',')[0].split(':')[1])
        q_item = cellblender.simulation_queue.task_dict.get(pid)
        if q_item:
            if (q_item['status'] == 'running') or (q_item['status'] == 'queued'):
                return False
        return True


    def wait ( self, wait_time ):
        import time
        app = bpy.context.scene.cellblender_test_suite
        if app.run_with_queue:
            print ( "============== WAITING for QUEUE ==============" )
            while not self.all_queue_processes_finished():
                print ( "============== WAITING for QUEUE to Finish ==============" )
                time.sleep ( 1.0 )
        else:
            if self.all_non_queue_processes_finished():
                print ( "============== ALL DONE ==============" )
            else:
                print ( "============== WAITING for COMMAND ==============" )
            time.sleep ( wait_time )

    def set_sim_seed ( self, seed=1 ):
        # This is a bit tricky since CellBlender won't allow a start seed greater than the end seed
        self.mcell.run_simulation.end_seed.expr = str(seed)
        self.mcell.run_simulation.start_seed.expr = str(seed)
        self.mcell.run_simulation.end_seed.expr = str(seed)


    def export_model ( self, iterations="100", time_step="1e-6", export_format="mcell_mdl_unified", seed=1 ):
        """ export_format is one of: mcell_mdl_unified, mcell_mdl_modular """
        print ( "Test Suite is exporting the model with seed " + str(seed) + " ..." )
        self.mcell.cellblender_main_panel.init_select = True
        self.mcell.initialization.iterations.set_expr(iterations)
        self.mcell.initialization.time_step.set_expr(time_step)
        self.set_sim_seed ( seed )
        self.mcell.export_project.export_format = export_format

        app = bpy.context.scene.cellblender_test_suite
        # Old export operator
        # bpy.ops.mcell.export_project()
        # New export operator
        bpy.ops.mcell.dm_export_mdl()


    def run_only ( self, wait_time=10.0, seed=1 ):
        """ export_format is one of: mcell_mdl_unified, mcell_mdl_modular """
        print ( "Test Suite is running the simulation with seed " + str(seed) + " ..." )
        self.mcell.cellblender_main_panel.init_select = True
        self.set_sim_seed ( seed )

        app = bpy.context.scene.cellblender_test_suite
        if app.run_mcell:
            bpy.ops.mcell.run_simulation()
            for i in range(10):
                self.wait ( wait_time / 10.0 )
                print ( "Test Suite is Waiting for MCell to complete ..." )
            print ( "Test Suite is done waiting!!" )




    def run_model ( self, iterations="100", time_step="1e-6", export_format="mcell_mdl_unified", wait_time=10.0, seed=1 ):
        """ export_format is one of: mcell_mdl_unified, mcell_mdl_modular """
        print ( "Test Suite is exporting the model and running the simulation with seed " + str(seed) + " ..." )
        self.mcell.cellblender_main_panel.init_select = True
        self.mcell.initialization.iterations.set_expr(iterations)
        self.mcell.initialization.time_step.set_expr(time_step)
        self.set_sim_seed ( seed )
        self.mcell.export_project.export_format = export_format

        app = bpy.context.scene.cellblender_test_suite
        if app.run_mcell:
            bpy.ops.mcell.run_simulation()
            for i in range(10):
                self.wait ( wait_time / 10.0 )
                print ( "Test Suite is Waiting for MCell to complete ..." )
            print ( "Test Suite is done waiting!!" )
        else:
            # Old export operator
            # bpy.ops.mcell.export_project()
            # New export operator
            bpy.ops.mcell.dm_export_mdl()


    def refresh_molecules ( self ):
        """ Refresh the display """
        app = bpy.context.scene.cellblender_test_suite
        if app.run_mcell:
            bpy.ops.cbm.refresh_operator()


    def old_change_molecule_display ( self, mol, glyph="Cube", letter="A", scale=1.0, red=-1, green=-1, blue=-1 ):
        app = bpy.context.scene.cellblender_test_suite
        if app.run_mcell:
            #if mol.name == "Molecule":
            #    print ("Name isn't correct")
            #    return
            print ( "Changing Display for Molecule \"" + mol.name + "\" to R="+str(red)+",G="+str(green)+",B="+str(blue) )
            self.mcell.cellblender_main_panel.molecule_select = True
            self.mcell.molecules.show_display = True
            mol.glyph = glyph
            mol.letter = letter
            mol.scale = scale
            if red >= 0: mol.color.r = red
            if green >= 0: mol.color.g = green
            if blue >= 0: mol.color.b = blue

            print ( "Done Changing Display for Molecule \"" + mol.name + "\"" )

    def change_molecule_display ( self, mol, glyph="Cube", letter="A", scale=1.0, emit=0.5, red=-1, green=-1, blue=-1 ):
        print ( "Inside change_molecule_display\n" )

        if mol != None:

            print ( "Changing Display for Molecule \"" + mol.name + "\" to R="+str(red)+",G="+str(green)+",B="+str(blue) )

            app = bpy.context.scene.cellblender_test_suite
            self.mcell.cellblender_main_panel.molecule_select = True
            self.mcell.molecules.show_display = True

            mol.glyph = glyph
            mol.letter = letter
            mol.scale = scale
            mat_name = "mol_" + mol.name + "_mat"
            if mat_name in bpy.data.materials:
                cur_red = bpy.data.materials[mat_name].diffuse_color[0]
                cur_green = bpy.data.materials[mat_name].diffuse_color[1]
                cur_blue = bpy.data.materials[mat_name].diffuse_color[2]
                if red >= 0: cur_red = red
                if green >= 0: cur_green = green
                if blue >= 0: cur_blue = blue
                bpy.data.materials[mat_name].diffuse_color = (cur_red, cur_green, cur_blue)
                bpy.data.materials[mat_name].emit = emit
            print ( "Done Changing Display for Molecule \"" + mol.name + "\"" )

        print ( "Leaving change_molecule_display\n" )


    def set_mol_material ( self, mol_name, red=-1, green=-1, blue=-1 ):
        app = bpy.context.scene.cellblender_test_suite
        self.mcell.cellblender_main_panel.molecule_select = True
        self.mcell.molecules.show_display = True

        if red < 0: red = random.random()
        if green < 0: green = random.random()
        if blue < 0: blue = random.random()
        # print ( "Changing Material for Molecule \"" + mol_name + "\" to R="+str(red)+",G="+str(green)+",B="+str(blue) )
        mat_name = "mol_" + mol_name + "_mat"
        if mat_name in bpy.data.materials:
            bpy.data.materials[mat_name].diffuse_color = (red, green, blue)

        # print ( "Done Changing Material for Molecule \"" + mol_name + "\"" )

    def get_mdl_file_path ( self ):
        return self.path_to_blend[:self.path_to_blend.rfind('.')] + "_files" + os.sep + "mcell" + os.sep + "output_data"

    def get_main_mdl_file_path ( self ):
        return self.get_mdl_file_path() + os.sep + "Scene.main.mdl"

    def get_subfiles_from_mdl_file ( self, parent_file ):
        """ Find the list of included files and dynamic geometry referenced files """
        # Note that this is not currently recursive ... in other words it only checks files included in the top level file
        # While this function does return the dynamic geometry list file, it does not return the files contained in that list
        # Since the only dynamic geometry being tested was created by the test suite, checking those files would not be testing CellBlender.
        # The same is true of the dynamic geometry list file, but it's being included anyway ... since it's just one file.
        subfiles = []
        main_mdl_lines = open(parent_file,'rb').readlines()
        for l in main_mdl_lines:
          l = l.decode().strip()
          if (l.startswith('INCLUDE_FILE = "')) or (l.startswith('DYNAMIC_GEOMETRY = "')):
            l = l[l.index('"')+1:]
            l = l[:l.index('"')]
            subfiles.append ( l )
        return subfiles

    def compare_mdl_with_sha1 ( self, good_hash="", test_name=None ):
        """ Compute the sha1 for the main MDL file and included MDL files and compare with good_hash """
        app = bpy.context.scene.cellblender_test_suite
        
        file_name = self.get_main_mdl_file_path()

        if test_name == None:
            test_name = "Test"

        hashobject = hashlib.sha1()
        if os.path.isfile(file_name):
            hashobject.update(open(file_name, 'rb').read())
            print ( "Computed hash for " + file_name + " = " + str(hashobject.hexdigest()) )
            path = file_name[0:file_name.rfind(os.sep)]
            for f in self.get_subfiles_from_mdl_file(file_name):
                hashobject.update(open(path+os.sep+f, 'rb').read())
                print ( "    plus hash for " + path+os.sep+f + " = " + str(hashobject.hexdigest()) )

            file_hash = str(hashobject.hexdigest())
            print("  SHA1 = " + file_hash + " for \n     " + file_name )

            if len(good_hash) <= 0:

                print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                print ( "%% " + test_name + "   W A R N I N G :  No Hash value provided. Hash from '" + file_name + "' is " + file_hash )
                print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                app.test_status = "F"

            else:

                if file_hash == good_hash:
                    print ( "\n##############################################################################################################" )
                    print ( "##############################################################################################################" )
                    print ( "## " + test_name )
                    print ( "##    O K :  Test Expected " + good_hash + " - confirmed." )
                    print ( "##############################################################################################################" )
                    print ( "##############################################################################################################\n" )
                    app.test_status = "P"

                else:
                    print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                    print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                    print ( "%% " + test_name + "   E R R O R :  Test Expected " + good_hash + ", but got " + file_hash )
                    print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                    print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
                    app.test_status = "F"

                    if app.exit_on_error:
                        bpy.ops.wm.quit_blender()
                    if app.update_soure_file and (len(app.source_file_to_update) > 0):
                        print ( "Updating source file to change " + good_hash + " into " + file_hash )
                        f = open ( app.source_file_to_update, mode='r' )
                        fstring = f.read()
                        f.close()
                        new_string = fstring.replace ( good_hash, file_hash )
                        f = open ( app.source_file_to_update, mode='w' )
                        f.write(new_string)
                        f.close()

        else:

            print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
            print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
            print ( "%% " + test_name + "   E R R O R :  File '%s' does not exist" % file_name )
            print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
            print ( "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" )
            app.test_status = "F"
            if app.exit_on_error:
                bpy.ops.wm.quit_blender() 


    """
    def get_3d_view_areas(self):
        areas_3d = []
        for area in self.context.screen.areas:
            if area.type == 'VIEW_3D':
                areas_3d = areas_3d + [area]
                # area.spaces.active.show_manipulator = False
        return areas_3d
    """

    def get_3d_view_spaces(self):
        spaces_3d = []
        for area in self.context.screen.areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    spaces_3d = spaces_3d + [space]
                    # area.spaces.active.show_manipulator = False
        return spaces_3d



    def scale_view_distance ( self, scale ):
        """ Change the view distance for all 3D_VIEW windows """
        spaces = self.get_3d_view_spaces()
        for space in spaces:
            space.region_3d.view_distance *= scale
        #bpy.ops.view3d.zoom(delta=3)
        #set_view_3d()


    def set_axis_angle ( self, axis, angle ):
        """ Change the view axis and angle for all 3D_VIEW windows """
        spaces = self.get_3d_view_spaces()
        for space in spaces:
            space.region_3d.view_rotation.axis = mathutils.Vector(axis)
            space.region_3d.view_rotation.angle = angle
        #set_view_3d()


    def hide_manipulator ( self, hide=True ):
        # C.screen.areas[4].spaces[0].show_manipulator = False
        spaces = self.get_3d_view_spaces()
        for space in spaces:
            space.show_manipulator = not hide


    def switch_to_perspective ( self ):
        """ Change to perspective for all 3D_VIEW windows """
        spaces = self.get_3d_view_spaces()
        for space in spaces:
            space.region_3d.view_perspective = 'PERSP'

    def switch_to_orthographic ( self ):
        """ Change to orthographic for all 3D_VIEW windows """
        spaces = self.get_3d_view_spaces()
        for space in spaces:
            space.region_3d.view_perspective = 'ORTHO'

    def play_animation ( self ):
        """ Play the animation """
        app = bpy.context.scene.cellblender_test_suite
        if app.run_mcell:
            bpy.ops.screen.animation_play()


######################
#   Model  Support   #
######################

class point:
  x=0;
  y=0;
  z=0;

  def __init__ ( self, x, y, z ):
    self.x = x;
    self.y = y;
    self.z = z;
  
  def equals ( self, p ):
    if ( (self.x == p.x) and (self.y == p.y) and (self.z == p.z) ):
      return ( True );
    else:
      return ( False );

  def equals ( self, p ):
    return (self == p )

  def toList ( self ):
    return ( [ self.x, self.y, self.z ] );

  def toString ( self ):
    return ( "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")" );


class face:
  verts = [];
  
  def __init__ ( self, v1, v2, v3 ):
    self.verts = [];
    self.verts.append ( v1 );
    self.verts.append ( v2 );
    self.verts.append ( v3 );
  
  def toString( self ):
    return ( "[" + str(verts[0]) + "," + str(verts[1]) + "," + str(verts[2]) + "]" );


class line:
  p1 = point(0,0,0);
  p2 = point(0,0,0);

  def __init__ ( self, p1, p2 ):
    self.p1 = p1;
    self.p2 = p2;
  
  def toString( self ):
    return ( "["+str(p1.x)+","+str(p1.y)+","+str(p1.z)+"]-["+str(p2.x)+","+str(p2.y)+","+str(p2.z)+"]" );


import array
import traceback


class plf_object:

  # An object that can hold points, lines, and faces (only points and faces are currently implemented)

  points = []
  faces = []
  
  def __init__ ( self ):
    self.points = []
    self.faces = []
  
  def add_point ( self, p ):
    self.points.append ( p );

  def add_face ( self, f ):
    self.faces.append ( f );

  def offset_points ( self, dx, dy, dz ):
    for p in self.points:
      p.x += dx;
      p.y += dy;
      p.z += dz;

  def scale_points ( self, sx, sy, sz ):
    for p in self.points:
      p.x *= sx;
      p.y *= sy;
      p.z *= sz;

  def dither_points ( self, sigma_x, sigma_y, sigma_z ):
    g = random.gauss
    for p in self.points:
      p.x += g(0,sigma_x);
      p.y += g(0,sigma_y);
      p.z += g(0,sigma_z);

  def sqr ( self, v ):
    return ( v * v );

  def dump_as_plf ( self, file_name=None ):
    if file_name != None:
      out_file = open ( file_name, "w" )

    for p in self.points:
      if file_name == None:
        print ( "P " + str(p.x) + " " + str(p.y) + " " + str(p.z) );
      else:
        out_file.write ( "P " + str(p.x) + " " + str(p.y) + " " + str(p.z) + "\n" );

    for f in self.faces:
      for edge in range(3):
        p1i = f.verts[edge];
        p2i = f.verts[(edge+1)%3];
        if file_name == None:
          print  ( "L " + str(p1i) + " " + str(p2i) );
        else:
          out_file.write  ( "L " + str(p1i) + " " + str(p2i) + "\n" );

    for f in self.faces:
      s = "F"
      for edge in f.verts:
        s += " " + str(edge)
      if file_name == None:
        print ( s )
      else:
        out_file.write ( s + "\n" )

    if file_name != None:
      out_file.close()


  def get_average_edge_length ( self ):
    len_sum = 0;
    num_summed = 0;
    for f in self.faces:
      for edge in range(3):
        p1i = f.verts[edge];
        p2i = f.verts[(edge+1)%3];
        p1 = self.points[p1i];
        p2 = self.points[p2i];
        len_sum += math.sqrt ( self.sqr(p1.x-p2.x) + self.sqr(p1.y-p2.y) + self.sqr(p1.z-p2.z) );
        num_summed += 1;
    # Handle the case where there are faces
    if num_summed == 0: num_summed = 1
    return ( len_sum / num_summed );


  def merge ( self, obj_to_add ):
    # Loop through all faces of the new object to be merged
    for oa_face in obj_to_add.faces:
      # Find point indexes that match in the target object or add them
      new_verts = [ -1, -1, -1 ];
      for new_vert_index in range(3):
        # Loop through all existing points in the target object looking for a match
        looking_for = None
        looking_for = obj_to_add.points[oa_face.verts[new_vert_index]]
        found = -1
        for p in self.points:
          if (p.x == looking_for.x) and (p.y == looking_for.y) and (p.z == looking_for.z):
            found = self.points.index(p)
            break
        if found >= 0:
          new_verts[new_vert_index] = found
        if (new_verts[new_vert_index] < 0):
          # The point was not found in the target object, so add it
          new_p = point ( looking_for.x, looking_for.y, looking_for.z );
          self.points.append ( new_p );
          new_verts[new_vert_index] = self.points.index(new_p);

      new_f = face(new_verts[0], new_verts[1], new_verts[2]);
      self.faces.append ( new_f );

  def remove_point_by_index ( self, index ):
    # Start by removing all faces using this index
    n = len(self.faces)-1
    face_index = n;
    while face_index >= 0:
      f = self.faces[face_index]
      remove = False
      for point_index in range(3):
        if (f.verts[point_index] == index):
          remove = True;
          break;
      if (remove):
        self.faces.pop( face_index );
      face_index += -1

    # Renumber all point indices greater than the index to be removed
    for f in self.faces:
      for point_index in range(3):
        if (f.verts[point_index] > index):
          f.verts[point_index] += -1;

    # Now remove the point itself
    self.points.pop ( index );


  def remove_all_with_z_gt ( self, z ):
    self.remove_all_with_z ( z, True );

  def remove_all_with_z_lt ( self, z ):
    self.remove_all_with_z ( z, False );

  def remove_all_with_z ( self, z, gt ):
    n = len(self.points)-1;
    point_index = n
    while point_index >= 0:
      p = self.points[point_index];
      remove = False;
      if (gt):
        if (p.z > z):
          remove = True;
      else:
        if (p.z < z):
          remove = True;
      if (remove):
        self.remove_point_by_index ( point_index ); # This removes faces as well
      point_index += -1

  def get_all_with_z_at ( self, z, tolerance ):
    result_list = []
    for point_index in range(len(self.points)):
      p = self.points[point_index];
      if ( (p.z >= z-tolerance) and (p.z <= z+tolerance) ):
        result_list.append ( point_index );
    result = None
    if len(result_list) > 0:
      result = []
      for i in range(len(result_list)):
        result.append ( result_list[i] );
    return ( result );



  def write_as_binary_geometry ( self, object_name, file_name=None, ):
    print ( "Saving binary geometry file " + file_name )
    try:
      geo_file = open ( file_name, "wb" )

      array.array ( 'B', [1] ).tofile(geo_file)                 # Version number of this file

      array.array ( 'i', [1] ).tofile(geo_file)                 # Number of Objects, -1 implies whatever is in the file

      # Write out an object
      array.array ( 'B', [2] ).tofile(geo_file)                 # 2 = Code for a polygon list
      array.array ( 'I', [len(object_name)] ).tofile(geo_file)  # Length of Object Name
      a = array.array ( 'B' )                                   # Object Name
      a.frombytes ( object_name.encode() )                      # Object Name
      a.tofile(geo_file)                                        # Object Name
      array.array ( 'I', [0] ).tofile(geo_file)                 # Number of Transforms

      array.array ( 'I', [len(self.points)] ).tofile(geo_file)  # Number of points (verts)
      for p in self.points:
        array.array ( 'd', p.toList() ).tofile(geo_file)        # Each point (x,y,z) as double
      array.array ( 'I', [len(self.faces)] ).tofile(geo_file)   # Number of faces (polygons)
      for f in self.faces:
        array.array ( 'I', f.verts ).tofile(geo_file)           # Each face is a list of integers
      array.array ( 'I', [0] ).tofile(geo_file)                 # Number of Regions

      geo_file.close()

    except IOError:
      print(("\n***** IOError: File: %s\n") % (file_name))

    except ValueError:
      print(("\n***** ValueError: Invalid data in file: %s\n") % (file_name))

    except RuntimeError as rte:
      print(("\n***** RuntimeError writing file: %s\n") % (file_name))
      print("      str(error): \n" + str(rte) + "\n")
      fail_error = sys.exc_info()
      print ( "    Error Type: " + str(fail_error[0]) )
      print ( "    Error Value: " + str(fail_error[1]) )
      tb = fail_error[2]
      # tb.print_stack()
      print ( "=== Traceback Start ===" )
      traceback.print_tb(tb)
      print ( "=== Traceback End ===" )

    except Exception as uex:
      # Catch any exception
      print ( "\n***** Unexpected exception:" + str(uex) + "\n" )
      raise


  def read_from_binary_geometry ( self, file_name ):
    # print ( "Reading binary geometry file " + file_name )
    try:
      geo_file = open ( file_name, "rb" )

      a = array.array ( 'B' )
      a.fromfile(geo_file, 1)                                   # Version number of this file

      if a[0] != 1:
        raise ValueError ( 'File \'%s\' does not begin with Version=1' % file_name )

      a = array.array ( 'i' )
      a.fromfile(geo_file, 1)                                   # Number of Objects, -1 implies whatever is in the file

      if a[0] != 1:
        raise ValueError ( 'File \'%s\' does not contain just one object' % file_name )

      a = array.array ( 'B' )
      a.fromfile(geo_file, 1)                                   # Code for this object (should be 2)

      if a[0] != 2:
        raise ValueError ( 'File \'%s\' does not contain a POLYGON LIST object' % file_name )

      a = array.array ( 'I' )
      a.fromfile(geo_file, 1)
      name_len = a[0]
      a = array.array ( 'B' )
      a.fromfile(geo_file, name_len)
      obj_name = a.tostring().decode()

      a = array.array ( 'I' )
      a.fromfile(geo_file, 1)                                   # Number of Transforms

      if a[0] != 0:
        raise ValueError ( 'File \'%s\' contains transforms which are not supported' % file_name )

      a = array.array ( 'I' )
      a.fromfile(geo_file, 1)                                   # Number of verts

      num_verts = a[0]

      v = array.array ( 'd' )
      v.fromfile(geo_file, 3*num_verts)                         # All verts


      a = array.array ( 'I' )
      a.fromfile(geo_file, 1)                                   # Number of faces

      num_faces = a[0]

      f = array.array ( 'I' )
      f.fromfile(geo_file, 3*num_faces)                         # All faces

      a = array.array ( 'I' )
      a.fromfile(geo_file, 1)                                   # Number of Regions

      if a[0] != 0:
        raise ValueError ( 'File \'%s\' contains regions which are not supported' % file_name )

      geo_file.close()

      # Convert from arrays to lists inside this plf object

      self.points = []
      while len(v) > 0:
        self.points.append ( point ( v.pop(0), v.pop(0), v.pop(0) ) )

      """ This worked but was slow - Merging isn't needed when the faces already refer to the points in a list
      self.faces = []
      while len(f) > 0:
        new_face = plf_object();
        new_face.add_point ( self.points[f.pop(0)] );
        new_face.add_point ( self.points[f.pop(0)] );
        new_face.add_point ( self.points[f.pop(0)] );
        new_face.add_face ( face (0, 1, 2) );
        self.merge ( new_face );
      """

      self.faces = []
      while len(f) > 0:
        self.faces.append ( face ( f.pop(0), f.pop(0), f.pop(0) ) )




    except IOError:
      print(("\n***** IOError: File: %s\n") % (file_name))

    except ValueError:
      print(("\n***** ValueError: Invalid data in file: %s\n") % (file_name))

    except RuntimeError as rte:
      print(("\n***** RuntimeError writing file: %s\n") % (file_name))
      print("      str(error): \n" + str(rte) + "\n")
      fail_error = sys.exc_info()
      print ( "    Error Type: " + str(fail_error[0]) )
      print ( "    Error Value: " + str(fail_error[1]) )
      tb = fail_error[2]
      # tb.print_stack()
      print ( "=== Traceback Start ===" )
      traceback.print_tb(tb)
      print ( "=== Traceback End ===" )

    except Exception as uex:
      # Catch any exception
      print ( "\n***** Unexpected exception:" + str(uex) + "\n" )
      raise



  def write_as_mdl ( self, object_name, file_name=None, partitions=False, instantiate=False ):
    if file_name != None:
      out_file = open ( file_name, "w" )
      if partitions:
          out_file.write ( "PARTITION_X = [[-2.0 TO 2.0 STEP 0.5]]\n" )
          out_file.write ( "PARTITION_Y = [[-2.0 TO 2.0 STEP 0.5]]\n" )
          out_file.write ( "PARTITION_Z = [[-2.0 TO 2.0 STEP 0.5]]\n" )
          out_file.write ( "\n" )
      out_file.write ( object_name + " POLYGON_LIST\n" )
      out_file.write ( "{\n" )
      out_file.write ( "  VERTEX_LIST\n" )
      out_file.write ( "  {\n" )
      for p in self.points:
          out_file.write ( "    [ " + str(p.x) + ", " + str(p.y) + ", " + str(p.z) + " ]\n" );
      out_file.write ( "  }\n" )
      out_file.write ( "  ELEMENT_CONNECTIONS\n" )
      out_file.write ( "  {\n" )
      for f in self.faces:
          s = "    [ " + str(f.verts[0]) + ", " + str(f.verts[1]) + ", " + str(f.verts[2]) + " ]\n"
          out_file.write ( s );
      out_file.write ( "  }\n" )
      out_file.write ( "}\n" )
      if instantiate:
          out_file.write ( "\n" )
          out_file.write ( "INSTANTIATE Scene OBJECT {\n" )
          out_file.write ( "  " + object_name + " OBJECT " + object_name + " {}\n" )
          out_file.write ( "}\n" )
      out_file.close()


  def read_from_regularized_mdl ( self, file_name=None, partitions=False, instantiate=False ):

    # This function makes some assumptions about the format of the geometry in an MDL file

    self.points = []
    self.faces = []

    if file_name == None:
      # Generate an easy tetrahedron for testing
      self.add_point ( point(0,0,0) )
      self.add_point ( point(0,0,1) )
      self.add_point ( point(0,1,0) )
      self.add_point ( point(1,0,0) )
      self.add_face ( face ( 0, 1, 2 ) )
      self.add_face ( face ( 0, 1, 3 ) )
      self.add_face ( face ( 0, 2, 3 ) )
      self.add_face ( face ( 1, 2, 3 ) )

    if file_name != None:
      try:
        f = open ( file_name, 'r' )
        lines = f.readlines();

        mode = ""

        for line in lines:
          l = line.strip()

          if l == "VERTEX_LIST":
            mode = 'v'
          elif l == "ELEMENT_CONNECTIONS":
            mode = 'f'
          elif l == "}":
            mode = ""

          if (len(l)>1):
            if (l[0] == '[') and (l[-1] == ']'):
              # This is list
              v = l[1:-1].replace(',',' ').split()

              if mode == 'v':
                # This is a vertex
                self.add_point ( point ( float(v[0]), float(v[1]), float(v[2]) ) )
              elif mode == 'f':
                # This is a face
                self.add_face ( face ( int(v[0]), int(v[1]), int(v[2]) ) )
        f.close()
      except FileNotFoundError as ioe:
          # User has probably dragged off the time line, just ignore it
          pass
      except Exception as e:
          print ( "Exception reading MDL: " + str(e) )
      except:
          print ( "Unknown Exception" )



class BasicBox (plf_object):

  def __init__ ( self, size_x=1.0, size_y=1.0, size_z=1.0, x_subs=3, y_subs=3, z_subs=3 ):

    # Create a box of the requested size

    self.points = [];
    self.faces = [];

    self.points = self.points + [ point (  size_x,  size_y, -size_z ) ]
    self.points = self.points + [ point (  size_x, -size_y, -size_z ) ]
    self.points = self.points + [ point ( -size_x, -size_y, -size_z ) ]
    self.points = self.points + [ point ( -size_x,  size_y, -size_z ) ]
    self.points = self.points + [ point (  size_x,  size_y,  size_z ) ]
    self.points = self.points + [ point (  size_x, -size_y,  size_z ) ]
    self.points = self.points + [ point ( -size_x, -size_y,  size_z ) ]
    self.points = self.points + [ point ( -size_x,  size_y,  size_z ) ]

    face_list = [ [ 1, 2, 3 ], [ 7, 6, 5 ], [ 4, 5, 1 ], [ 5, 6, 2 ],
                  [ 2, 6, 7 ], [ 0, 3, 7 ], [ 0, 1, 3 ], [ 4, 7, 5 ],
                  [ 0, 4, 1 ], [ 1, 5, 2 ], [ 3, 2, 7 ], [ 4, 0, 7 ] ]

    """ This worked but was slow - Merging isn't needed when the faces already refer to the points in a list
    for f in face_list:
      new_face = plf_object();
      new_face.add_point ( self.points[f[0]] );
      new_face.add_point ( self.points[f[1]] );
      new_face.add_point ( self.points[f[2]] );
      new_face.add_face ( face (0, 1, 2) );
      self.merge ( new_face );
    """

    for f in face_list:
      self.faces.append ( face ( f[0], f[1], f[2] ) )




class BasicBox_Subdiv (plf_object):

  def __init__ ( self, size_x=1.0, size_y=1.0, size_z=1.0, x_subs=3, y_subs=3, z_subs=3 ):

    # Create a unit box first then resize it later

    xcoords = [ (2*(x-(x_subs/2.0))/x_subs) for x in range(0,x_subs+1) ]
    ycoords = [ (2*(y-(y_subs/2.0))/y_subs) for y in range(0,y_subs+1) ]
    zcoords = [ (2*(z-(z_subs/2.0))/z_subs) for z in range(0,z_subs+1) ]

    # Create the top and bottom faces using integer coordinates

    faces_index_list = []

    # Make the bottom and top (along z)
    for x in range(x_subs):
      for y in range(y_subs):
        vertex_0_00 = [x+0,y+0,0]
        vertex_0_01 = [x+1,y+0,0]
        vertex_0_10 = [x+0,y+1,0]
        vertex_0_11 = [x+1,y+1,0]
        faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_01] )
        faces_index_list.append ( [vertex_0_00, vertex_0_10, vertex_0_11] )
        vertex_1_00 = [x+0,y+0,z_subs]
        vertex_1_01 = [x+1,y+0,z_subs]
        vertex_1_10 = [x+0,y+1,z_subs]
        vertex_1_11 = [x+1,y+1,z_subs]
        faces_index_list.append ( [vertex_1_00, vertex_1_01, vertex_1_11] )
        faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_10] )

    # Make the right and left (along y)
    for x in range(x_subs):
      for z in range(z_subs):
        vertex_0_00 = [x+0,0,z+0]
        vertex_0_01 = [x+1,0,z+0]
        vertex_0_10 = [x+0,0,z+1]
        vertex_0_11 = [x+1,0,z+1]
        faces_index_list.append ( [vertex_0_00, vertex_0_01, vertex_0_11] )
        faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_10] )
        vertex_1_00 = [x+0,y_subs,z+0]
        vertex_1_01 = [x+1,y_subs,z+0]
        vertex_1_10 = [x+0,y_subs,z+1]
        vertex_1_11 = [x+1,y_subs,z+1]
        faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_01] )
        faces_index_list.append ( [vertex_1_00, vertex_1_10, vertex_1_11] )

    # Make the back and front (along x)
    for y in range(y_subs):
      for z in range(z_subs):
        vertex_0_00 = [0,y+0,z+0]
        vertex_0_01 = [0,y+1,z+0]
        vertex_0_10 = [0,y+0,z+1]
        vertex_0_11 = [0,y+1,z+1]
        faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_01] )
        faces_index_list.append ( [vertex_0_00, vertex_0_10, vertex_0_11] )
        vertex_1_00 = [x_subs,y+0,z+0]
        vertex_1_01 = [x_subs,y+1,z+0]
        vertex_1_10 = [x_subs,y+0,z+1]
        vertex_1_11 = [x_subs,y+1,z+1]
        faces_index_list.append ( [vertex_1_00, vertex_1_01, vertex_1_11] )
        faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_10] )

    # Create the points list and faces list
    faces = []
    point_inds = []

    # First build the faces and the list of points with integer coordinates
    for fi in faces_index_list:
      f = []
      for pi in fi:
        if not (pi in point_inds):
          point_inds.append(pi)
        f.append ( point_inds.index(pi) )
      faces.append ( f )

    # Next build the points list from the points index list (one-for-one to match the faces indicies)
    points = []
    for pi in point_inds:
      points.append ( [ size_x*xcoords[pi[0]], size_y*ycoords[pi[1]], size_z*zcoords[pi[2]] ] )

    # Finally build the PLF structures from these lists

    self.points = [];
    self.faces = [];

    for p in points:
      self.points.append ( point ( p[0], p[1], p[2] ) )

    """ This worked but was slow - Merging isn't needed when the faces already refer to the points in a list
    for f in faces:
      new_face = plf_object();
      new_face.add_point ( self.points[f[0]] );
      new_face.add_point ( self.points[f[1]] );
      new_face.add_point ( self.points[f[2]] );
      new_face.add_face ( face (0, 1, 2) );
      self.merge ( new_face );
    """

    for f in faces:
      self.faces.append ( face ( f[0], f[1], f[2] ) )







class IcoSphere ( plf_object ):

  # Subclass of plf_object that builds an icosphere with recursion

  def add_normalized_vertex ( self, p ):
    # Normalize the point
    # Add to the list of points if it's not already in the list
    # Return an index to the new or existing point in the list

    l = math.sqrt ( (p.x * p.x) + (p.y * p.y) + (p.z * p.z) );
    pnorm = point ( p.x/l, p.y/l, p.z/l );

    # Check if it's already there
    index = -1;
    for pt in self.points:
      if (pt.x == pnorm.x) and (pt.y == pnorm.y) and (pt.z == pnorm.z):
        index = self.points.index(pt)
        break;

    if (index < 0):
      self.points.append ( pnorm );
      index = self.points.index ( pnorm );
      #print ( "Added vertex at " + str(index) );
    #else:
    #  print ( "Found vertex at " + str(index) );
    return (index);


  def __init__ ( self, recursion_level, scale_x=1.0, scale_y=1.0, scale_z=1.0 ):

    self.points = [];

    t = (1.0 + math.sqrt(5.0)) / 2.0;  # Approx 1.618033988749895
    
    # Create 12 verticies from the 3 perpendicular planes whose corners define an icosahedron

    self.add_normalized_vertex ( point (-1,  t,  0) );
    self.add_normalized_vertex ( point ( 1,  t,  0) );
    self.add_normalized_vertex ( point (-1, -t,  0) );
    self.add_normalized_vertex ( point ( 1, -t,  0) );

    self.add_normalized_vertex ( point ( 0, -1,  t) );
    self.add_normalized_vertex ( point ( 0,  1,  t) );
    self.add_normalized_vertex ( point ( 0, -1, -t) );
    self.add_normalized_vertex ( point ( 0,  1, -t) );

    self.add_normalized_vertex ( point ( t,  0, -1) );
    self.add_normalized_vertex ( point ( t,  0,  1) );
    self.add_normalized_vertex ( point (-t,  0, -1) );
    self.add_normalized_vertex ( point (-t,  0,  1) );
    
    
    # Rotate all points such that the resulting icosphere will be separable at the equator
    
    if (True):
      # A PI/6 rotation about z (transform x and y) gives an approximate equator in x-y plane
      angle = (math.pi / 2) - math.atan(1/t);
      # print ( "Rotating with angle = " + str(180 * angle / math.pi) );
      for p in self.points:
        newx = (math.cos(angle) * p.x) - (math.sin(angle) * p.z);
        newz = (math.sin(angle) * p.x) + (math.cos(angle) * p.z);
        p.x = newx;
        p.z = newz;

    # Build the original 20 faces for the Icosphere

    self.faces = []

    # Add 5 faces around point 0 (top)
    self.faces.append ( face (  0, 11,  5 ) );    
    self.faces.append ( face (  0,  5,  1 ) );    
    self.faces.append ( face (  0,  1,  7 ) );    
    self.faces.append ( face (  0,  7, 10 ) );    
    self.faces.append ( face (  0, 10, 11 ) );    

    # Add 5 faces adjacent faces
    self.faces.append ( face (  1,  5,  9 ) );    
    self.faces.append ( face (  5, 11,  4 ) );    
    self.faces.append ( face ( 11, 10,  2 ) );    
    self.faces.append ( face ( 10,  7,  6 ) );    
    self.faces.append ( face (  7,  1,  8 ) );    

    # Add 5 faces around point 3 (bottom)
    self.faces.append ( face (  3,  9,  4 ) );    
    self.faces.append ( face (  3,  4,  2 ) );    
    self.faces.append ( face (  3,  2,  6 ) );    
    self.faces.append ( face (  3,  6,  8 ) );    
    self.faces.append ( face (  3,  8,  9 ) );    

    # Add 5 faces adjacent faces
    self.faces.append ( face (  4,  9,  5 ) );    
    self.faces.append ( face (  2,  4, 11 ) );    
    self.faces.append ( face (  6,  2, 10 ) );    
    self.faces.append ( face (  8,  6,  7 ) );    
    self.faces.append ( face (  9,  8,  1 ) );
    

    # Subdivide the faces as requested by the recursion_level argument
    old_points = None;
    old_faces = None;
    
    for rlevel in range(recursion_level):
      # System.out.println ( "\nRecursion Level = " + rlevel );
      # Save the old points and faces and build a new set for this recursion level
      old_points = self.points;
      old_faces = self.faces;
      self.points = []
      self.faces = []
      for f in old_faces:
        # Split this face into 4 more faces
        midpoint = point(0,0,0)
        potential_new_points = []
        for i in range(6):
          potential_new_points.append ( point(0,0,0) )
        for side in range(3):
          p1 = old_points[f.verts[side]];
          p2 = old_points[f.verts[(side+1)%3]];
          midpoint = point ( ((p1.x+p2.x)/2), ((p1.y+p2.y)/2), ((p1.z+p2.z)/2) );
          potential_new_points[2*side] = p1;
          potential_new_points[(2*side)+1] = midpoint;
        # Add the 4 new faces
        # Start with the verticies ... add them all since add_normalized_vertex() will remove duplicates
        vertex_indicies = []
        for i in range(6):
          vertex_indicies.append ( 0 )
        for i in range(6):
          vertex_indicies[i] = self.add_normalized_vertex ( potential_new_points[i] );
        # Now add the 4 new faces
        self.faces.append ( face ( vertex_indicies[0], vertex_indicies[1], vertex_indicies[5] ) );
        self.faces.append ( face ( vertex_indicies[1], vertex_indicies[2], vertex_indicies[3] ) );
        self.faces.append ( face ( vertex_indicies[3], vertex_indicies[4], vertex_indicies[5] ) );
        self.faces.append ( face ( vertex_indicies[1], vertex_indicies[3], vertex_indicies[5] ) );

    for pt in self.points:
      pt.x *= scale_x
      pt.y *= scale_y
      pt.z *= scale_z




class Capsule (plf_object):

  def sort_ring_indicies ( self, ring ):
    for i in range(len(ring)):
      for j in range(i+1,len(ring)):
        pi = self.points[ring[i]];
        pj = self.points[ring[j]];
        itheta = math.atan2(pi.x, pi.y);
        jtheta = math.atan2(pj.x, pj.y);
        if (jtheta < itheta):
          temp = ring[i];
          ring[i] = ring[j];
          ring[j] = temp;


  def __init__ ( self, recursion_level, radius, height, subdivide_sides=True ):

    self.points = [];
    self.faces = []

    h = height/2; # h is the height of each half
    tol = 0.0001;

    # Make half of an icosphere for the bottom (start with the whole icosphere and remove the top half)
    ico = IcoSphere ( recursion_level );
    ico.remove_all_with_z_gt ( tol );
    ico.scale_points ( radius, radius, radius )
    ico.offset_points ( 0, 0, -h );
    self.merge ( ico );

    # Make half of an icosphere for the top (start with the whole icosphere and remove the bottom half)
    ico = IcoSphere ( recursion_level );
    ico.remove_all_with_z_lt ( -tol );
    ico.scale_points ( radius, radius, radius )
    ico.offset_points ( 0, 0, h );
    self.merge ( ico );
    
    # Get the bottom and top rings to make the side faces
    bot_ring = self.get_all_with_z_at(-h, tol);
    top_ring = self.get_all_with_z_at(h, tol);

    # Make the sides
    if ((bot_ring==None) or (top_ring==None)):
      print ( "Error: one of the rings is null" );
    elif (len(bot_ring) != len(top_ring)):
      print ( "Error: rings are not the same length" );
    elif (h <= 0):
      print ( "Note: no height to make the cylinder" );
    else:
      self.sort_ring_indicies ( bot_ring );
      self.sort_ring_indicies ( top_ring );
      
      if not subdivide_sides:

        # Create a single face with only two triangles for each face of the cylinder

        n = len(bot_ring)

        # Loop around the circumference of the cylinder
        for i in range(n):

          # Get the corner points of the entire face from top to bottom
          cb1 = self.points[bot_ring[i]];
          ct1 = self.points[top_ring[i]];
          cb2 = self.points[bot_ring[(i+1)%n]];
          ct2 = self.points[top_ring[(i+1)%n]];

          # Make two triangular faces for this full-length rectangle

          new_face = plf_object();
          new_face.add_point ( cb1 );
          new_face.add_point ( ct1 );
          new_face.add_point ( cb2 );
          new_face.add_face ( face (0, 1, 2) );
          self.merge ( new_face );

          new_face = plf_object();
          new_face.add_point ( ct1 );
          new_face.add_point ( ct2 );
          new_face.add_point ( cb2 );
          new_face.add_face ( face (0, 1, 2) );
          self.merge ( new_face );

      else:

        # Segment the cylinder along its length to create roughly square (but triangulated) segments

        avg_len = self.get_average_edge_length();
        num_segs = int(math.floor(((2*h)+(avg_len/2)) / avg_len));
        if (num_segs <= 0):
          num_segs = 1;
        
        # Loop through each ring segment from bottom to top
        for seg_num in range(num_segs):

          n = len(bot_ring)

          # Loop around the circumference of the cylinder
          for i in range(n):

            # Get the corner points of the entire face from top to bottom
            cb1 = self.points[bot_ring[i]];
            ct1 = self.points[top_ring[i]];
            cb2 = self.points[bot_ring[(i+1)%n]];
            ct2 = self.points[top_ring[(i+1)%n]];
            
            # print ( "Corners: " + str(cb1.x) + "," + str(ct1.x) + "," + str(cb2.x) + "," + str(ct2.x) )

            # Start out assuming they fill to all 4 corners
            pb1 = point (cb1.x, cb1.y, cb1.z);
            pt1 = point (ct1.x, ct1.y, ct1.z);
            pb2 = point (cb2.x, cb2.y, cb2.z);
            pt2 = point (ct2.x, ct2.y, ct2.z);

            if (seg_num > 0):
              # Need to interpolate the bottom because it's no longer the bottom ring
              pb1.x = cb1.x + ((ct1.x-cb1.x)*(seg_num * 1.0 / num_segs));
              pb1.y = cb1.y + ((ct1.y-cb1.y)*(seg_num * 1.0 / num_segs));
              pb1.z = cb1.z + ((ct1.z-cb1.z)*(seg_num * 1.0 / num_segs));

              pb2.x = cb2.x + ((ct2.x-cb2.x)*(seg_num * 1.0 / num_segs));
              pb2.y = cb2.y + ((ct2.y-cb2.y)*(seg_num * 1.0 / num_segs));
              pb2.z = cb2.z + ((ct2.z-cb2.z)*(seg_num * 1.0 / num_segs));

            if (seg_num < (num_segs-1)):
              # Need to interpolate the top because it's not the top ring
              pt1.x = cb1.x + ((ct1.x-cb1.x)*((seg_num+1) * 1.0 / num_segs));
              pt1.y = cb1.y + ((ct1.y-cb1.y)*((seg_num+1) * 1.0 / num_segs));
              pt1.z = cb1.z + ((ct1.z-cb1.z)*((seg_num+1) * 1.0 / num_segs));

              pt2.x = cb2.x + ((ct2.x-cb2.x)*((seg_num+1) * 1.0 / num_segs));
              pt2.y = cb2.y + ((ct2.y-cb2.y)*((seg_num+1) * 1.0 / num_segs));
              pt2.z = cb2.z + ((ct2.z-cb2.z)*((seg_num+1) * 1.0 / num_segs));

            # Make the two triangular faces for this rectangle

            new_face = plf_object();
            new_face.add_point ( pb1 );
            new_face.add_point ( pt1 );
            new_face.add_point ( pb2 );
            new_face.add_face ( face (0, 1, 2) );
            self.merge ( new_face );

            new_face = plf_object();
            new_face.add_point ( pt1 );
            new_face.add_point ( pt2 );
            new_face.add_point ( pb2 );
            new_face.add_face ( face (0, 1, 2) );
            self.merge ( new_face );



class ShapedCylinder (plf_object):

  def sort_ring_indicies ( self, ring ):
    for i in range(len(ring)):
      for j in range(i+1,len(ring)):
        pi = self.points[ring[i]];
        pj = self.points[ring[j]];
        itheta = math.atan2(pi.x, pi.y);
        jtheta = math.atan2(pj.x, pj.y);
        if (jtheta < itheta):
          temp = ring[i];
          ring[i] = ring[j];
          ring[j] = temp;


  def __init__ ( self, num_sectors, z_profile ):
    """ z_profile is a sorted list of tuples where each tuple is (z,r), and the list is sorted with increasing z """

    self.points = [];
    self.faces = [];
    
    # Make the sides

    if ( len(z_profile) < 2 ):

      print ( "Error: z-profile must contain at least 2 entries (bottom and top)" );

    else:

      # Build the cylinder from bottom to top creating faces along the way

      # Loop through each ring segment from bottom to top (start with lowest ring as "upper")
      lower_z = -1
      lower_r = -1
      lower_ring = []
      upper_ring = []

      for seg_num in range(len(z_profile)):

        # Prepare to build a new upper ring
        upper_z = z_profile[seg_num][0]
        upper_r = z_profile[seg_num][1]

        # Loop around the circumference of the cylinder building a new upper ring
        if upper_r > 0:
          for i in range(num_sectors):
            theta = i * 2 * math.pi / num_sectors
            new_point = point ( upper_r*math.cos(theta), upper_r*math.sin(theta), upper_z )
            self.points = self.points + [ new_point ]
            upper_ring = upper_ring + [ new_point ]
        elif upper_r == 0:
          new_point = point ( 0.0, 0.0, upper_z )
          self.points = self.points + [ new_point ]
          for i in range(num_sectors):
            upper_ring = upper_ring + [ new_point ]

        if (seg_num > 0) and (len(upper_ring) > 0) and (len(lower_ring) > 0):
        
          # Both the upper and lower rings exist and are valid, so build the faces

          for i in range(num_sectors):

            # Make the faces for this rectangle / triangle

            pb1 = lower_ring[i];
            pt1 = upper_ring[i];
            pb2 = lower_ring[(i+1)%num_sectors];
            pt2 = upper_ring[(i+1)%num_sectors];

            if (lower_r >= 0) and (upper_r > 0):

              # We have either a triangle or a rectangle. Make this face.

              new_face = plf_object();  
              new_face.add_point ( pt1 );
              new_face.add_point ( pt2 );
              new_face.add_point ( pb2 );
              new_face.add_face ( face (0, 2, 1) );
              self.merge ( new_face );

            if (upper_r >= 0) and (lower_r > 0):

              # We have either a triangle or a rectangle. Make this face.

              new_face = plf_object();
              new_face.add_point ( pb1 );
              new_face.add_point ( pt1 );
              new_face.add_point ( pb2 );
              new_face.add_face ( face (0, 2, 1) );
              self.merge ( new_face );
              
        # Move the upper ring down to the lower ring
        lower_z = upper_z
        lower_r = upper_r
        lower_ring = upper_ring
        upper_ring = []



######################
#  Individual Tests  #
######################


###########################################################################################################
##   This is an example model used for all the SimRunner tests.

def SimRunnerExample ( context, method="QUEUE", test_name=None ):

    cb_model = CellBlender_Model ( context, test_name )

    scn = cb_model.get_scene()
    mcell = cb_model.get_mcell()
    mcell.run_simulation.simulation_run_control = method

    mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

    ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
    ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

    mol_a  = cb_model.get_molecule_species_by_name('a')

    cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="200" )

    cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=1.0 )

    cb_model.compare_mdl_with_sha1 ( "8263c1099a3d6d86640116a5f6ee6f5b4b663330", test_name=test_name )

    cb_model.refresh_molecules()

    cb_model.change_molecule_display ( mol_a, glyph='Cube', scale=2.0, red=1.0, green=0.0, blue=0.0 )

    cb_model.set_view_back()

    cb_model.scale_view_distance ( 0.1 )

    cb_model.hide_manipulator ( hide=True )

    cb_model.play_animation()



###########################################################################################################
#group_name = "Sim Runner Tests"
#test_name = "Simulation Runner Command Test"
#operator_name = "cellblender_test.sim_runner_command"
#next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

#class SimRunnerCommandTestOp(bpy.types.Operator):
#    bl_idname = operator_name
#    bl_label = test_name
#    self_test_name = test_name
#
#    def invoke(self, context, event):
#        self.execute ( context )
#        return {'FINISHED'}
#
#    def execute(self, context):
#        global active_frame_change_handler
#        active_frame_change_handler = None
#        SimRunnerExample ( context, method="COMMAND", test_name=self.self_test_name )
#        return { 'FINISHED' }



###########################################################################################################
group_name = "Sim Runner Tests"
test_name = "Simulation Runner Queue Test"
operator_name = "cellblender_test.sim_runner_queue"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SimRunnerQueueTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):
        global active_frame_change_handler
        active_frame_change_handler = None
        SimRunnerExample ( context, method="QUEUE", test_name=self.self_test_name )
        return { 'FINISHED' }



###########################################################################################################
#group_name = "Sim Runner Tests"
#test_name = "Simulation Runner Java Test"
#operator_name = "cellblender_test.sim_runner_java"
#next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

#class SimRunnerJavaTestOp(bpy.types.Operator):
#    bl_idname = operator_name
#    bl_label = test_name
#    self_test_name = test_name
#
#    def invoke(self, context, event):
#        self.execute ( context )
#        return {'FINISHED'}
#
#    def execute(self, context):
#        global active_frame_change_handler
#        active_frame_change_handler = None
#        SimRunnerExample ( context, method="JAVA", test_name=self.self_test_name )
#        return { 'FINISHED' }



###########################################################################################################
#group_name = "Sim Runner Tests"
#test_name = "Simulation Runner Open GL Test"
#operator_name = "cellblender_test.sim_runner_opengl"
#next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

#class SimRunnerOpenGLTestOp(bpy.types.Operator):
#    bl_idname = operator_name
#    bl_label = test_name
#    self_test_name = test_name

#    def invoke(self, context, event):
#        self.execute ( context )
#        return {'FINISHED'}

#    def execute(self, context):
#        SimRunnerExample ( context, method="OPENGL", test_name=self.self_test_name )
#        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Single Molecule Test"
operator_name = "cellblender_test.single_mol"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SingleMoleculeTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        mol = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mol, glyph="Torus", scale=5.0, red=1, green=1, blue=0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="1" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=2.0 )
        
        cb_model.compare_mdl_with_sha1 ( "e686b50419ad1a94388bb5e922ef6a9b92346260", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.02 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Double Sphere Test"
operator_name = "cellblender_test.double_sphere"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class DoubleSphereTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        mol_b = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a  = cb_model.get_molecule_species_by_name('a')
        mol_b  = cb_model.get_molecule_species_by_name('b')

        cb_model.change_molecule_display ( mol_a, glyph='Letter', letter='A', scale=2.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_b, glyph='Letter', letter='B', scale=2.0, red=0.0, green=1.0, blue=0.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="400", d="0.5", y="-0.25" )
        cb_model.add_molecule_release_site_to_model ( mol="b", q_expr="400", d="0.5", y="0.25" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=2.0 )

        cb_model.compare_mdl_with_sha1 ( "5029857613a93bad467d7e91451713ec4a2b78d7", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.1 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Volume Diffusion Constant Test"
operator_name = "cellblender_test.vol_diffusion_const"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class VolDiffusionConstTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        mol_b = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-7" )
        mol_c = cb_model.add_molecule_species_to_model ( name="c", diff_const_expr="1e-8" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a  = cb_model.get_molecule_species_by_name('a')
        mol_b  = cb_model.get_molecule_species_by_name('b')
        mol_c  = cb_model.get_molecule_species_by_name('c')

        cb_model.change_molecule_display ( mol_a, glyph='Letter', letter='A', scale=2.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_b, glyph='Letter', letter='B', scale=2.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_c, glyph='Letter', letter='C', scale=2.0, red=0.1, green=0.1, blue=1.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="100", d="0.01", y="-0.25" )
        cb_model.add_molecule_release_site_to_model ( mol="b", q_expr="100", d="0.01", y= "0.0" )
        cb_model.add_molecule_release_site_to_model ( mol="c", q_expr="100", d="0.01", y= "0.25" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=3.0 )

        cb_model.compare_mdl_with_sha1 ( "85028326cb23454b1c5f9a2b3b8e7316d51ffbc3", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.1 )
        cb_model.switch_to_orthographic()

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Simple Reaction Test"
operator_name = "cellblender_test.reaction"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ReactionTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        mol_b = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-6" )
        mol_c = cb_model.add_molecule_species_to_model ( name="bg", diff_const_expr="1e-5" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a  = cb_model.get_molecule_species_by_name('a')
        mol_b  = cb_model.get_molecule_species_by_name('b')
        mol_c  = cb_model.get_molecule_species_by_name('bg')

        cb_model.change_molecule_display ( mol_a, glyph='Cube', scale=2.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_b, glyph='Cube', scale=2.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_c, glyph='Torus', scale=10.0, red=1.0, green=1.0, blue=0.5 )

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="400", d="0.5", y="-0.05" )
        cb_model.add_molecule_release_site_to_model ( mol="b", q_expr="400", d="0.5", y="0.05" )

        cb_model.add_reaction_to_model ( rin="a + b", rtype="irreversible", rout="bg", fwd_rate="1e8", bkwd_rate="" )

        cb_model.run_model ( iterations='2000', time_step='1e-6', wait_time=20.0 )

        cb_model.compare_mdl_with_sha1 ( "e4498510e8d8a2c804707dfc314786d6ce558122", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.1 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Release Shape Test"
operator_name = "cellblender_test.release_shape"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ReleaseShapeTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.add_cube_to_model ( name="Cell", draw_type="WIRE" )

        diff_const = "1e-6"

        mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr=diff_const )
        mol_b = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr=diff_const )
        mol_c = cb_model.add_molecule_species_to_model ( name="bg", diff_const_expr=diff_const )
        mol_d = cb_model.add_molecule_species_to_model ( name="d", diff_const_expr=diff_const )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a  = cb_model.get_molecule_species_by_name('a')
        mol_b  = cb_model.get_molecule_species_by_name('b')
        mol_c  = cb_model.get_molecule_species_by_name('bg')
        mol_d  = cb_model.get_molecule_species_by_name('d')

        mol_scale = 2.5

        cb_model.change_molecule_display ( mol_a, glyph='Cube', scale=mol_scale, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_b, glyph='Cube', scale=mol_scale, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_c, glyph='Cube', scale=mol_scale, red=0.0, green=0.0, blue=1.0 )
        cb_model.change_molecule_display ( mol_d, glyph='Cube', scale=mol_scale, red=1.0, green=1.0, blue=0.0 )

        num_rel = "1000"

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr=num_rel, shape="OBJECT", obj_expr="Cell",  )
        cb_model.add_molecule_release_site_to_model ( mol="b", q_expr=num_rel, shape="SPHERICAL",       d="1.5", y="1" )
        cb_model.add_molecule_release_site_to_model ( mol="bg", q_expr=num_rel, shape="CUBIC",           d="1.5", y="-1" )
        cb_model.add_molecule_release_site_to_model ( mol="d", q_expr=num_rel, shape="SPHERICAL_SHELL", d="1.5", z="1" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=5.0 )

        cb_model.compare_mdl_with_sha1 ( "9e4bc202f9cfb65a0575b15695a51917e666bd00", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Parameter System Test"
operator_name = "cellblender_test.par_system"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ParSystemTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        # These are low level parameter operator and property setting commands

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "should_be_gone" )
        cb_model.parameter_system_op_remove()


        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "should_be_gone_1" )


        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "cant_delete_1" )
        cb_model.parameter_system_prop_expr ( "5 + 5" )
        cb_model.parameter_system_prop_units ( "mm" )
        cb_model.parameter_system_prop_desc ( "Test of adding a parameter via low level operators and properties" )

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "cant_delete_2" )
        cb_model.parameter_system_prop_expr ( "1e-6" )
        cb_model.parameter_system_prop_units ( "mm" )
        cb_model.parameter_system_prop_desc ( "Test of adding a parameter via low level operators and properties" )

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "should_be_gone_2" )
        cb_model.parameter_system_op_remove()


        cb_model.mcell.initialization.iterations.set_expr("cant_delete_1")
        cb_model.mcell.initialization.time_step.set_expr("cant_delete_2 * 2")

        # These are relatively high level parameter addition commands

        cb_model.add_parameter_to_model ( name="A", expr="1.23", units="A units", desc="" )
        cb_model.add_parameter_to_model ( name="B", expr="A * 2", units="B units", desc="" )
        cb_model.add_parameter_to_model ( name="C", expr="A * B", units="", desc="A * B" )
        cb_model.add_parameter_to_model ( name="dc", expr="1e-8", units="", desc="Diffusion Constant" )

        mol = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="dc" )
        

        # Back to some low level calls

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "cant_delete_3" )
        cb_model.parameter_system_prop_expr ( "123" )
        cb_model.parameter_system_prop_units ( "ft" )
        cb_model.parameter_system_prop_desc ( "Another GP depends on me" )

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "depends_on_cant_del_3" )
        cb_model.parameter_system_prop_expr ( "2 * cant_delete_3" )
        cb_model.parameter_system_prop_units ( "ft" )
        cb_model.parameter_system_prop_desc ( "This depends on cant_delete_3" )


        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "cant_delete_1" ) )

        cb_model.parameter_system_op_add()
        cb_model.parameter_system_prop_name ( "should_be_gone_3" )


        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "should_be_gone_3" ) )
        cb_model.parameter_system_op_remove()

        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "should_be_gone_1" ) )
        cb_model.parameter_system_op_remove()

        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "A" ) )
        cb_model.parameter_system_prop_name ( "AinC" )

        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "B" ) )
        cb_model.parameter_system_prop_name ( "BinC" )

        cb_model.parameter_system_op_set_active ( cb_model.parameter_system_index_of_name ( "cant_delete_1" ) )
        # Unfortunately, trying to remove a parameter that is used by another throws a RuntimeError, so comment to avoid an error
        #cb_model.parameter_system_op_remove()



        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mol, glyph='Torus', scale=4.0, red=1.0, green=1.0, blue=0.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="C" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=4.0 )

        cb_model.compare_mdl_with_sha1 ( "0e8e59531032418691f245f668df968aca0ac7b6", test_name=self.self_test_name )
        
        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.04 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }


###########################################################################################################
# Shared routines for various paramter test configurations

def pname ( n ):
    name = None
    if n < 26:
        name = chr(ord('a')+n)
    else:
        name = "P_" + str(n)
    return name

def ParSysTest ( cb_model, first="1", num_pars=10, num_back=1, mdl_hash="", test_name="ParSysTest", wait_time=4.0 ):

    scn = cb_model.get_scene()
    mcell = cb_model.get_mcell()

    # Add new parameters
    if cb_model.using_id_params():
        # Use batch add
        pars = []
        for n in range(num_pars):
            par = {}
            exp_str = first
            for i in range(max(n-num_back,0),n):
                exp_str += ' + '
                exp_str += pname(i)
            par['par_name'] = pname(n)
            par['par_description'] = "Parameter "+par['par_name']
            par['par_units'] = "u"
            par['par_expression'] = exp_str
            pars.append ( par )
        cb_model.context.scene.mcell.parameter_system.add_general_parameters_from_list ( cb_model.context, pars )

    else:
        # Use non-batch add
        for n in range(num_pars):
            exp_str = first
            for i in range(max(n-num_back,0),n):
                exp_str += ' + '
                exp_str += pname(i)

            par_name = pname(n)
            cb_model.add_parameter_to_model ( name=par_name, expr=exp_str, units="u", desc="Parameter "+par_name )

    mol = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

    ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
    ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

    mol  = cb_model.get_molecule_species_by_name('a')

    cb_model.change_molecule_display ( mol, glyph='Torus', scale=4.0, red=1.0, green=1.0, blue=0.0 )

    cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="10" )

    cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=wait_time )

    cb_model.compare_mdl_with_sha1 ( mdl_hash, test_name=test_name )

    cb_model.refresh_molecules()

    cb_model.select_none()


    cb_model.set_view_back()

    cb_model.scale_view_distance ( 0.04 )

    cb_model.hide_manipulator ( hide=True )

    cb_model.play_animation()

    return cb_model


###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "200 Pars Counting"
operator_name = "cellblender_test.par_sys_200pc"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ParSys200pCntTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )
        cb_model = ParSysTest ( cb_model, first='1', num_pars=200, num_back=1, mdl_hash="348f796badcbcaf05562d772ef498c263ea0ed10", test_name=self.self_test_name )

        return { 'FINISHED' }


###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "100 Pars Using 3 Each"
operator_name = "cellblender_test.par_sys_100p3e"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ParSystem100p3eTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )
        if cb_model.using_id_params():
            cb_model = ParSysTest ( cb_model, first='1e-6', num_pars=100, num_back=3, mdl_hash="1e8dca080ab8ab213f9f0d381d05bd9cadb3dfc7", test_name=self.self_test_name )
        else:
            cb_model = ParSysTest ( cb_model, first='1e-6', num_pars=100, num_back=3, mdl_hash="1be16b43f98f8a61617eb8450601a5deafccd3f3", test_name=self.self_test_name )

        return { 'FINISHED' }


###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "1000 Pars Using 3 Each"
operator_name = "cellblender_test.par_sys_1000p3e"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ParSystem1000p3eTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )
        if cb_model.using_id_params():
            cb_model = ParSysTest ( cb_model, first='1e-6', num_pars=1000, num_back=3, mdl_hash="959a55e1de527d2a3e24518bb19e27b97a07057c", test_name=self.self_test_name )
        else:
            cb_model = ParSysTest ( cb_model, first='1e-6', num_pars=1000, num_back=3, mdl_hash="fe97effc69d90e15c5a39b72aebfbbd660d3f707", test_name=self.self_test_name )

        return { 'FINISHED' }



###########################################################################################################
group_name = "Non-Geometry Tests"
test_name = "Molecule Glyph Test"
operator_name = "cellblender_test.molecule_glyph"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class GlyphTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()
        
        cb_model.add_parameter_to_model ( name="n", expr="10", units="", desc="Number of molecules to release" )
        cb_model.add_parameter_to_model ( name="dc", expr="1e-6", units="", desc="Diffusion Constant" )

        # Create a default molecule as a way to get the glyph names without hard-coding here
        mol = cb_model.add_molecule_species_to_model ( name="NoMols" )

        # Get the current glyph names
        glyph_names = [ l[0] for l in mol.glyph_enum ]
        glyph_letters = [ l[0] for l in mol.letter_enum ]

        for glyph_name in glyph_names:
            if glyph_name == 'Letter':
                for letter_name in glyph_letters:
                    mol = cb_model.add_molecule_species_to_model ( name=letter_name, diff_const_expr="dc" )
                    cb_model.change_molecule_display ( mol, glyph="Letter", letter=letter_name, scale=1.0, red=random.random(), green=random.random(), blue=random.random() )
                    cb_model.add_molecule_release_site_to_model ( mol=letter_name, q_expr="n" )
            else:
                mol = cb_model.add_molecule_species_to_model ( name=glyph_name, diff_const_expr="dc" )
                cb_model.change_molecule_display ( mol, glyph=glyph_name, scale=1.0, red=random.random(), green=random.random(), blue=random.random() )
                cb_model.add_molecule_release_site_to_model ( mol=glyph_name, q_expr="n" )

        cb_model.run_model ( iterations='1000', time_step='1e-6', wait_time=4.0 )

        cb_model.compare_mdl_with_sha1 ( "2551b6fe95415e7053cd40c02fe61844ee034bcd", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.04 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }





###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Simple Cube Test"
operator_name = "cellblender_test.cube_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class CubeTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.add_cube_to_model ( name="Cell", draw_type="WIRE" )

        mol = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mol, glyph='Cube', scale=4.0, red=1.0, green=0.0, blue=0.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="Cell", q_expr="1000" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=2.0 )

        cb_model.compare_mdl_with_sha1 ( "1d006610fe4a01735e92e0a07e3faae722383a3f", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }


###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Cube Surface Test"
operator_name = "cellblender_test.cube_surf_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class CubeSurfaceTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.add_cube_to_model ( name="Cell", draw_type="WIRE" )
        cb_model.add_surface_region_to_model_object_by_normal ( "Cell", "top", 0, 0, 1, 0.8 )

        mola = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        mols = cb_model.add_molecule_species_to_model ( name="s", mol_type="2D", diff_const_expr="1e-6" )
        molb = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        mols  = cb_model.get_molecule_species_by_name('s')
        molb  = cb_model.get_molecule_species_by_name('b')

        cb_model.change_molecule_display ( mola, glyph='Cube', scale=3.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mols, glyph='Cone', scale=3.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molb, glyph='Torus', scale=9.0, emit=2.0, red=1.0, green=1.0, blue=1.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="Cell", q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( mol="s", shape="OBJECT", obj_expr="Cell[top]", orient="'", q_expr="1000" )

        cb_model.add_reaction_to_model ( rin="a' + s,", rtype="irreversible", rout="b, + s,", fwd_rate="1e8", bkwd_rate="" )


        cb_model.run_model ( iterations='500', time_step='1e-6', wait_time=6.0 )

        cb_model.compare_mdl_with_sha1 ( "ec58f3b5fbff36014d9cbf20ce2166bc7d750460", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        
        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Sphere Surface Test"
operator_name = "cellblender_test.sphere_surf_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SphereSurfaceTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.add_icosphere_to_model ( name="Cell", draw_type="WIRE" )
        cb_model.add_surface_region_to_model_object_by_normal ( "Cell", "top", 0, 0, 1, 0.8 )

        mola = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        mols = cb_model.add_molecule_species_to_model ( name="s", mol_type="2D", diff_const_expr="1e-6" )
        molb = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        mols  = cb_model.get_molecule_species_by_name('s')
        molb  = cb_model.get_molecule_species_by_name('b')

        cb_model.change_molecule_display ( mola, glyph='Cube', scale=3.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mols, glyph='Cone', scale=3.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molb, glyph='Cube', scale=6.0, red=1.0, green=1.0, blue=1.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="Cell", q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( mol="s", shape="OBJECT", obj_expr="Cell[top]", orient="'", q_expr="1000" )

        cb_model.add_reaction_to_model ( rin="a' + s,", rtype="irreversible", rout="b, + s,", fwd_rate="1e8", bkwd_rate="" )

        cb_model.run_model ( iterations='500', time_step='1e-6', wait_time=7.0 )

        cb_model.compare_mdl_with_sha1 ( "423801fc511d12515dcd25f6336feca082d013b7", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        
        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }




###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Overlapping Surface Test"
operator_name = "cellblender_test.overlapping_surf_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class OverlappingSurfaceTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.add_icosphere_to_model ( name="Cell", draw_type="WIRE", subdiv=4 )
        cb_model.add_surface_region_to_model_object_by_normal ( "Cell", "top", 0, 0, 1, 0.0 )
        cb_model.add_surface_region_to_model_object_by_normal ( "Cell", "y",   0, 1, 0, 0.0 )

        mola  = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-5" )
        mols1 = cb_model.add_molecule_species_to_model ( name="s1", mol_type="2D", diff_const_expr="0" )
        mols2 = cb_model.add_molecule_species_to_model ( name="s2", mol_type="2D", diff_const_expr="0" )
        molb1 = cb_model.add_molecule_species_to_model ( name="b1", diff_const_expr="1e-7" )
        molb2 = cb_model.add_molecule_species_to_model ( name="b2", diff_const_expr="1e-7" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        mols1 = cb_model.get_molecule_species_by_name('s1')
        mols2 = cb_model.get_molecule_species_by_name('s2')
        molb1  = cb_model.get_molecule_species_by_name('b1')
        molb2  = cb_model.get_molecule_species_by_name('b2')

        cb_model.change_molecule_display ( mola, glyph='Cube',  scale=3.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mols1, glyph='Cone', scale=3.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( mols2, glyph='Cone', scale=3.0, red=1.0, green=0.0, blue=1.0 )
        cb_model.change_molecule_display ( molb1, glyph='Cube', scale=4.0, red=1.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molb2, glyph='Cube', scale=4.0, red=0.0, green=1.0, blue=1.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="Cell", q_expr="2000" )
        cb_model.add_molecule_release_site_to_model ( mol="s1", shape="OBJECT", obj_expr="Cell[top]", orient="'", q_expr="2000" )
        cb_model.add_molecule_release_site_to_model ( mol="s2", shape="OBJECT", obj_expr="Cell[y]", orient="'", q_expr="2000" )

        cb_model.add_reaction_to_model ( rin="a' + s1,", rtype="irreversible", rout="a' + b1, + s1,", fwd_rate="1e10", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="a' + s2,", rtype="irreversible", rout="a' + b2, + s2,", fwd_rate="1e10", bkwd_rate="" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=5.0 )

        cb_model.compare_mdl_with_sha1 ( "5a0eb3b118623ce7ba3cd8db13b14dd426e01ff3", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }




###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Surface Classes Test"
operator_name = "cellblender_test.surface_classes_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SurfaceClassesTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.switch_to_orthographic()

        cb_model.add_cube_to_model ( name="ti", draw_type="WIRE", x=0, y=0, z=0, size=0.5 )
        cb_model.add_surface_region_to_model_object_by_normal ( "ti", "t_reg" )  # Without a normal vector this assigns all faces by region (not by "ALL")
        cb_model.add_cube_to_model ( name="to", draw_type="WIRE", x=0, y=0, z=0, size=1.0 )

        cb_model.add_cube_to_model ( name="ri", draw_type="WIRE", x=0, y=-3, z=0, size=0.5 )
        cb_model.add_surface_region_to_model_object_by_normal ( "ri", "r_reg" )  # Without a normal vector this assigns all faces by region (not by "ALL")
        cb_model.add_cube_to_model ( name="ro", draw_type="WIRE", x=0, y=-3, z=0, size=1.0 )

        cb_model.add_cube_to_model ( name="ai", draw_type="WIRE", x=0, y=3, z=0, size=0.5 )
        # cb_model.add_surface_region_to_model_object_by_normal ( "ai", "a_reg" )  # Without a normal vector this assigns all faces by region (not by "ALL")
        cb_model.add_cube_to_model ( name="ao", draw_type="WIRE", x=0, y=3, z=0, size=1.0 )

        cb_model.add_cube_to_model ( name="ci", draw_type="WIRE", x=0, y=0, z=3, size=0.5 )
        cb_model.add_surface_region_to_model_object_by_normal ( "ci", "c_reg" )  # Without a normal vector this assigns all faces by region (not by "ALL")
        cb_model.add_cube_to_model ( name="co", draw_type="WIRE", x=0, y=0, z=3, size=1.0 )

        cb_model.add_label_to_model ( name="t", text="Trans",   x=0, y=-1.13, z=-2,  size=1, rx=math.pi/2, ry=0, rz=math.pi/2 )
        cb_model.add_label_to_model ( name="c", text="Clamp",   x=0, y=-1.26, z=4.4, size=1, rx=math.pi/2, ry=0, rz=math.pi/2 )
        cb_model.add_label_to_model ( name="r", text="Reflect", x=0, y=-4.38, z=-2,  size=1, rx=math.pi/2, ry=0, rz=math.pi/2 )
        cb_model.add_label_to_model ( name="a", text="Absorb",  x=0, y=1.82,  z=-2,  size=1, rx=math.pi/2, ry=0, rz=math.pi/2 )

        mola = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        molt = cb_model.add_molecule_species_to_model ( name="t", diff_const_expr="1e-6" )
        molr = cb_model.add_molecule_species_to_model ( name="r", diff_const_expr="1e-6" )
        molc = cb_model.add_molecule_species_to_model ( name="c", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        molt  = cb_model.get_molecule_species_by_name('t')
        molr  = cb_model.get_molecule_species_by_name('r')
        molc  = cb_model.get_molecule_species_by_name('c')

        cb_model.change_molecule_display ( mola, glyph='Cube', scale=5.0, red=0.0, green=0.7, blue=1.0 )
        cb_model.change_molecule_display ( molt, glyph='Cube', scale=5.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molr, glyph='Cube', scale=5.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( molc, glyph='Cube', scale=5.0, red=1.0, green=1.0, blue=0.5 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="ai", q_expr="100" )
        cb_model.add_molecule_release_site_to_model ( mol="t", shape="OBJECT", obj_expr="ti", q_expr="100" )
        cb_model.add_molecule_release_site_to_model ( mol="r", shape="OBJECT", obj_expr="ri", q_expr="100" )
        cb_model.add_molecule_release_site_to_model ( mol="c", shape="OBJECT", obj_expr="ci", q_expr="100" )

        cb_model.add_surface_class_to_model ( "trans_to_t" )
        cb_model.add_property_to_surface_class ( "t", sc_orient=";", sc_type="TRANSPARENT" )

        cb_model.add_surface_class_to_model ( "reflect_to_r" )
        cb_model.add_property_to_surface_class ( "r", sc_orient=";", sc_type="REFLECTIVE" )

        cb_model.add_surface_class_to_model ( "absorb_to_a" )
        cb_model.add_property_to_surface_class ( "a", sc_orient=";", sc_type="ABSORPTIVE" )

        cb_model.add_surface_class_to_model ( "clamp_to_c" )
        cb_model.add_property_to_surface_class ( "c", sc_orient=";", sc_type="CLAMP_CONCENTRATION",  sc_clamp_val_str="1.5e-7" )


        cb_model.assign_surface_class_to_region ( "trans_to_t", "ti", "t_reg" )
        cb_model.assign_surface_class_to_region ( "reflect_to_r", "ri", "r_reg" )
        ## cb_model.assign_surface_class_to_region ( "absorb_to_a", "ai", "a_reg" )
        cb_model.assign_surface_class_to_region ( "absorb_to_a", "ai", "ALL" )
        cb_model.assign_surface_class_to_region ( "clamp_to_c", "ci", "c_reg" )


        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[0].molecule_name = 't'
        mcell.rxn_output.rxn_output_list[0].count_location = 'Object'
        mcell.rxn_output.rxn_output_list[0].object_name = 'ti'

        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[1].molecule_name = 'r'
        mcell.rxn_output.rxn_output_list[1].count_location = 'Object'
        mcell.rxn_output.rxn_output_list[1].object_name = 'ri'

        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[2].molecule_name = 'a'
        mcell.rxn_output.rxn_output_list[2].count_location = 'Object'
        mcell.rxn_output.rxn_output_list[2].object_name = 'ai'

        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[3].molecule_name = 'c'
        mcell.rxn_output.rxn_output_list[3].count_location = 'Object'
        mcell.rxn_output.rxn_output_list[3].object_name = 'ci'

        mcell.rxn_output.plot_layout = ' '
        mcell.rxn_output.mol_colors = True

        cb_model.run_model ( iterations='5000', time_step='1e-6', wait_time=40.0 )

        cb_model.compare_mdl_with_sha1 ( "63c08fa5300d6744d701b9d6d15c59ce89dacfe5", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.5 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Capsule in Capsule Test"
operator_name = "cellblender_test.capsule_tests"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class CapsuleTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        # Create the capsule object, and define the surface as a membrane

        cb_model.add_capsule_to_model ( name="shell",   draw_type="WIRE", x=0, y=0, z=0, sigma=0, subdiv=2, radius=0.501, cyl_len=4.002, subdivide_sides=False )
        cb_model.add_capsule_to_model ( name="capsule", draw_type="WIRE", x=0, y=0, z=0, sigma=0, subdiv=2, radius=0.500, cyl_len=4,     subdivide_sides=False )
        cb_model.add_surface_region_to_model_object_by_normal ( "capsule", "top", nx=0, ny=0, nz=1, min_dot_prod=0.5 )
        cb_model.add_surface_region_to_model_object_by_normal ( "capsule", "bot", nx=0, ny=0, nz=-1, min_dot_prod=0.5 )


        mola  = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )
        molpa = cb_model.add_molecule_species_to_model ( name="pa", mol_type="2D", diff_const_expr="0" )
        molb  = cb_model.add_molecule_species_to_model ( name="b", diff_const_expr="1e-5" )
        molpb = cb_model.add_molecule_species_to_model ( name="pb", mol_type="2D", diff_const_expr="0" )
        molc  = cb_model.add_molecule_species_to_model ( name="c", diff_const_expr="1e-7" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        molpa = cb_model.get_molecule_species_by_name('p1')
        molb  = cb_model.get_molecule_species_by_name('b')
        molpb = cb_model.get_molecule_species_by_name('pb')
        molc  = cb_model.get_molecule_species_by_name('c')

        cb_model.change_molecule_display ( mola,  glyph='Cube', scale=2.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( molpa, glyph='Cone', scale=2.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molb,  glyph='Cube', scale=3.0, red=1.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molpb, glyph='Cone', scale=2.0, red=0.0, green=1.0, blue=1.0 )
        cb_model.change_molecule_display ( molc,  glyph='Cube', scale=4.0, red=1.0, green=1.0, blue=1.0 )


        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="capsule", q_expr="2000" )
        cb_model.add_molecule_release_site_to_model ( mol="pa", shape="OBJECT", obj_expr="capsule[top]", orient="'", q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( mol="pb", shape="OBJECT", obj_expr="capsule[bot]", orient="'", q_expr="1000" )
        #### Add a single b molecule so the display values can be set ... otherwise they're not applied properly
        #cb_model.add_molecule_release_site_to_model ( mol="b", q_expr="1", shape="SPHERICAL", d="0", z="0.000" )
        #cb_model.add_molecule_release_site_to_model ( mol="c", q_expr="1", shape="SPHERICAL", d="0", z="0.000" )


        cb_model.add_reaction_to_model ( rin="a' + pa,", rtype="irreversible", rout="b, + pa,", fwd_rate="1e9", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="b, + pb,", rtype="irreversible", rout="c' + pb,", fwd_rate="1e9", bkwd_rate="" )

        cb_model.add_count_output_to_model ( mol_name="a" )
        cb_model.add_count_output_to_model ( mol_name="b" )
        cb_model.add_count_output_to_model ( mol_name="c", object_name="capsule", count_location="Object" )

        cb_model.set_visualization ( enable_visualization=True, export_all=True, all_iterations=False, start=0, end=100000, step=2 )

        mcell.rxn_output.plot_layout = ' '
        mcell.rxn_output.mol_colors = True

        mcell.partitions.include = True
        bpy.ops.mcell.auto_generate_boundaries()

        cb_model.run_model ( iterations='10000', time_step='1e-6', wait_time=50.0 )

        cb_model.compare_mdl_with_sha1 ( "9413bb5f46ac9479bbbc71b2af0cf21afa6d1648", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }




###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Goblet Test"
operator_name = "cellblender_test.goblet_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class GobletTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        # Create a goblet

        thk = 0.02
        
        # This version will be a torus with a hollow shaft:
        #goblet = [ (-2,0.8), (-1.8,0.1), (0,0.1), (0.2,0.5), (2,0.8),
        #           (2,0.8-thk), (0.2,0.5-thk), (0,0.1-thk), (-1.8,0.1-thk), (-2,0.8-thk), (-2,0.8) ]

        # This version will be a solid:
        goblet = [ (-2.1,-1), (-1.9,0), (-2,0.8), (-(2-thk),0.8), (-1.8,0.1), (0,0.1), (0.2,0.5), (2,0.8),
                   (2,0.8-thk), (0.2,0.5-thk), (0,0.0), (0.1,-1) ]

        cb_model.add_shaped_cylinder_to_model ( name="goblet", draw_type="WIRE", x=0, y=0, z=0, sigma=0, numsect=10, z_profile=goblet )

        mola  = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mola, glyph='Cube', scale=3.0, red=0.96, green=1.0, blue=0.3 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="goblet", q_expr="1000" )

        cb_model.set_visualization ( enable_visualization=True, export_all=True, all_iterations=False, start=0, end=100000, step=1 )

        cb_model.run_model ( iterations='1000', time_step='1e-6', wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "6bd75c3193a22497a8eb6eb794130e8db98b4dec", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "Dividing Capsule Test"
operator_name = "cellblender_test.ecoli_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

"""
NOTE: This algorithm doesn't generate equally spaced slices as expected.
"""

class EcoliTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        # Create a dividing ecoli according to parameters listed below
        
        ecoli = []
        
        ns  = 19          # Number of sections around the circumference of the cylinder
        ncf = 5           # Number of cap facets from side to tip
        ilength = 2.0     # Initial length of entire object from tip to tip
        flength = 10.0    # Final length of entire object from tip to tip
        mnclength = 1.0   # Minimum length of a single cell
        mxclength = 4.0   # Maximum length of a single cell
        glength = 0.8     # Distance between cells
        radius = 0.5      # Radius of cylinder
        num_frames = 250  # Frames from start to finish
        pinch = True      # Flag to "pinch" the cell for division
        
        frame_to_show = 225  # Compute this frame of the series (this could be a function of the current frame for scene updating)

        total_length = ilength + ( frame_to_show * (flength-ilength) / num_frames ) # Length of entire object from tip to tip

        # Create the radial profile of the "chain" of ecoli cells

        # As a cell approaches its maximum length, it will start to split by constricting in the middle
        # At the point of it's maximum length, it will have constricted to zero radius in the middle
        # The constriction area ranges from 0 to the cell radius
        # If cell is less than mxclength - radius, then there is no constriction zone
        # When the cell is between (mxclength - radius) and (mxclength) there will be a constriction
        #
        
        # Start with the total length based on the current time frame:
        
        # Compute the number of cells
        
        norm_length = total_length / (mxclength + glength)
        num_cells = int ( math.pow ( 2, int ( math.log2 ( 2 * norm_length ) ) ) )
        seglength = total_length/num_cells
        cell_length = seglength - (glength)
        
        ecoli = []
        
        hg = glength / 2.0
        z = -total_length / 2.0
        z = z - (hg/2)
        ecoli = ecoli + [ (z, 0.0) ]
        for cnum in range(num_cells):

          # Create the bottom cap

          for fn in range(ncf):
            angle = fn * (math.pi/2) / ncf
            ecoli = ecoli + [ ( z+hg+(radius*((1-math.cos(angle)))), radius*math.sin(angle) ) ]
          
          ecoli = ecoli + [ ( z+hg+radius, radius ) ]

          # Create the cylinder for the main body
          
          cylinder_length = cell_length - (2 * radius)
          nominal_length = math.pi * radius / (2 * ncf)
          num_segments = round ( (cylinder_length + (nominal_length/2)) / nominal_length )
          
          # Force an even number of segments so there's a pinch center
          if (num_segments % 2) > 0:
            num_segments += 1

          bot_z = z + hg + radius
          for cyl_seg_num in range(num_segments-1):
            pinch_factor = 1.0
            if pinch and (cell_length > (mxclength - (2*radius))):
              # Need to start pinching the center
              pinch_dist = ( cell_length - (mxclength - (2*radius)) ) / 2
              if pinch_dist > 0:
                dist_from_center = ((cyl_seg_num+1) * cylinder_length / num_segments) - (cylinder_length/2)
                if abs(dist_from_center) < pinch_dist:
                  norm_dist = abs(dist_from_center) / radius
                  pinch_factor = math.sin ( math.acos((pinch_dist/radius)-norm_dist) )
            
            ecoli = ecoli + [ ( bot_z + (cylinder_length*(cyl_seg_num+1)/num_segments), radius * pinch_factor ) ]

          # Create the top cap

          ecoli = ecoli + [ ( z+seglength-(radius), radius ) ]

          for fn in range(ncf):
            angle = ((ncf-1)-fn) * (math.pi/2) / ncf
            ecoli = ecoli + [ ( z+seglength+(radius*((0+math.cos(angle))))-radius, radius*math.sin(angle) ) ]

          z += seglength

        # Close the entire capsule
        ecoli = ecoli + [ (z, 0.0) ]
        
        cb_model.add_shaped_cylinder_to_model ( name="ecoli", draw_type="SOLID", x=0, y=0, z=0, sigma=0, numsect=ns, z_profile=ecoli )

        # Set up the material for the object
        if len(bpy.data.materials) <= 0:
            new_mat = bpy.data.materials.new("cell")
        bpy.data.materials[0].name = 'cell'
        bpy.data.materials['cell'].use_transparency = True
        bpy.data.materials['cell'].alpha = 0.3

        # Assign the material to the object
        bpy.ops.object.material_slot_add()
        scn.objects['ecoli'].material_slots[0].material = bpy.data.materials['cell']
        scn.objects['ecoli'].show_transparent = True


        mola  = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mola, glyph='Cube', scale=5.0, red=0.0, green=0.7, blue=1.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="ecoli", q_expr="1000" )

        cb_model.set_visualization ( enable_visualization=True, export_all=True, all_iterations=False, start=0, end=100000, step=1 )

        cb_model.run_model ( iterations='1000', time_step='1e-6', wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "da8ff36b3a428bc1aa9078745ab367f73a29423e", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        
        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.45 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
##   Helper Function supporting MDL Import Testing

def write_geometry_file_M_D_L ( filename ):
  ol = [

    { "name": "M",
      "vertex_list": [
        [ -0.1742, -0.0654, 0.6820 ], [ -0.2652, -0.0654, 0.6820 ], [ -0.4922, -0.0654, 0.4020 ], [ -0.7182, -0.0654, 0.6820 ],
        [ -0.8102, -0.0654, 0.6820 ], [ -0.8102, -0.0654, 0.0000 ], [ -0.7122, -0.0654, 0.0000 ], [ -0.7112, -0.0654, 0.5310 ],
        [ -0.4922, -0.0654, 0.2670 ], [ -0.2732, -0.0654, 0.5310 ], [ -0.2722, -0.0654, 0.0000 ], [ -0.1742, -0.0654, 0.0000 ],
        [ -0.7122,  0.0654, 0.0000 ], [ -0.7112,  0.0654, 0.5310 ], [ -0.4922,  0.0654, 0.4020 ], [ -0.7182,  0.0654, 0.6820 ],
        [ -0.4922,  0.0654, 0.2670 ], [ -0.1742,  0.0654, 0.6820 ], [ -0.2732,  0.0654, 0.5310 ], [ -0.2722,  0.0654, 0.0000 ],
        [ -0.1742,  0.0654, 0.0000 ], [ -0.8102,  0.0654, 0.6820 ], [ -0.8102,  0.0654, 0.0000 ], [ -0.2652,  0.0654, 0.6820 ]
      ],
      "element_connections": [
        [  9,  1,  0 ], [  4,  7,  5 ], [  8,  7,  2 ], [ 10,  9, 11 ], [  9,  0, 11 ], [  2,  9,  8 ], [  2,  1,  9 ], [  7,  3,  2 ],
        [ 18, 17, 23 ], [ 13, 15, 21 ], [ 16, 14, 13 ], [ 19, 20, 18 ], [ 18, 20, 17 ], [ 14, 16, 18 ], [ 14, 18, 23 ], [ 13, 14, 15 ],
        [  6, 12, 22 ], [  9, 18, 16 ], [ 10, 19, 18 ], [  2, 14, 23 ], [ 11, 20, 19 ], [  1, 23, 17 ],
        [  5, 22, 21 ], [  8, 16, 13 ], [  7, 13, 12 ], [  3, 15, 14 ], [  0, 17, 20 ], [  4, 21, 15 ], [  6,  5,  7 ], [  4,  3,  7 ],
        [ 21, 22, 13 ], [ 12, 13, 22 ], [  5,  6, 22 ], [  8,  9, 16 ], [  9, 10, 18 ], [  1,  2, 23 ],
        [ 10, 11, 19 ], [  0,  1, 17 ], [  4,  5, 21 ], [  7,  8, 13 ], [  6,  7, 12 ], [  2,  3, 14 ], [ 11,  0, 20 ], [  3,  4, 15 ]
      ]
    },

    { "name": "D",
      "vertex_list": [
        [ -0.0262, -0.0654, 0.0000 ], [  0.2397, -0.0654, 0.0000 ], [  0.3446, -0.0654, 0.0131 ], [  0.4335, -0.0654, 0.0495 ],
        [  0.4993, -0.0654, 0.0976 ], [  0.5490, -0.0654, 0.1685 ], [  0.5817, -0.0654, 0.2474 ], [  0.5966, -0.0654, 0.3384 ],
        [  0.5923, -0.0654, 0.4221 ], [  0.5636, -0.0654, 0.5009 ], [  0.5147, -0.0654, 0.5718 ], [  0.4448, -0.0654, 0.6293 ],
        [  0.3531, -0.0654, 0.6679 ], [  0.2387, -0.0654, 0.6820 ], [ -0.0262, -0.0654, 0.6820 ], [  0.0717, -0.0654, 0.5940 ],
        [  0.2227, -0.0654, 0.5940 ], [  0.3096, -0.0654, 0.5847 ], [  0.3796, -0.0654, 0.5588 ], [  0.4333, -0.0654, 0.5188 ],
        [  0.4710, -0.0654, 0.4674 ], [  0.4933, -0.0654, 0.4073 ], [  0.5007, -0.0654, 0.3410 ], [  0.4938, -0.0654, 0.2732 ],
        [  0.4654, -0.0654, 0.2101 ], [  0.4248, -0.0654, 0.1576 ], [  0.3640, -0.0654, 0.1157 ], [  0.3023, -0.0654, 0.0961 ],
        [  0.2277, -0.0654, 0.0880 ], [  0.0717, -0.0654, 0.0880 ], [  0.5923,  0.0654, 0.4221 ], [  0.4933,  0.0654, 0.4073 ],
        [ -0.0262,  0.0654, 0.0000 ], [ -0.0262,  0.0654, 0.6820 ], [  0.3023,  0.0654, 0.0961 ], [  0.2277,  0.0654, 0.0880 ],
        [  0.2387,  0.0654, 0.6820 ], [  0.2397,  0.0654, 0.0000 ], [  0.0717,  0.0654, 0.5940 ], [  0.4938,  0.0654, 0.2732 ],
        [  0.4654,  0.0654, 0.2101 ], [  0.4335,  0.0654, 0.0495 ], [  0.4993,  0.0654, 0.0976 ], [  0.0717,  0.0654, 0.0880 ],
        [  0.5147,  0.0654, 0.5718 ], [  0.4448,  0.0654, 0.6293 ], [  0.4248,  0.0654, 0.1576 ], [  0.5490,  0.0654, 0.1685 ],
        [  0.3096,  0.0654, 0.5847 ], [  0.3796,  0.0654, 0.5588 ], [  0.5636,  0.0654, 0.5009 ], [  0.5817,  0.0654, 0.2474 ],
        [  0.4333,  0.0654, 0.5188 ], [  0.4710,  0.0654, 0.4674 ], [  0.2227,  0.0654, 0.5940 ], [  0.3531,  0.0654, 0.6679 ],
        [  0.5966,  0.0654, 0.3384 ], [  0.3446,  0.0654, 0.0131 ], [  0.5007,  0.0654, 0.3410 ], [  0.3640,  0.0654, 0.1157 ]
      ],
      "element_connections": [
        [  0, 14, 15 ], [  0, 15, 29 ], [ 20, 10,  9 ], [  5, 23,  6 ], [ 23,  7,  6 ], [ 22,  8,  7 ], [  4, 24,  5 ], [ 27, 26,  2 ],
        [ 11, 18, 12 ], [ 13, 15, 14 ], [ 20,  9, 21 ], [ 13, 16, 15 ], [ 19, 10, 20 ], [ 13, 17, 16 ], [ 18, 11, 19 ], [ 13, 12, 17 ],
        [ 10, 19, 11 ], [  8, 21,  9 ], [ 17, 12, 18 ], [ 24, 23,  5 ], [ 22,  7, 23 ], [ 21,  8, 22 ], [ 25, 24,  4 ], [  3, 25,  4 ],
        [ 28,  1, 29 ], [  3, 26, 25 ], [ 27,  1, 28 ], [  3,  2, 26 ], [  1, 27,  2 ], [ 29,  1,  0 ], [ 32, 38, 33 ], [ 32, 43, 38 ],
        [ 53, 50, 44 ], [ 47, 51, 39 ], [ 39, 51, 56 ], [ 58, 56, 30 ], [ 42, 47, 40 ], [ 34, 57, 59 ], [ 45, 55, 49 ], [ 36, 33, 38 ],
        [ 53, 31, 50 ], [ 36, 38, 54 ], [ 52, 53, 44 ], [ 36, 54, 48 ], [ 49, 52, 45 ], [ 36, 48, 55 ], [ 44, 45, 52 ], [ 30, 50, 31 ],
        [ 48, 49, 55 ], [ 40, 47, 39 ], [ 58, 39, 56 ], [ 31, 58, 30 ], [ 46, 42, 40 ], [ 41, 42, 46 ], [ 35, 43, 37 ], [ 41, 46, 59 ],
        [ 34, 35, 37 ], [ 41, 59, 57 ], [ 37, 57, 34 ], [ 43, 32, 37 ], [  9, 50, 30 ], [  5,  6, 51 ], [  7,  8, 30 ], [ 28, 35, 34 ],
        [ 19, 52, 49 ], [ 22, 23, 39 ], [  3, 41, 57 ], [ 14, 33, 36 ], [ 12, 55, 45 ], [ 21, 31, 53 ], [ 27, 34, 59 ], [  1, 37, 32 ],
        [ 10, 44, 50 ], [  6,  7, 56 ], [ 17, 48, 54 ], [ 11, 45, 44 ], [ 20, 53, 52 ], [ 13, 36, 55 ], [ 25, 46, 40 ], [ 26, 59, 46 ],
        [ 24, 40, 39 ], [  4, 42, 41 ], [ 16, 54, 38 ], [ 18, 49, 48 ], [ 22, 58, 31 ], [  4,  5, 47 ], [  0, 32, 33 ], [  2, 57, 37 ],
        [ 15, 38, 43 ], [ 29, 43, 35 ], [  8,  9, 30 ], [ 47,  5, 51 ], [ 56,  7, 30 ], [ 27, 28, 34 ], [ 18, 19, 49 ], [ 58, 22, 39 ],
        [  2,  3, 57 ], [ 13, 14, 36 ], [ 11, 12, 45 ], [ 20, 21, 53 ], [ 26, 27, 59 ], [  0,  1, 32 ], [  9, 10, 50 ], [ 51,  6, 56 ],
        [ 16, 17, 54 ], [ 10, 11, 44 ], [ 19, 20, 52 ], [ 12, 13, 55 ], [ 24, 25, 40 ], [ 25, 26, 46 ], [ 23, 24, 39 ], [  3,  4, 41 ],
        [ 15, 16, 38 ], [ 17, 18, 48 ], [ 21, 22, 31 ], [ 42,  4, 47 ], [ 14,  0, 33 ], [  1,  2, 37 ], [ 29, 15, 43 ], [ 28, 29, 35 ]
      ]
    },

    { "name": "L",
      "vertex_list": [
        [  0.8197, -0.0654, 0.6820 ], [  0.7217, -0.0654, 0.6820 ], [  0.7217, -0.0654, 0.0000 ], [  1.1277, -0.0654, 0.0000 ],
        [  1.1277, -0.0654, 0.0880 ], [  0.8197, -0.0654, 0.0880 ], [  1.1277,  0.0654, 0.0880 ], [  0.8197,  0.0654, 0.0880 ],
        [  0.8197,  0.0654, 0.6820 ], [  0.7217,  0.0654, 0.0000 ], [  1.1277,  0.0654, 0.0000 ], [  0.7217,  0.0654, 0.6820 ]
      ],
      "element_connections": [
        [ 2,  1, 0 ], [ 2, 0,  5 ], [ 2,  5, 4 ], [ 2, 4,  3 ], [ 9, 8, 11 ], [ 9, 7, 8 ], [ 9, 6, 7 ], [ 9, 10,  6 ],
        [ 3, 10, 9 ], [ 4, 6, 10 ], [ 1, 11, 8 ], [ 2, 9, 11 ], [ 0, 8,  7 ], [ 5, 7, 6 ], [ 2, 3, 9 ], [ 3,  4, 10 ],
        [ 0,  1, 8 ], [ 1, 2, 11 ], [ 5,  0, 7 ], [ 4, 5,  6 ]
      ]
    }

  ]

  f = open ( filename, "w" )
  for o in ol:
    f.write ( o['name'] + " POLYGON_LIST\n" )
    f.write ( "{\n" )

    f.write ( "  VERTEX_LIST\n" )
    f.write ( "  {\n" )
    vl = o['vertex_list']
    for v in vl:
      s = "    ["
      i = 0
      for n in v:
        if n < 0:
          s += " %.4f" % n
        else:
          s += "  %.4f" % n
        if i < 2:
          s += ","
        i += 1
      s += " ]\n"
      f.write ( s )

    f.write ( "  }\n" )

    f.write ( "  ELEMENT_CONNECTIONS\n" )
    f.write ( "  {\n" )
    el = o['element_connections']
    for ec in el:
      s = "    ["
      i = 0
      for n in ec:
        s += " %d" % n
        if i < 2:
          s += ","
        i += 1
      s += " ]\n"
      f.write ( s )

    f.write ( "  }\n" )

    f.write ( "}\n" )

    f.write ( "\n" )


###########################################################################################################
group_name = "Simple Geometry Tests"
test_name = "MDL Geometry Import Test"
operator_name = "cellblender_test.import_geometry"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class MDLGeoImport(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        cb_model.switch_to_orthographic()

        molM = cb_model.add_molecule_species_to_model ( name="M", diff_const_expr="5e-5" )
        molD = cb_model.add_molecule_species_to_model ( name="D", diff_const_expr="1e-5" )
        molL = cb_model.add_molecule_species_to_model ( name="L", diff_const_expr="5e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        molM  = cb_model.get_molecule_species_by_name('M')
        molD  = cb_model.get_molecule_species_by_name('D')
        molL  = cb_model.get_molecule_species_by_name('L')

        cb_model.change_molecule_display ( molM, glyph='Cube', scale=3.0, red=0.0, green=0.7, blue=1.0 )
        cb_model.change_molecule_display ( molD, glyph='Cube', scale=3.0, red=0.0, green=1.0, blue=0.0 )
        cb_model.change_molecule_display ( molL, glyph='Cube', scale=3.0, red=1.0, green=0.0, blue=0.0 )

        cb_model.add_molecule_release_site_to_model ( mol="M",  name="m_rel",  q_expr="1000", d="0", x="-0.7614", y="0", z="0.042", shape="SPHERICAL" )
        cb_model.add_molecule_release_site_to_model ( mol="D",  name="d_rel",  q_expr="1000", d="0", x= "0.0257", y="0", z="0.042", shape="SPHERICAL" )
        cb_model.add_molecule_release_site_to_model ( mol="L",  name="l_rel",  q_expr= "500", d="0", x= "1.0846", y="0", z="0.042", shape="SPHERICAL" )

        f = "mdl_geometry_test.mdl"
        bp = cb_model.path_to_blend
        p = bp[0:bp.rfind(os.sep)]
        fn = p + os.sep + f

        print ( "\n\nWriting Test MDL Geometry File: " + fn )
        write_geometry_file_M_D_L ( fn )

        print ( "Importing Test MDL Geometry File: " + fn + "\n\n" )
        bpy.ops.import_mdl_mesh.mdl(filepath=fn, files=[{"name":f}], directory=p, filter_glob="*.mdl", add_to_model_objects=True)

        cb_model.set_draw_type_for_object ( name="M", draw_type="WIRE" )
        cb_model.set_draw_type_for_object ( name="D", draw_type="WIRE" )
        cb_model.set_draw_type_for_object ( name="L", draw_type="WIRE" )

        cb_model.add_label_to_model ( name="mc", text="Import",   x=-0.65, y=0, z=-0.45,  size=0.5, rx=math.pi/2, ry=0, rz=0 )

        cb_model.run_model ( iterations='500', time_step='1e-6', wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "ddc8c38d8d53bdc3cc4bfee5461684b5a2da2127", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        scn.frame_current = 1
        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.1 )
        cb_model.set_axis_angle ( [0.961, -0.177, -0.213], 1.4253 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
## Shared support functions for dynamic geometry tests


def make_squashed_z_box_script ( subs=[1,1,1], min_len=0.25, max_len=3.5, period_frames=100 ):
    # Produce a dynamic geometry script for a squashed-z cube based on various parameters
    # Search and replace hard-coded portions of the script with the given parameter values
    # Return the modified script as a string
    script = """# This script gets both its inputs and outputs from the environment:
import math

cur_frame = frame_number

####### These fields will be re-written by this script below #######
x_subs=###
y_subs=###
z_subs=###
min_len=###
max_len=###
period_frames=###
####################################################################

size_x = min_len + ( (max_len-min_len) * ( (1 - math.cos ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )
size_y = min_len + ( (max_len-min_len) * ( (1 - math.cos ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )
size_z = min_len + ( (max_len-min_len) * ( (1 - math.sin ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )

# Create a unit box first then resize it later

# For some reason, these list comprehensions wouldn't work in this environment
#xcoords = [ (2*(x-(x_subs/2.0))/x_subs) for x in range(0,x_subs+1) ]
#ycoords = [ (2*(y-(y_subs/2.0))/y_subs) for y in range(0,y_subs+1) ]
#zcoords = [ (2*(z-(z_subs/2.0))/z_subs) for z in range(0,z_subs+1) ]

# Create the coordinate ranges by looping:
xcoords = []
for x in range(0,x_subs+1):
    xcoords.append ( 2*(x-(x_subs/2.0))/x_subs )

ycoords = []
for y in range(0,y_subs+1):
   ycoords.append ( 2*(y-(y_subs/2.0))/y_subs )

zcoords = []
for z in range(0,z_subs+1):
    zcoords.append ( 2*(z-(z_subs/2.0))/z_subs )

# Hard code the ranges to -1 to 1 since the list comprehensions give errors
#xcoords = [ -1.0, 1.0 ]
#ycoords = [ -1.0, 1.0 ]
#zcoords = [ -1.0, 1.0 ]


# Create the top and bottom faces using integer coordinates

faces_index_list = []

# Make the bottom and top (along z)
for x in range(x_subs):
  for y in range(y_subs):
    vertex_0_00 = [x+0,y+0,0]
    vertex_0_01 = [x+1,y+0,0]
    vertex_0_10 = [x+0,y+1,0]
    vertex_0_11 = [x+1,y+1,0]
    faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_01] )
    faces_index_list.append ( [vertex_0_00, vertex_0_10, vertex_0_11] )
    vertex_1_00 = [x+0,y+0,z_subs]
    vertex_1_01 = [x+1,y+0,z_subs]
    vertex_1_10 = [x+0,y+1,z_subs]
    vertex_1_11 = [x+1,y+1,z_subs]
    faces_index_list.append ( [vertex_1_00, vertex_1_01, vertex_1_11] )
    faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_10] )

# Make the right and left (along y)
for x in range(x_subs):
  for z in range(z_subs):
    vertex_0_00 = [x+0,0,z+0]
    vertex_0_01 = [x+1,0,z+0]
    vertex_0_10 = [x+0,0,z+1]
    vertex_0_11 = [x+1,0,z+1]
    faces_index_list.append ( [vertex_0_00, vertex_0_01, vertex_0_11] )
    faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_10] )
    vertex_1_00 = [x+0,y_subs,z+0]
    vertex_1_01 = [x+1,y_subs,z+0]
    vertex_1_10 = [x+0,y_subs,z+1]
    vertex_1_11 = [x+1,y_subs,z+1]
    faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_01] )
    faces_index_list.append ( [vertex_1_00, vertex_1_10, vertex_1_11] )

# Make the back and front (along x)
for y in range(y_subs):
  for z in range(z_subs):
    vertex_0_00 = [0,y+0,z+0]
    vertex_0_01 = [0,y+1,z+0]
    vertex_0_10 = [0,y+0,z+1]
    vertex_0_11 = [0,y+1,z+1]
    faces_index_list.append ( [vertex_0_00, vertex_0_11, vertex_0_01] )
    faces_index_list.append ( [vertex_0_00, vertex_0_10, vertex_0_11] )
    vertex_1_00 = [x_subs,y+0,z+0]
    vertex_1_01 = [x_subs,y+1,z+0]
    vertex_1_10 = [x_subs,y+0,z+1]
    vertex_1_11 = [x_subs,y+1,z+1]
    faces_index_list.append ( [vertex_1_00, vertex_1_01, vertex_1_11] )
    faces_index_list.append ( [vertex_1_00, vertex_1_11, vertex_1_10] )


# Build the faces and the list of points with integer coordinates
faces.clear()
point_inds = []
for fi in faces_index_list:
  f = []
  for pi in fi:
    if not (pi in point_inds):
      point_inds.append(pi)
    f.append ( point_inds.index(pi) )
  faces.append ( f )

# Build the points list from the points index list (one-for-one to match the cube_faces indicies)
points.clear()
for pi in point_inds:
  points.append ( [ size_x*xcoords[pi[0]], size_y*ycoords[pi[1]], size_z*zcoords[pi[2]] ] )
"""

    script = script.replace ( "min_len=###", "min_len=%g" % min_len )
    script = script.replace ( "max_len=###", "max_len=%g" % max_len )
    script = script.replace ( "period_frames=###", "period_frames=%d" % period_frames )
    script = script.replace ( "x_subs=###", "x_subs=%d" % subs[0] )
    script = script.replace ( "y_subs=###", "y_subs=%d" % subs[1] )
    script = script.replace ( "z_subs=###", "z_subs=%d" % subs[2] )
    return ( script )


def DynamicScriptedCubeTest ( context,
                              obj_name="box",
                              mol_types="vs",
                              size=[1.0,1.0,1.0],
                              subs=[1,1,1],
                              dc_2D='1e-4',       # String because it's a CellBlender parameter
                              dc_3D='1e-5',       # String because it's a CellBlender parameter
                              time_step='1e-6',   # String because it's a CellBlender parameter
                              iterations='300',   # String because it's a CellBlender parameter
                              min_len=0.25,
                              max_len=3.5,
                              period_frames=100,
                              mdl_hash="",
                              test_name="Dynamic Geometry Cube",
                              wait_time=30.0, seed=1 ):

    global active_frame_change_handler
    active_frame_change_handler = None


    cb_model = CellBlender_Model ( context, test_name )

    scn = cb_model.get_scene()
    mcell = cb_model.get_mcell()

    cb_model.add_cube_to_model ( name=obj_name, draw_type="BOUNDS" )

    # Copy the script text into a Blender text object named DynGeoScript.py

    script_name = 'DynGeoScript.py'
    print ( "  Script: " + script_name )
    if script_name in bpy.data.texts:
      bpy.data.texts[script_name].clear()
    else:
      bpy.data.texts.new(script_name)
    bpy.data.texts[script_name].write ( make_squashed_z_box_script(subs, min_len, max_len, period_frames) )

    # Modify the object to be dynamic

    mcell.model_objects.object_list[obj_name].dynamic = True
    mcell.model_objects.object_list[obj_name].script_name = script_name
    mcell.model_objects.object_list[obj_name].dynamic_display_source = 'script'


    if "v" in mol_types: molv = cb_model.add_molecule_species_to_model ( name="v", mol_type="3D", diff_const_expr=dc_3D )
    if "s" in mol_types: mols = cb_model.add_molecule_species_to_model ( name="s", mol_type="2D", diff_const_expr=dc_2D )

    ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
    ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!
    if "v" in mol_types: molv  = cb_model.get_molecule_species_by_name('v')
    if "s" in mol_types: mols  = cb_model.get_molecule_species_by_name('s')

    if "v" in mol_types: cb_model.add_molecule_release_site_to_model ( mol="v", shape="OBJECT", obj_expr=obj_name, q_expr="1000" )
    if "s" in mol_types: cb_model.add_molecule_release_site_to_model ( mol="s", shape="OBJECT", obj_expr=obj_name, q_expr="1000" )

    if "v" in mol_types: cb_model.change_molecule_display ( molv, glyph='Cube', scale=3.0, red=1.0, green=1.0, blue=1.0 )
    if "s" in mol_types: cb_model.change_molecule_display ( mols, glyph='Cone', scale=5.0, red=0.0, green=1.0, blue=0.1 )

    mcell.initialization.large_molecular_displacement = 'IGNORED'

    cb_model.run_model ( iterations=iterations, time_step=time_step, wait_time=wait_time )

    # Check whether the test passed or not
    cb_model.compare_mdl_with_sha1 ( "", test_name=test_name )

    # Set up the view as desired for this model

    cb_model.refresh_molecules()
    cb_model.select_none()
    cb_model.set_view_back()
    cb_model.switch_to_orthographic()
    cb_model.scale_view_distance ( 1.5 )
    cb_model.set_axis_angle ( [0.961, -0.177, -0.213], 1.4253 )
    cb_model.scale_view_distance ( 0.25 )
    cb_model.hide_manipulator ( hide=True )

    return cb_model






###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Cube Test Minimal Geometry"
operator_name = "cellblender_test.dynamic_cube_test_minimal"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class DynCubeTestMinimalGeomOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = DynamicScriptedCubeTest ( context, time_step='1e-06', iterations='300', period_frames=100, min_len=0.25, max_len=3.5, mdl_hash="3667bfa5bfba57320581eb37f0b3b1c9c8ed2145", test_name=self.self_test_name, wait_time=15.0, seed=1 )

        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Cube Test Volume Only"
operator_name = "cellblender_test.dynamic_cube_test_vol_only"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class DynCubeTestVolOnlyOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = DynamicScriptedCubeTest ( context, mol_types="v", dc_2D='1e-7', dc_3D='1e-7', time_step='1e-6', iterations='300', period_frames=100, min_len=0.25, max_len=3.5, mdl_hash="69aaace54f2eebbd7963a9a5892cc9c2d19f0ef1", test_name=self.self_test_name, wait_time=15.0, seed=1 )

        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }




###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Cube Test Surface Only"
operator_name = "cellblender_test.dynamic_cube_test_surf_only"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class DynCubeTestSurfOnlyOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = DynamicScriptedCubeTest ( context, mol_types="s", dc_2D='1e-7', dc_3D='1e-7', time_step='1e-6', iterations='300', period_frames=100, min_len=0.25, max_len=3.5, mdl_hash="d7506ce0f5063b723ba4b8df8ccacd04a47f5115", test_name=self.self_test_name, wait_time=15.0, seed=1 )

        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }






###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Geometry - Cube with 10 Z-Slices"
operator_name = "cellblender_test.dynamic_cube_test_10_z_slices"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class DynCubeTestVolOnlyZ10Op(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = DynamicScriptedCubeTest ( context, subs=[1,1,10], time_step='1e-6', iterations='300', period_frames=100, min_len=0.25, max_len=3.5, mdl_hash="3667bfa5bfba57320581eb37f0b3b1c9c8ed2145", test_name=self.self_test_name, wait_time=15.0, seed=1 )
        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }







###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Tapered Cube Test"
operator_name = "cellblender_test.dynamic_tapered_cube"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

dyn_tapered_cube_script = """# This script gets both its inputs and outputs from the environment:
#
#  frame_number is the frame number indexed from the start of the simulation
#  time_step is the amount of time between each frame (same as CellBlender's time_step)
#  points [] is a list of points where each point is a list of 3 doubles: x, y, z
#  faces [] is a list of faces where each face is a list of 3 integer indexes of points (0 based)
#  regions_dict {} is a dictionary of regions
#  region_props {} is a dictionary of region properties
#  origin [0,0,0] is a list of 3 coordinates for the origin of this object
#
# This script must fill out the points and faces lists for the time given by frame_number and time_step.
# It may also change the regions and origin for each frame
# CellBlender will call this function repeatedly to create the dynamic MDL and possibly during display.

import math

points.clear()
faces.clear()

min_length = 0.5
max_length = 1.0
period_frames = 100

sx = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * frame_number / period_frames )) / 2 ) )
sy = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * frame_number / period_frames )) / 2 ) )
sz = min_length + ( (max_length-min_length) * ( (1 - math.sin ( 2 * math.pi * frame_number / period_frames )) / 2 ) )
sz = 2 * sz

# These define the coordinates of the rectangular box
points.append ( [  sx,  sy, -sz ] )
points.append ( [  sx, -sy, -sz ] )
points.append ( [ -sx, -sy, -sz ] )
points.append ( [ -sx,  sy, -sz ] )
points.append ( [  sx,  sy,  sz ] )
points.append ( [  sx, -sy,  sz ] )
points.append ( [ -sx, -sy,  sz ] )
points.append ( [ -sx,  sy,  sz ] )

# These define the faces of the rectangular box
faces.append ( [ 1, 2, 3 ] )
faces.append ( [ 7, 6, 5 ] )
faces.append ( [ 4, 5, 1 ] )
faces.append ( [ 5, 6, 2 ] )
faces.append ( [ 2, 6, 7 ] )
faces.append ( [ 0, 3, 7 ] )
faces.append ( [ 0, 1, 3 ] )
faces.append ( [ 4, 7, 5 ] )
faces.append ( [ 0, 4, 1 ] )
faces.append ( [ 1, 5, 2 ] )
faces.append ( [ 3, 2, 7 ] )
faces.append ( [ 4, 0, 7 ] )

# Taper the box to get a different shape
for i in range(len(points)):
    if points[i][2] > 0:
        # z coordinate is greater than 0 so shrink x and y coordinates
        points[i][0] = points[i][0] * 0.2
        points[i][1] = points[i][1] * 0.2
    else:
        # z coordinate is less than or equal to 0 so expand x and y coordinates
        points[i][0] = points[i][0] * 2
        points[i][1] = points[i][1] * 2
"""

class DynTaperedCubeTest(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        obj_name = "Cell"

        cb_model.add_cube_to_model ( name=obj_name, draw_type="WIRE" )

        # Copy the script text into a Blender text object named DynGeoScript.py

        script_name = 'DynGeoScript.py'
        print ( "  Script: " + script_name )
        if script_name in bpy.data.texts:
          bpy.data.texts[script_name].clear()
        else:
          bpy.data.texts.new(script_name)
        bpy.data.texts[script_name].write ( dyn_tapered_cube_script )

        # Modify the object to be dynamic

        mcell.model_objects.object_list[obj_name].dynamic = True
        mcell.model_objects.object_list[obj_name].script_name = script_name
        mcell.model_objects.object_list[obj_name].dynamic_display_source = 'script'

        # Build the rest of the model

        mol = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-3" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol  = cb_model.get_molecule_species_by_name('a')

        cb_model.change_molecule_display ( mol, glyph='Cube', scale=4.0, red=1.0, green=0.0, blue=0.0 )

        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="Cell", q_expr="1000" )

        cb_model.run_model ( iterations='200', time_step='1e-6', wait_time=2.0 )

        cb_model.compare_mdl_with_sha1 ( "c3a9d9fbd7f064bbf60a36bb895fdd992625f7de", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.5 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }


###########################################################################################################
group_name = "Dynamic Geometry Tests"
test_name = "Dynamic Icosphere Test"
operator_name = "cellblender_test.dynamic_icosphere_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )


class DynIcosphereTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def create_cell ( self, scene, frame_num=None ):

        cur_frame = frame_num
        if cur_frame == None:
          cur_frame = scene.frame_current

        # OK:   (0.8,1.2), (0.5,1.5)
        # Fail: (0.5,3.0), (0.5,2.0)
        min_length = 0.5
        max_length = 2.0
        period_frames = 100

        size_x = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )
        size_y = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )
        size_z = min_length + ( (max_length-min_length) * ( (1 - math.sin ( 2 * math.pi * cur_frame / period_frames )) / 2 ) )

        #return IcoSphere ( 2 )
        return IcoSphere ( 2, scale_x=size_x, scale_y=size_y, scale_z=size_z )


    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        dyn_icosphere_script = """# This script gets both its inputs and outputs from the environment:
#
#  frame_number is the frame number indexed from the start of the simulation
#  time_step is the amount of time between each frame (same as CellBlender's time_step)
#  points [] is a list of points where each point is a list of 3 doubles: x, y, z
#  faces [] is a list of faces where each face is a list of 3 integer indexes of points (0 based)
#  regions_dict {} is a dictionary of regions
#  region_props {} is a dictionary of region properties
#  origin [0,0,0] is a list of 3 coordinates for the origin of this object
#
# This script must fill out the points and faces lists for the time given by frame_number and time_step.
# It may also change the regions and origin for each frame
# CellBlender will call this function repeatedly to create the dynamic MDL and possibly during display.

import math
import cellblender_test_suite as cbts

min_length = 0.5
max_length = 2.0
period_frames = 100

size_x = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * frame_number / period_frames )) / 2 ) )
size_y = min_length + ( (max_length-min_length) * ( (1 - math.cos ( 2 * math.pi * frame_number / period_frames )) / 2 ) )
size_z = min_length + ( (max_length-min_length) * ( (1 - math.sin ( 2 * math.pi * frame_number / period_frames )) / 2 ) )

ico = cbts.IcoSphere ( 2, scale_x=size_x, scale_y=size_y, scale_z=size_z )

points.clear()
faces.clear()

for p in ico.points:
    points.append ( [p.x, p.y, p.z] )

for f in ico.faces:
    faces.append ( [ f.verts[0], f.verts[1], f.verts[2] ] )

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

"""


        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        obj_name = "Cell"

        cb_model.add_cube_to_model ( name=obj_name, draw_type="WIRE" )
        # cb_model.add_active_object_to_model ( name="cell", draw_type="WIRE" )

        # Copy the script text into a Blender text object named DynGeoScript.py

        script_name = 'DynGeoScript.py'
        print ( "  Script: " + script_name )
        if script_name in bpy.data.texts:
          bpy.data.texts[script_name].clear()
        else:
          bpy.data.texts.new(script_name)
        bpy.data.texts[script_name].write ( dyn_icosphere_script )

        # Modify the object to be dynamic

        mcell.model_objects.object_list[obj_name].dynamic = True
        mcell.model_objects.object_list[obj_name].script_name = script_name
        mcell.model_objects.object_list[obj_name].dynamic_display_source = 'script'

        # Build the rest of the model


        molv = cb_model.add_molecule_species_to_model ( name="v", mol_type="3D", diff_const_expr="1e-5" )
        mols = cb_model.add_molecule_species_to_model ( name="s", mol_type="2D", diff_const_expr="1e-4" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        molv  = cb_model.get_molecule_species_by_name('v')
        mols  = cb_model.get_molecule_species_by_name('s')

        cb_model.add_molecule_release_site_to_model ( mol="v", shape="OBJECT", obj_expr=obj_name, q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( mol="s", shape="OBJECT", obj_expr=obj_name, q_expr="1000" )


        cb_model.decouple_export_and_run ( context )

        #cb_model.export_model ( iterations='300', time_step='1e-6', seed=2, export_format="mcell_mdl_modular" )
        cb_model.export_model ( iterations='300', time_step='1e-6', seed=2 )


        # Update the main MDL file Scene.main.mdl to insert the DYNAMIC_GEOMETRY directive



        cb_model.run_only ( wait_time=30.0, seed=2 )

        cb_model.compare_mdl_with_sha1 ( "98fca76aa30e8f801c182f9bc5b0d4ae617ede60", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.change_molecule_display ( molv, glyph='Cube', scale=3.0, red=1.0, green=1.0, blue=1.0 )
        cb_model.change_molecule_display ( mols, glyph='Cone', scale=5.0, red=0.0, green=1.0, blue=0.1 )

        cb_model.set_view_back()

        cb_model.switch_to_orthographic()
        # cb_model.set_axis_angle ( [0, 1, 0], 0 )
        cb_model.scale_view_distance ( 0.7 )
        cb_model.set_axis_angle ( [0.961, -0.177, -0.213], 1.4253 )

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }






###########################################################################################################
group_name = "Counting Tests"
test_name = "Simple Molecule Count Test"
operator_name = "cellblender_test.simple_molecule_count_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SimpleMoleculeCountTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):
    
        global active_frame_change_handler
        active_frame_change_handler = None

        print ( str(test_groups) )

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        mol_a = cb_model.add_molecule_species_to_model ( name="a", diff_const_expr="1e-6" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a  = cb_model.get_molecule_species_by_name('a')

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="500", d="0.5" )
        cb_model.add_reaction_to_model ( name="Decay", rin="a",  rtype="irreversible", rout="NULL", fwd_rate="1e5", bkwd_rate="" )

        cb_model.add_count_output_to_model ( mol_name="a", rxn_name=None, object_name=None, region_name=None, count_location="World" )
        cb_model.add_count_output_to_model ( mol_name=None, rxn_name="Decay", object_name=None, region_name=None, count_location="World" )


        cb_model.run_model ( iterations='100', time_step='1e-6', wait_time=3.0 )

        cb_model.compare_mdl_with_sha1 ( "b35a4dc33ba608930b208c1b0f5951ce800e9ec8", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()

        cb_model.change_molecule_display ( mol_a, glyph='Cube', scale=2.0, red=1.0, green=0.0, blue=0.0 )
        cb_model.set_view_back()
        cb_model.scale_view_distance ( 0.1 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }




###########################################################################################################
group_name = "Counting Tests"
test_name = "Release Time Patterns Test"
operator_name = "cellblender_test.rel_time_patterns_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class ReleaseTimePatternsTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        diff_const = "0"

        mol_a =  cb_model.add_molecule_species_to_model ( name="a",  diff_const_expr=diff_const )
        mol_b =  cb_model.add_molecule_species_to_model ( name="b",  diff_const_expr=diff_const )
        mol_bg = cb_model.add_molecule_species_to_model ( name="bg", diff_const_expr="0" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a   = cb_model.get_molecule_species_by_name('a')
        mol_b   = cb_model.get_molecule_species_by_name('b')
        mol_bg  = cb_model.get_molecule_species_by_name('bg')

        decay_rate = "8e6"
        cb_model.add_reaction_to_model ( rin="a",  rtype="irreversible", rout="NULL", fwd_rate=decay_rate, bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="b",  rtype="irreversible", rout="NULL", fwd_rate=decay_rate+"/5", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="bg", rtype="irreversible", rout="NULL", fwd_rate=decay_rate+"/500", bkwd_rate="" )


        dt = "1e-6"
        cb_model.add_release_pattern_to_model ( name="spike_pattern", delay="300 * " + dt, release_interval="10 * " + dt, train_duration="100 * " + dt, train_interval="200 * " + dt, num_trains="5" )
        cb_model.add_release_pattern_to_model ( name="background", delay="0", release_interval="100 * " + dt, train_duration="1e20", train_interval="2e20", num_trains="1" )


        num_rel = "10"

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr=num_rel, shape="SPHERICAL", d="0.1", z="0.2", pattern="spike_pattern" )
        cb_model.add_molecule_release_site_to_model ( mol="b", q_expr=num_rel, shape="SPHERICAL", d="0.1", z="0.4", pattern="spike_pattern" )
        cb_model.add_molecule_release_site_to_model ( mol="bg", q_expr="1",    shape="SPHERICAL", d="1.0", z="0.0", pattern="background" )

        #### Add a single a molecule so the display values can be set ... otherwise they're not applied properly
        cb_model.add_molecule_release_site_to_model ( mol="a",  name="a_dummy",  q_expr="1", shape="SPHERICAL" )
        #### Add a single b molecule so the display values can be set ... otherwise they're not applied properly
        cb_model.add_molecule_release_site_to_model ( mol="b",  name="b_dummy",  q_expr="1", shape="SPHERICAL" )
        #### Add a single b molecule so the display values can be set ... otherwise they're not applied properly
        cb_model.add_molecule_release_site_to_model ( mol="bg", name="bg_dummy", q_expr="1", shape="SPHERICAL" )


        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[0].molecule_name = 'a'

        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[1].molecule_name = 'b'

        bpy.ops.mcell.rxn_output_add()
        mcell.rxn_output.rxn_output_list[2].molecule_name = 'bg'


        cb_model.run_model ( iterations='1500', time_step=dt, wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "61639ba5586eb57aa327f80cff3922d5bd08fc06", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        mol_scale = 1.0

        cb_model.change_molecule_display ( mol_a,  glyph='Cube',  scale=mol_scale, red=1.0, green=0.0, blue=0.0 )
        cb_model.change_molecule_display ( mol_b,  glyph='Cube',  scale=mol_scale, red=0.5, green=0.5, blue=1.0 )
        cb_model.change_molecule_display ( mol_bg, glyph='Torus', scale=mol_scale, red=1.0, green=1.0, blue=1.0 )

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.05 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
##   Main Function supporting Lotka Volterra models

def LotkaVolterraTorus ( context, prey_birth_rate, predation_rate, pred_death_rate, interaction_radius, time_step, iterations, mdl_hash, test_name, wait_time ):

    cb_model = CellBlender_Model ( context, test_name )

    scn = cb_model.get_scene()
    mcell = cb_model.get_mcell()

    # Create the Torus
    # bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=10,major_radius=0.1,minor_radius=0.03)
    
    cb_model.add_fixed_torus_to_model ( name="arena" )
    # cb_model.add_cube_to_model ( name="arena" )
    
    ###scn.objects.active.name = 'arena'

    # Set up the material for the Torus
    if len(bpy.data.materials) <= 0:
        new_mat = bpy.data.materials.new("cell")
    bpy.data.materials[0].name = 'cell'
    bpy.data.materials['cell'].use_transparency = True
    bpy.data.materials['cell'].alpha = 0.3

    # Assign the material to the Torus
    bpy.ops.object.material_slot_add()
    scn.objects['arena'].material_slots[0].material = bpy.data.materials['cell']
    scn.objects['arena'].show_transparent = True

    # Add the new Torus to the model objects list
    mcell.cellblender_main_panel.objects_select = True
    bpy.ops.mcell.model_objects_add()

    # Add the molecules
    prey = cb_model.add_molecule_species_to_model ( name="prey", diff_const_expr="6e-6" )
    pred = cb_model.add_molecule_species_to_model ( name="predator", diff_const_expr="6e-6" )

    ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
    ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

    prey = cb_model.get_molecule_species_by_name('prey')
    pred = cb_model.get_molecule_species_by_name('predator')

    cb_model.add_molecule_release_site_to_model ( name="prey_rel", mol="prey", shape="OBJECT", obj_expr="arena", q_expr="1000" )
    cb_model.add_molecule_release_site_to_model ( name="pred_rel", mol="predator", shape="OBJECT", obj_expr="arena", q_expr="1000" )

    cb_model.add_reaction_to_model ( rin="prey", rtype="irreversible", rout="prey + prey", fwd_rate=prey_birth_rate, bkwd_rate="" )
    cb_model.add_reaction_to_model ( rin="prey + predator", rtype="irreversible", rout="predator + predator", fwd_rate=predation_rate, bkwd_rate="" )
    cb_model.add_reaction_to_model ( rin="predator", rtype="irreversible", rout="NULL", fwd_rate=pred_death_rate, bkwd_rate="" )

    bpy.ops.mcell.rxn_output_add()
    mcell.rxn_output.rxn_output_list[0].molecule_name = 'prey'

    bpy.ops.mcell.rxn_output_add()
    mcell.rxn_output.rxn_output_list[1].molecule_name = 'predator'

    mcell.rxn_output.plot_layout = ' '

    mcell.partitions.include = True
    bpy.ops.mcell.auto_generate_boundaries()

    if interaction_radius == None:
        mcell.initialization.interaction_radius.set_expr ( "" )
    else:
        mcell.initialization.interaction_radius.set_expr ( interaction_radius )

    # mcell.run_simulation.simulation_run_control = 'JAVA'
    cb_model.run_model ( iterations=iterations, time_step=time_step, wait_time=wait_time )

    cb_model.compare_mdl_with_sha1 ( mdl_hash, test_name=test_name )

    cb_model.refresh_molecules()

    scn.frame_current = 10

    cb_model.set_view_back()

    mcell.rxn_output.mol_colors = True

    cb_model.change_molecule_display ( prey, glyph='Cube',       scale=0.2, red=0.0, green=1.0, blue=0.0 )
    cb_model.change_molecule_display ( pred, glyph='Octahedron', scale=0.3, red=1.0, green=0.0, blue=0.0 )

    cb_model.scale_view_distance ( 0.015 )

    return cb_model



###########################################################################################################
group_name = "Complete Model Tests"
test_name = "Lotka Volterra Torus - Diffusion Limited Reaction"
operator_name = "cellblender_test.lotka_volterra_torus_test_diff_lim"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class LotkaVolterraTorusTestDiffLimOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = LotkaVolterraTorus ( context, prey_birth_rate="8.6e6", predation_rate="1e12", pred_death_rate="5e6", interaction_radius="0.003", time_step="1e-8", iterations="1200", mdl_hash="5beae6fabdb57b3245403491edfc2c32ebcb1f00", test_name=self.self_test_name, wait_time=15.0 )
        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Complete Model Tests"
test_name = "Lotka Volterra Torus - Physiologic Reaction"
operator_name = "cellblender_test.lotka_volterra_torus_test_phys"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class LotkaVolterraTorusTestPhysOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = LotkaVolterraTorus ( context, prey_birth_rate="129e3", predation_rate="1e8", pred_death_rate="130e3", interaction_radius=None, time_step="1e-6", iterations="1200", mdl_hash="4ed241042418f86e99291ad285c1a6cde9e57427", test_name=self.self_test_name, wait_time=60.0 )
        cb_model.hide_manipulator ( hide=True )
        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################
group_name = "Complete Model Tests"
test_name = "Organelle Test"
operator_name = "cellblender_test.organelle_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class OrganelleTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()


        # Set some shared parameters
        subdiv = 3

        # Set up a transparent material for the cell membranes
        if len(bpy.data.materials) <= 0:
            new_mat = bpy.data.materials.new("membrane")
        bpy.data.materials[0].name = 'membrane'
        bpy.data.materials['membrane'].use_transparency = True
        bpy.data.materials['membrane'].alpha = 0.25

        # Create Organelle 1

        # Create the object and add it to the CellBlender model
        cb_model.add_icosphere_to_model ( name="Organelle_1", draw_type="SOLID", size=0.3, y=-0.25, subdiv=subdiv+1 )
        cb_model.add_surface_region_to_model_object_by_normal ( "Organelle_1", "top", 0, 1, 0, 0.92 )
        bpy.ops.object.material_slot_add()
        scn.objects['Organelle_1'].material_slots[0].material = bpy.data.materials['membrane']
        scn.objects['Organelle_1'].show_transparent = True

        # Create Organelle 2

        # Create the object and add it to the CellBlender model
        cb_model.add_icosphere_to_model ( name="Organelle_2", draw_type="SOLID", size=0.2, y=0.31, subdiv=subdiv+1 )
        cb_model.add_surface_region_to_model_object_by_normal ( "Organelle_2", "top", 0, -1, 0, 0.8 )
        bpy.ops.object.material_slot_add()
        scn.objects['Organelle_2'].material_slots[0].material = bpy.data.materials['membrane']
        scn.objects['Organelle_2'].show_transparent = True


        # Create Cell itself

        cb_model.add_icosphere_to_model ( name="Cell", draw_type="SOLID", size=0.625, subdiv=subdiv )
        bpy.ops.object.material_slot_add()
        scn.objects['Cell'].material_slots[0].material = bpy.data.materials['membrane']
        scn.objects['Cell'].show_transparent = True


        # Define the molecule species

        mola = cb_model.add_molecule_species_to_model ( name="a", mol_type="3D", diff_const_expr="1e-6" )
        molb = cb_model.add_molecule_species_to_model ( name="b", mol_type="3D", diff_const_expr="1e-6" )
        molc = cb_model.add_molecule_species_to_model ( name="c", mol_type="3D", diff_const_expr="1e-6" )
        mold = cb_model.add_molecule_species_to_model ( name="d", mol_type="3D", diff_const_expr="1e-6" )

        molt1 = cb_model.add_molecule_species_to_model ( name="t1", mol_type="2D", diff_const_expr="1e-7" )
        molt2 = cb_model.add_molecule_species_to_model ( name="t2", mol_type="2D", diff_const_expr="1e-8" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mola  = cb_model.get_molecule_species_by_name('a')
        molb  = cb_model.get_molecule_species_by_name('b')
        molc  = cb_model.get_molecule_species_by_name('c')
        mold  = cb_model.get_molecule_species_by_name('d')
        molt1 = cb_model.get_molecule_species_by_name('t1')
        molt2 = cb_model.get_molecule_species_by_name('t2')
        
        cb_model.change_molecule_display ( mola, glyph='Letter', letter='A', scale=1.0, red=0.0, green=0.0, blue=0.8, emit=1.0 )
        cb_model.change_molecule_display ( molb, glyph='Letter', letter='B', scale=1.0, red=0.0, green=0.8, blue=0.8, emit=0.8 )
        cb_model.change_molecule_display ( molc, glyph='Letter', letter='C', scale=2.0, red=1.0, green=0.2, blue=1.0, emit=2.0 )
        cb_model.change_molecule_display ( mold, glyph='Cube', scale=2.0, red=1.0, green=1.0, blue=1.0 )

        cb_model.change_molecule_display ( molt1, glyph='Cone', scale=1.3, red=0.0, green=0.8, blue=0.0 )
        cb_model.change_molecule_display ( molt2, glyph='Receptor', scale=1.0, red=0.8, green=0.0, blue=0.0 )


        cb_model.add_molecule_release_site_to_model ( name="rel_a",  mol="a",  shape="OBJECT", obj_expr="Cell[ALL] - (Organelle_1[ALL] + Organelle_2[ALL])", q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( name="rel_b",  mol="b",  shape="OBJECT", obj_expr="Organelle_1[ALL]", q_expr="1000" )
        cb_model.add_molecule_release_site_to_model ( name="rel_t1", mol="t1", shape="OBJECT", obj_expr="Organelle_1[top]", orient="'", q_expr="700" )
        cb_model.add_molecule_release_site_to_model ( name="rel_t2", mol="t2", shape="OBJECT", obj_expr="Organelle_2[top]", orient="'", q_expr="700" )


        cb_model.add_reaction_to_model ( rin="a + b",    rtype="irreversible", rout="c",        fwd_rate="1e9", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="a' + t1'", rtype="irreversible", rout="a, + t1'", fwd_rate="3e8", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="c' + t2'", rtype="irreversible", rout="d, + t2'", fwd_rate="3e9", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="c, + t1'", rtype="irreversible", rout="c' + t1'", fwd_rate="3e8", bkwd_rate="" )

        cb_model.add_count_output_to_model ( mol_name="a" )
        cb_model.add_count_output_to_model ( mol_name="b" )
        cb_model.add_count_output_to_model ( mol_name="c" )
        cb_model.add_count_output_to_model ( mol_name="d" )

        #cb_model.add_count_output_to_model ( mol_name="t1" )
        #cb_model.add_count_output_to_model ( mol_name="t2" )

        mcell.rxn_output.plot_layout = ' '
        mcell.rxn_output.mol_colors = True


        mcell.partitions.include = True
        bpy.ops.mcell.auto_generate_boundaries()


        cb_model.run_model ( iterations='1000', time_step='1e-6', wait_time=25.0 )

        cb_model.compare_mdl_with_sha1 ( "169ab78d07b4583655f55da36807efd9417290fd", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        scn.frame_current = 2

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.07 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



###########################################################################################################

# Capsule is 1 BU in diameter (0.5 in radius) and has a total height of 4 (-2 to +2)
group_name = "Complete Model Tests"
test_name = "E. coli MinD/MinE System"
operator_name = "cellblender_test.mind_mine_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class MinDMinETestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()


        # Define the parameters to be used later

        cb_model.add_parameter_to_model ( name="k1", expr="1", units="s-1", desc="k1" )
        cb_model.add_parameter_to_model ( name="k2", expr="3.8e3", units="M-1s-1", desc="k2" )
        cb_model.add_parameter_to_model ( name="k3", expr="9e5", units="M-1s-1", desc="k3" )
        cb_model.add_parameter_to_model ( name="k4", expr="5.6e7", units="M-1s-1", desc="k4" )
        cb_model.add_parameter_to_model ( name="k5", expr="0.7", units="s-1", desc="k5" )
        cb_model.add_parameter_to_model ( name="dte", expr="2e-6", units="", desc="dte" )
        cb_model.add_parameter_to_model ( name="dt", expr="100*dte", units="", desc="dt" )


        # Create the capsule object, and define the surface as a membrane

        cb_model.add_capsule_to_model ( name="ecoli", draw_type="SOLID", x=0, y=0, z=0, sigma=0, subdiv=2, radius=0.5, cyl_len=3 )
        cb_model.add_surface_region_to_model_object_by_normal ( "ecoli", "membrane" )

        # Set up the material for the cell
        if len(bpy.data.materials) <= 0:
            new_mat = bpy.data.materials.new("ecoli")
        bpy.data.materials[0].name = 'ecoli'
        bpy.data.materials['ecoli'].use_transparency = True
        bpy.data.materials['ecoli'].alpha = 0.25

        # Assign the material to the cell
        bpy.ops.object.material_slot_add()
        scn.objects['ecoli'].material_slots[0].material = bpy.data.materials['ecoli']
        scn.objects['ecoli'].show_transparent = True

        # Create a surface class and assign it to the membrane

        cb_model.add_surface_class_to_model ( "surf" )
        cb_model.assign_surface_class_to_region ( "surf", "ecoli", "membrane" )


        # Define the molecule species

        mind_adp = cb_model.add_molecule_species_to_model ( name="mind_adp", mol_type="3D", diff_const_expr="2.5e-8" )
        mind_atp = cb_model.add_molecule_species_to_model ( name="mind_atp", mol_type="3D", diff_const_expr="2.5e-8" )
        mine     = cb_model.add_molecule_species_to_model ( name="mine",     mol_type="3D", diff_const_expr="2.5e-8", custom_time_step="dte" )
        mind_m   = cb_model.add_molecule_species_to_model ( name="mind_m",   mol_type="2D", diff_const_expr="0" )
        minde_m  = cb_model.add_molecule_species_to_model ( name="minde_m",  mol_type="2D", diff_const_expr="0" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mind_adp = cb_model.get_molecule_species_by_name('mind_adp')
        mind_atp = cb_model.get_molecule_species_by_name('mind_atp')
        mine     = cb_model.get_molecule_species_by_name('mine')
        mind_m   = cb_model.get_molecule_species_by_name('mind_m')
        minde_m  = cb_model.get_molecule_species_by_name('minde_m')

        # Set the molecule glyphs
        cb_model.change_molecule_display ( mind_adp, glyph='Icosahedron', scale=1.0, red=0.8, green=0.0, blue=0.0, emit=0.0 )
        cb_model.change_molecule_display ( mind_atp, glyph='Icosahedron', scale=1.0, red=0.0, green=0.5, blue=0.0, emit=0.0 )
        cb_model.change_molecule_display ( mine,     glyph='Icosahedron', scale=1.0, red=0.0, green=0.0, blue=0.5, emit=1.0 )
        cb_model.change_molecule_display ( mind_m,   glyph='Icosahedron', scale=1.5, red=0.0, green=1.0, blue=0.0, emit=2.0 )
        cb_model.change_molecule_display ( minde_m,  glyph='Icosahedron', scale=1.5, red=1.0, green=0.0, blue=1.0, emit=2.0 )


        # Define the release sites

        cb_model.add_molecule_release_site_to_model ( name="mind_rel",  mol="mind_adp",  shape="OBJECT", obj_expr="ecoli", q_expr="4320" )
        cb_model.add_molecule_release_site_to_model ( name="mine_rel",  mol="mine",      shape="OBJECT", obj_expr="ecoli", q_expr="1080" )


        # Define the reactions

        cb_model.add_reaction_to_model ( rin="mind_adp",             rtype="irreversible", rout="mind_atp",           fwd_rate="k1", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="mind_atp, @ surf'",    rtype="irreversible", rout="mind_m,",            fwd_rate="k2", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="mind_atp, + mind_m,",  rtype="irreversible", rout="mind_m, + mind_m,",  fwd_rate="k3", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="mind_atp, + minde_m,", rtype="irreversible", rout="mind_m, + minde_m,", fwd_rate="k3", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="mine, + mind_m,",      rtype="irreversible", rout="minde_m,",           fwd_rate="k4", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="minde_m,",             rtype="irreversible", rout="mind_adp, + mine,",  fwd_rate="k5", bkwd_rate="" )

        # Specify the output

        cb_model.add_count_output_to_model ( mol_name="mind_adp" )
        cb_model.add_count_output_to_model ( mol_name="mind_atp" )
        cb_model.add_count_output_to_model ( mol_name="mind_m" )
        cb_model.add_count_output_to_model ( mol_name="minde_m" )
        cb_model.add_count_output_to_model ( mol_name="mine" )

        # Set a few special parameters
        mcell.initialization.time_step_max.set_expr('100*dt')
        mcell.initialization.interaction_radius.set_expr('1e-5')
        mcell.initialization.vacancy_search_distance.set_expr('0.08')
        mcell.initialization.surface_grid_density.set_expr('4000')
        mcell.initialization.surface_grid_density.set_expr('4000')
        mcell.initialization.accurate_3d_reactions = False

        # Setup the partitions

        cb_model.set_partitions ( xs=-0.5, xe=0.5, xd=0.02, ys=-0.5, ye=0.5, yd=0.02, zs=-2.0, ze=2.0, zd=0.2 )

        # Setup the visualization

        cb_model.set_visualization ( enable_visualization=True, export_all=True, all_iterations=False, start=0, end=6000000, step=1000 )

        cb_model.run_model ( iterations='0.8 * 200/dt', time_step='dt', wait_time=5.0 )  # Can use to generate MDL, but SHA1 won't be right: export_format="mcell_mdl_modular", 

        cb_model.compare_mdl_with_sha1 ( "ecd38f44858e26219dcea028a2956fed20d94c24", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()


        return { 'FINISHED' }



###########################################################################################################
group_name = "Complete Model Tests"
test_name = "Simple Synapse Model"
operator_name = "cellblender_test.simple_synapse_model"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class SimpleSynapseTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()

        # Create a synapse

        gap = 0.07  # A 300nm active area might have a 20nm gap

        spine_head_shape = [ (3.5,0), (3.5,0.45), (1.45,0.45), (1.2,0.5), (1.0,0.6), (0.7,0.8), (0.5,0.9), (0.3,0.9), (0.15,0.82), (0.048,0.7), (0.0,0.5), (0.0,0.45), (0.0,0.3), (0.0,0.15), (0.0,0.0) ]
        spine_head_pre_shape = []
        for p in spine_head_shape:
            # Append to the end to get the correct order for outward facing normals
            spine_head_pre_shape.append ( (-p[0]-(gap/2),p[1] ) )
        spine_head_post_shape = []
        for p in spine_head_shape:
            # Prepend to the front to get the correct order for outward facing normals
            spine_head_post_shape.insert ( 0, (p[0]+(gap/2),p[1] ) )

        cb_model.add_shaped_cylinder_to_model ( name="neuron_pre", draw_type="WIRE", x=0, y=0, z=0, sigma=0, numsect=10, z_profile=spine_head_pre_shape )
        cb_model.add_surface_region_to_model_object_by_normal ( "neuron_pre", "synapse_pre", 0, 0, 1, 0.99 )

        cb_model.add_shaped_cylinder_to_model ( name="neuron_post", draw_type="WIRE", x=0, y=0, z=0, sigma=0, numsect=10, z_profile=spine_head_post_shape )
        cb_model.add_surface_region_to_model_object_by_normal ( "neuron_post", "synapse_post", 0, 0, -1, 0.99 )


        mol_a       = cb_model.add_molecule_species_to_model ( name="a",      mol_type="3D", diff_const_expr="1e-5" )
        mol_nt      = cb_model.add_molecule_species_to_model ( name="nt",     mol_type="3D", diff_const_expr="2e-7" )
        mol_s_pre   = cb_model.add_molecule_species_to_model ( name="s_pre",  mol_type="2D", diff_const_expr="0" )
        mol_s_post  = cb_model.add_molecule_species_to_model ( name="s_post", mol_type="2D", diff_const_expr="0" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a       = cb_model.get_molecule_species_by_name("a")
        mol_nt      = cb_model.get_molecule_species_by_name("nt")
        mol_s_pre   = cb_model.get_molecule_species_by_name("s_pre")
        mol_s_post  = cb_model.get_molecule_species_by_name("s_post")


        cb_model.change_molecule_display ( mol_a,      glyph='Cube',        scale=3.0, red=0.96, green=1.0,  blue=0.3,  emit=2.0 )
        cb_model.change_molecule_display ( mol_nt,     glyph='Icosahedron', scale=3.0, red=1.0,  green=0.03, blue=0.47, emit=2.0 )
        cb_model.change_molecule_display ( mol_s_pre,  glyph='Cone',        scale=3.0, red=0.0,  green=0.8,  blue=0.0,  emit=1.0 )
        cb_model.change_molecule_display ( mol_s_post, glyph='Cone',        scale=3.0, red=0.0,  green=0.26, blue=0.8,  emit=1.0 )


        cb_model.add_surface_class_to_model ( "pre_surf" )
        cb_model.add_surface_class_to_model ( "post_surf" )

        cb_model.assign_surface_class_to_region ( "pre_surf", "neuron_pre", "synapse_pre" )
        cb_model.assign_surface_class_to_region ( "post_surf", "neuron_post", "synapse_post" )


        cb_model.add_reaction_to_model ( rin="a; @ pre_surf,",    rtype="irreversible", rout="s_pre,",   fwd_rate="1e19", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="s_pre,",            rtype="irreversible", rout="nt,",      fwd_rate="1e4",  bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="nt; @ post_surf'",  rtype="irreversible", rout="s_post,",  fwd_rate="1e19", bkwd_rate="" )
        cb_model.add_reaction_to_model ( rin="s_post'",           rtype="irreversible", rout="a'",       fwd_rate="1e4",  bkwd_rate="" )


        cb_model.add_molecule_release_site_to_model ( mol="a", shape="OBJECT", obj_expr="neuron_pre", q_expr="1000" )

        cb_model.set_visualization ( enable_visualization=True, export_all=True, all_iterations=False, start=0, end=100000, step=1 )

        cb_model.run_model ( iterations='1000', time_step='1e-6', wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "e86e25e48d7d85fee416ee384d05cbc4773c9c56", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        scn.frame_current = 1

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 0.25 )
        cb_model.switch_to_orthographic()
        cb_model.set_axis_angle ( [0.0, -1.0, 0.0], math.pi/2 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }





###########################################################################################################
group_name = "Stress Tests"
test_name = "Stress Model Objects"
operator_name = "cellblender_test.stress_model_objects_test"
next_test_group_num = register_test ( test_groups, group_name, test_name, operator_name, next_test_group_num )

class StressModelObjectsTestOp(bpy.types.Operator):
    bl_idname = operator_name
    bl_label = test_name
    self_test_name = test_name

    def invoke(self, context, event):
        self.execute ( context )
        return {'FINISHED'}

    def execute(self, context):

        global active_frame_change_handler
        active_frame_change_handler = None

        app = bpy.context.scene.cellblender_test_suite

        cb_model = CellBlender_Model ( context, self.self_test_name )

        scn = cb_model.get_scene()
        mcell = cb_model.get_mcell()



        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0

        dx = 1
        dy = 0

        x = 0
        y = 0

        for i in range(app.stress_test_level):

            cb_model.add_cube_to_model ( name="box_%d"%(i), draw_type="WIRE", x=x, y=y, z=0, size=0.45 )

            print ( "x = %f, y = %f" % (x, y) )
            x += dx
            y += dy
            if (x > max_x):
                dx = 0
                dy = 1
                max_x = x
            elif (y > max_y):
                dx = -1
                dy = 0
                max_y = y
            elif (x < min_x):
                dx = 0
                dy = -1
                min_x = x
            elif (y < min_y):
                dx = 1
                dy = 0
                min_y = y


        mol_a =  cb_model.add_molecule_species_to_model ( name="a",  diff_const_expr="1e-4" )

        ### N O T E:  The previous assignments may NOT be valid if items were added to the molecule list.
        ###  For that reason, the same assignments must be made again by name or Blender may CRASH!!

        mol_a   = cb_model.get_molecule_species_by_name('a')

        cb_model.add_molecule_release_site_to_model ( mol="a", q_expr="1000", shape="SPHERICAL", d="0.1", x="0", y="0", z="-1" )

        cb_model.run_model ( iterations='1500', time_step='1e-5', wait_time=10.0 )

        cb_model.compare_mdl_with_sha1 ( "03bee61bca5ebf9ce05b0f75a5a42b593fdc4a75", test_name=self.self_test_name )

        cb_model.refresh_molecules()

        cb_model.select_none()


        mol_scale = 5.0

        cb_model.change_molecule_display ( mol_a,  glyph='Cube',  scale=mol_scale, red=1.0, green=0.0, blue=0.0 )

        cb_model.set_view_back()

        cb_model.scale_view_distance ( 1.0 )

        cb_model.hide_manipulator ( hide=True )

        cb_model.play_animation()

        return { 'FINISHED' }



#############################################################
################## End of Individual Tests ##################
#############################################################



def add_handler ( handler_list, handler_function ):
    """ Only add a handler if it's not already in the list """
    if not (handler_function in handler_list):
        handler_list.append ( handler_function )
        
        #cellblender_added_handlers


def remove_handler ( handler_list, handler_function ):
    """ Only remove a handler if it's in the list """
    if handler_function in handler_list:
        handler_list.remove ( handler_function )


# Load scene callback
@persistent
def scene_loaded(dummy):
    bpy.context.scene.cellblender_test_suite.make_real()

# Frame change callback
@persistent
def test_suite_frame_change_handler(scene):
  global active_frame_change_handler
  if active_frame_change_handler != None:
      active_frame_change_handler ( scene )


def register():
    print ("Registering ", __name__)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.cellblender_test_suite = bpy.props.PointerProperty(type=CellBlenderTestPropertyGroup)
    # Add the scene update pre handler
    add_handler ( bpy.app.handlers.scene_update_pre, scene_loaded )
    add_handler ( bpy.app.handlers.frame_change_pre, test_suite_frame_change_handler )


def unregister():
    print ("Unregistering ", __name__)
    remove_handler ( bpy.app.handlers.frame_change_pre, test_suite_frame_change_handler )
    remove_handler ( bpy.app.handlers.scene_update_pre, scene_loaded )
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.cellblender_test_suite

if __name__ == "__main__":
    register()


# test call
#bpy.ops.modtst.dialog_operator('INVOKE_DEFAULT')


