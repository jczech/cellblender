# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import os
import atexit

bl_info = {
    "name": "CellBlender",
    "author": "Tom Bartol, Dipak Barua, Jacob Czech, Markus Dittrich, "
        "James Faeder, Bob Kuczewski, Devin Sullivan, Jose Juan Tapia",
    "version": (1, 2, 0),
    "blender": (2, 72, 0),
    "api": 55057,
    "location": "View3D -> ToolShelf -> CellBlender",
    "description": "CellBlender Modeling System for MCell",
    "warning": "",
    "wiki_url": "http://www.mcell.org",
    "tracker_url": "https://github.com/mcellteam/cellblender/issues",
    "category": "Cell Modeling"
}

from cellblender import cellblender_source_info
# cellblender_info was moved from __init__.py to cellblender_source_info.py
# This assignment fixes any broken references ... for now:
cellblender_info = cellblender_source_info.cellblender_info


simulation_popen_list = []

current_data_model = None

# To support reload properly, try to access a package var.
# If it's there, reload everything
if "bpy" in locals():
    print("Reloading CellBlender")
    import imp
    imp.reload(data_model)

    imp.reload(cellblender_main)

    imp.reload(parameter_system)
    imp.reload(cellblender_preferences)
    imp.reload(cellblender_project)
    imp.reload(cellblender_initialization)

    imp.reload(cellblender_scripting)
    imp.reload(cellblender_objects)
    imp.reload(cellblender_molecules)
    imp.reload(cellblender_molmaker)
    imp.reload(cellblender_reactions)
    imp.reload(cellblender_release)
    imp.reload(cellblender_surface_classes)
    imp.reload(cellblender_surface_regions)
    imp.reload(cellblender_reaction_output)
    imp.reload(cellblender_partitions)
    imp.reload(cellblender_simulation)
    imp.reload(cellblender_mol_viz)
    imp.reload(cellblender_meshalyzer)
    imp.reload(cellblender_legacy)
    imp.reload(object_surface_regions)
    imp.reload(run_simulations)
    imp.reload(io_mesh_mcell_mdl)
    imp.reload(sim_runner_queue)
    imp.reload(mdl)         # BK: Added for MDL
    imp.reload(bng)         # DB: Adde for BNG
    #    imp.reload(sbml)        #JJT: Added for SBML

    # Use "try" for optional modules
    try:
        imp.reload(data_plotters)
    except:
        print("cellblender.data_plotters was not reloaded")
else:
    print("Importing CellBlender")
    from . import data_model

    from . import cellblender_main

    from . import parameter_system
    from . import cellblender_preferences
    from . import cellblender_project
    from . import cellblender_initialization

    from . import cellblender_scripting
    from . import cellblender_objects
    from . import cellblender_molecules
    from . import cellblender_molmaker
    from . import cellblender_reactions
    from . import cellblender_release
    from . import cellblender_surface_classes
    from . import cellblender_surface_regions
    from . import cellblender_reaction_output
    from . import cellblender_partitions
    from . import cellblender_simulation
    from . import cellblender_mol_viz
    from . import cellblender_meshalyzer
    from . import cellblender_legacy
    from . import object_surface_regions
    from . import run_simulations
    from . import io_mesh_mcell_mdl
    from . import sim_runner_queue
    from . import mdl  # BK: Added for MDL
    from . import bng  # DB: Added for BNG
    #    from . import sbml #JJT: Added for SBML

    # Use "try" for optional modules
    try:
        from . import data_plotters
    except:
        print("cellblender.data_plotters was not imported")


###############################################################
### These functions support data model scripting

def get_data_model ( geometry=False ):
    import bpy
    import cellblender
    context = bpy.context
    mdm = context.scene.mcell.build_data_model_from_properties ( context, geometry=geometry )
    dm = { 'mcell' : mdm }
    return dm

def replace_data_model ( dm, geometry=False, scripts=False ):
    import bpy
    import cellblender
    context = bpy.context
    dm['mcell'] = context.scene.mcell.upgrade_data_model ( dm['mcell'] )
    context.scene.mcell.build_properties_from_data_model ( context, dm['mcell'], geometry=geometry, scripts=scripts )

def cd_to_project():
    import os
    original_cwd = os.getcwd()
    os.makedirs ( cellblender_utils.project_files_path(), exist_ok=True )
    os.chdir ( cellblender_utils.project_files_path() )
    return original_cwd

def cd_to_location ( location ):
    import os
    original_cwd = os.getcwd()
    os.chdir ( location )
    return original_cwd

###############################################################



# XXX: bpy.context.mcell isn't available here, so we can't use get_python_path
# as intended. It will always use Blender's python or the system version of
# python. Maybe this is good enough, but we might want to revisit this and
# clean it up.
python_path = cellblender_utils.get_python_path()
simulation_queue = sim_runner_queue.SimQueue(python_path)

import bpy
import sys


# Can't do this here because it gives: AttributeError: '_RestrictData' object has no attribute 'scenes'
#for scn in bpy.data.scenes:
#  print ( "Attempting to disable ID scripting for Scene " + str(scn) )
#  if 'mcell' in scn:
#    if 'run_simulation' in scn['mcell']:
#      if 'enable_python_scripting' in scn['mcell']['run_simulation']:
#        scn['mcell']['run_simulation']['enable_python_scripting'] = 0



#cellblender_added_handlers = []

def add_handler ( handler_list, handler_function ):
    """ Only add a handler if it's not already in the list """
    if not (handler_function in handler_list):
        handler_list.append ( handler_function )
        
        #cellblender_added_handlers


def remove_handler ( handler_list, handler_function ):
    """ Only remove a handler if it's in the list """
    if handler_function in handler_list:
        handler_list.remove ( handler_function )




# We use per module class registration/unregistration
def register():
    print ( "Registering CellBlender with Blender version = " + str(bpy.app.version) )
    bpy.utils.register_module(__name__, verbose=False)

    # Unregister and re-register panels to display them in order
    bpy.utils.unregister_class(cellblender_preferences.MCELL_PT_cellblender_preferences)
    bpy.utils.unregister_class(cellblender_project.MCELL_PT_project_settings)
    bpy.utils.unregister_class(cellblender_simulation.MCELL_PT_run_simulation)         # Need to unregister because it's registered automatically
    bpy.utils.unregister_class(cellblender_simulation.MCELL_PT_run_simulation_queue)
    bpy.utils.unregister_class(cellblender_mol_viz.MCELL_PT_viz_results)
    bpy.utils.unregister_class(cellblender_objects.MCELL_PT_model_objects)
    bpy.utils.unregister_class(cellblender_partitions.MCELL_PT_partitions)
    bpy.utils.unregister_class(cellblender_initialization.MCELL_PT_initialization)
    # bpy.utils.unregister_class(parameter_system.MCELL_PT_parameter_system)
    bpy.utils.unregister_class(cellblender_molecules.MCELL_PT_define_molecules)
    bpy.utils.unregister_class(cellblender_reactions.MCELL_PT_define_reactions)
    bpy.utils.unregister_class(cellblender_surface_classes.MCELL_PT_define_surface_classes)
    bpy.utils.unregister_class(cellblender_surface_regions.MCELL_PT_mod_surface_regions)
    bpy.utils.unregister_class(cellblender_release.MCELL_PT_release_pattern)
    bpy.utils.unregister_class(cellblender_release.MCELL_PT_molecule_release)
    bpy.utils.unregister_class(cellblender_reaction_output.MCELL_PT_reaction_output_settings)
    bpy.utils.unregister_class(cellblender_mol_viz.MCELL_PT_visualization_output_settings)


    # Don't normally re-register individual panels here with new panel system, but do it for now to test slowdown problem
    # TMB: Don't re-register here to disable all individual panels in old panel system

#    bpy.utils.register_class(cellblender_preferences.MCELL_PT_cellblender_preferences)
#    bpy.utils.register_class(cellblender_project.MCELL_PT_project_settings)
#    bpy.utils.register_class(cellblender_simulation.MCELL_PT_run_simulation)
#    bpy.utils.register_class(cellblender_simulation.MCELL_PT_run_simulation_queue)
#    bpy.utils.register_class(cellblender_mol_viz.MCELL_PT_viz_results)
#    bpy.utils.register_class(parameter_system.MCELL_PT_parameter_system)
#    bpy.utils.register_class(cellblender_partitions.MCELL_PT_partitions)
#    bpy.utils.register_class(cellblender_initialization.MCELL_PT_initialization)
#    bpy.utils.register_class(cellblender_molecules.MCELL_PT_define_molecules)
#    bpy.utils.register_class(cellblender_reactions.MCELL_PT_define_reactions)
#    bpy.utils.register_class(cellblender_surface_classes.MCELL_PT_define_surface_classes)
#    bpy.utils.register_class(cellblender_surface_regions.MCELL_PT_mod_surface_regions)
#    bpy.utils.register_class(cellblender_release.MCELL_PT_release_pattern)
#    bpy.utils.register_class(cellblender_release.MCELL_PT_molecule_release)
#    bpy.utils.register_class(cellblender_reaction_output.MCELL_PT_reaction_output_settings)
#    bpy.utils.register_class(cellblender_mol_viz.MCELL_PT_visualization_output_settings)

    # Remove all menu items first to avoid duplicates
    bpy.types.INFO_MT_file_import.remove(io_mesh_mcell_mdl.menu_func_import)
    bpy.types.INFO_MT_file_export.remove(io_mesh_mcell_mdl.menu_func_export)
    bpy.types.INFO_MT_file_import.remove(mdl.menu_func_import)
    bpy.types.INFO_MT_file_import.remove(bng.menu_func_bng_import)
    bpy.types.INFO_MT_file_import.remove(bng.menu_func_cbng_import)
    bpy.types.INFO_MT_file_import.remove(data_model.menu_func_import)
    bpy.types.INFO_MT_file_export.remove(data_model.menu_func_export)
    bpy.types.INFO_MT_file_import.remove(data_model.menu_func_import_all)
    bpy.types.INFO_MT_file_export.remove(data_model.menu_func_export_all)
    bpy.types.INFO_MT_file_import.remove(data_model.menu_func_import_all_json)
    bpy.types.INFO_MT_file_export.remove(data_model.menu_func_export_all_json)
    bpy.types.INFO_MT_file_export.remove(data_model.menu_func_print)


    # Now reinstall all menu items
    bpy.types.INFO_MT_file_import.append(io_mesh_mcell_mdl.menu_func_import)
    bpy.types.INFO_MT_file_export.append(io_mesh_mcell_mdl.menu_func_export)


    # BK: Added for MDL import
    bpy.types.INFO_MT_file_import.append(mdl.menu_func_import)

    # DB: Added for BioNetGen import
    bpy.types.INFO_MT_file_import.append(bng.menu_func_bng_import)
    bpy.types.INFO_MT_file_import.append(bng.menu_func_cbng_import)

    #JJT: And SBML import
    #bpy.types.INFO_MT_file_import.append(sbml.menu_func_import)

    # BK: Added for Data Model import and export
    bpy.types.INFO_MT_file_import.append(data_model.menu_func_import)
    bpy.types.INFO_MT_file_export.append(data_model.menu_func_export)
    bpy.types.INFO_MT_file_import.append(data_model.menu_func_import_all)
    bpy.types.INFO_MT_file_export.append(data_model.menu_func_export_all)
    bpy.types.INFO_MT_file_import.append(data_model.menu_func_import_all_json)
    bpy.types.INFO_MT_file_export.append(data_model.menu_func_export_all_json)
    bpy.types.INFO_MT_file_export.append(data_model.menu_func_print)



    bpy.types.Scene.mcell = bpy.props.PointerProperty(
        type=cellblender_main.MCellPropertyGroup)
    bpy.types.Object.mcell = bpy.props.PointerProperty(
        type=object_surface_regions.MCellObjectPropertyGroup)


    print("CellBlender registered")
    if (bpy.app.version not in cellblender_info['supported_version_list']):
        print("Warning, current Blender version", bpy.app.version,
              " is not in supported list:",
              cellblender_info['supported_version_list'])

    print("CellBlender Addon found: ", __file__)
    cellblender_info["cellblender_addon_path"] = os.path.dirname(__file__)
    print("CellBlender Addon Path is " + cellblender_info["cellblender_addon_path"])
    addon_path = os.path.dirname(__file__)

    # SELECT ONE OF THE FOLLOWING THREE:

    # To compute the ID on load, uncomment this choice and comment out the other two
    #cellblender_source_info.identify_source_version(addon_path,verbose=True)

    # To import the ID as python code, uncomment this choice and comment out the other two
    #from . import cellblender_id
    #cellblender_info['cellblender_source_sha1'] = cellblender_id.cellblender_id

    # To read the ID from the file as text, uncomment this choice and comment out the other two
    
    cs = open ( os.path.join(addon_path, 'cellblender_id.py') ).read()
    cellblender_info['cellblender_source_sha1'] = cs[1+cs.find("'"):cs.rfind("'")]


    print ( "CellBlender Source SHA1 = " + cellblender_info['cellblender_source_sha1'] )

    # Use "try" for optional modules
    try:
        # print ( "Reloading data_plottters" )
        cellblender_info['cellblender_plotting_modules'] = []
        plotters_list = data_plotters.find_plotting_options()
        # data_plotters.print_plotting_options()
        print("Begin installing the plotters")
        for plotter in plotters_list:
            #This assignment could be done all at once since plotters_list is
            # already a list.
            cellblender_info['cellblender_plotting_modules'] = \
                cellblender_info['cellblender_plotting_modules'] + [plotter]
            print("  System meets requirements for %s" % (plotter.get_name()))
    except:
        print("Error installing some plotting packages: " + str(sys.exc_info()))

    print ( "Adding handlers to bpy.app.handlers" )
    # Note that handlers appear to be called in the order listed here (first listed are called first)
    
    # Add the frame change pre handler
    add_handler ( bpy.app.handlers.frame_change_pre, cellblender_mol_viz.frame_change_handler )
    add_handler ( bpy.app.handlers.frame_change_pre, cellblender_objects.frame_change_handler )

    # Add the load_pre handlers
    add_handler ( bpy.app.handlers.load_pre, cellblender_main.report_load_pre )

    # Add the load_post handlers
    add_handler ( bpy.app.handlers.load_post, cellblender_simulation.disable_python )
    add_handler ( bpy.app.handlers.load_post, data_model.load_post )
    add_handler ( bpy.app.handlers.load_post, cellblender_simulation.clear_run_list )
    add_handler ( bpy.app.handlers.load_post, cellblender_objects.model_objects_update )
    add_handler ( bpy.app.handlers.load_post, object_surface_regions.object_regions_format_update )
    add_handler ( bpy.app.handlers.load_post, cellblender_main.mcell_valid_update )
    add_handler ( bpy.app.handlers.load_post, cellblender_preferences.load_preferences )
    add_handler ( bpy.app.handlers.load_post, cellblender_main.scene_loaded )
    add_handler ( bpy.app.handlers.load_post, cellblender_mol_viz.read_viz_data_load_post )

    # Add the scene update pre handler
    add_handler ( bpy.app.handlers.scene_update_pre, cellblender_main.scene_loaded )

    # Add the save_pre handlers
    add_handler ( bpy.app.handlers.save_pre, data_model.save_pre )
    add_handler ( bpy.app.handlers.save_pre, cellblender_objects.model_objects_update )

    # Add the save_post handlers
    add_handler ( bpy.app.handlers.save_post, cellblender_mol_viz.viz_data_save_post )

    # Register atexit function to shutdown simulation queue before quitting Blender
    atexit.register(simulation_queue.shutdown)

    # Molecule Labels
    bpy.types.WindowManager.display_mol_labels = bpy.props.PointerProperty(type=cellblender_molecules.MCELL_MolLabelProps)

    print("CellBlender Registered")



def unregister():

    # Molecule Labels
    cellblender_molecules.MCELL_OT_mol_show_text.handle_remove(bpy.context)
    del bpy.types.WindowManager.display_mol_labels

    remove_handler ( bpy.app.handlers.frame_change_pre, cellblender_objects.frame_change_handler )
    remove_handler ( bpy.app.handlers.frame_change_pre, cellblender_mol_viz.frame_change_handler )
    remove_handler ( bpy.app.handlers.load_pre,         cellblender_main.report_load_pre )
    remove_handler ( bpy.app.handlers.load_post, data_model.load_post )
    remove_handler ( bpy.app.handlers.load_post, cellblender_simulation.clear_run_list )
    remove_handler ( bpy.app.handlers.load_post, cellblender_objects.model_objects_update )
    remove_handler ( bpy.app.handlers.load_post, object_surface_regions.object_regions_format_update )
    remove_handler ( bpy.app.handlers.load_post, cellblender_main.mcell_valid_update )
    remove_handler ( bpy.app.handlers.load_post, cellblender_preferences.load_preferences )
    remove_handler ( bpy.app.handlers.load_post, cellblender_main.scene_loaded )
    remove_handler ( bpy.app.handlers.load_post, cellblender_mol_viz.read_viz_data_load_post )
    remove_handler ( bpy.app.handlers.save_post, cellblender_mol_viz.viz_data_save_post )
    remove_handler ( bpy.app.handlers.scene_update_pre, cellblender_main.scene_loaded )
    remove_handler ( bpy.app.handlers.save_pre, data_model.save_pre )
    remove_handler ( bpy.app.handlers.save_pre, cellblender_objects.model_objects_update )
    remove_handler ( bpy.app.handlers.load_post, cellblender_simulation.disable_python )

    atexit.unregister(simulation_queue.shutdown)

    bpy.utils.unregister_module(__name__)

    print("CellBlender unregistered")


# for testing
if __name__ == '__main__':
    register()
