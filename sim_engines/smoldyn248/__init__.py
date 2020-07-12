import subprocess
import sys
import os
import pickle
import math
import random
import array
import shutil

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

print ( "Executing Smoldyn Simulation" )

print ( "Note that CellBlender partitions are used to define Smoldyn Boundaries" )

# Name of this engine to display in the list of choices (Both should be unique within a CellBlender installation)
plug_code = "SMOLDYN248"
plug_name = "Prototype Smoldyn 2.48 Simulation"

smoldyn_files_dir = ""
project_files_dir = ""
start_seed = 1
end_seed = 1

def print_info():
  global parameter_dictionary
  print ( 50*'==' )
  for k in sorted(parameter_dictionary.keys()):
    print ( "" + k + " = " + str(parameter_dictionary[k]) )
  print ( 50*'==' )

def reset():
  global parameter_dictionary
  print ( "Reset was called" )
  parameter_dictionary['Output Detail (0-100)']['val'] = 20


def postprocess():
  global parameter_dictionary
  global smoldyn_files_dir
  global project_files_dir
  global start_seed
  global end_seed
  print ( "Postprocess was called with Smoldyn files at " + str(smoldyn_files_dir) )
  print ( "Postprocess was called for CellBlender files " + str(project_files_dir) )


  react_dir = os.path.join(project_files_dir, "output_data", "react_data")

  if os.path.exists(react_dir):
      shutil.rmtree(react_dir,ignore_errors=True)
  if not os.path.exists(react_dir):
      os.makedirs(react_dir)

  viz_dir = os.path.join(project_files_dir, "output_data", "viz_data")

  if os.path.exists(viz_dir):
      shutil.rmtree(viz_dir,ignore_errors=True)
  if not os.path.exists(viz_dir):
      os.makedirs(viz_dir)



  for run_seed in range(start_seed, end_seed+1):
    print ( "  Postprocessing for seed " + str(run_seed) )
    f1 = open ( os.path.join ( smoldyn_files_dir, 'run%d'%run_seed, 'viz_data.txt' ) )
    f2 = open ( os.path.join ( smoldyn_files_dir, 'run%d'%run_seed, 'viz_data2.txt' ) )
    f1d = f1.read()
    f2d = f2.read()
    f1s = [ l for l in f1d.split('\n') if len(l) > 0 ]
    f2s = [ l for l in f2d.split('\n') if len(l) > 0 ]

    # Convert each string to a list that includes the molecule name at the end
    n = min(len(f1s),len(f2s))
    full_list = []
    for i in range(n):
      l = f2s[i].strip().split()
      l.append ( f1s[i][0:f1s[i].index('(')] )
      full_list.append ( l )

    first_iteration = int(full_list[0][0])
    last_iteration = int(full_list[-1][0])
    iter_list = sorted(set([ int(l[0]) for l in full_list]))

    frame_dict = {}
    for k in iter_list:
      frame_dict[k] = {}

    for l in full_list:
      i = int(l[0])
      mol = l[-1]
      if not mol in frame_dict[i]:
        frame_dict[i][mol] = []
      frame_dict[i][mol].append ( [ l[3], l[4], l[5] ] )

    # The frame_dict is now organized to use for writing molecule files

    ndigits = 1 + math.log(last_iteration+1,10)
    file_name_template = "Scene.cellbin.%%0%dd.dat" % ndigits

    seed_dir = "seed_%05d" % run_seed

    viz_seed_dir = os.path.join(viz_dir, seed_dir)

    if os.path.exists(viz_seed_dir):
        shutil.rmtree(viz_seed_dir,ignore_errors=True)
    if not os.path.exists(viz_seed_dir):
        os.makedirs(viz_seed_dir)

    react_seed_dir = os.path.join(react_dir, seed_dir)

    if os.path.exists(react_seed_dir):
        shutil.rmtree(react_seed_dir,ignore_errors=True)
    if not os.path.exists(react_seed_dir):
        os.makedirs(react_seed_dir)


    for i in iter_list:
      frame = frame_dict[i]

      # Write the viz data (every iteration for now)
      viz_file_name = file_name_template % i
      viz_file_name = os.path.join(viz_seed_dir,viz_file_name)
      #if (i % print_every) == 0:
      #  if output_detail > 0: print ( "File = " + viz_file_name )
      f = open(viz_file_name,"wb")
      int_array = array.array("I")   # Marker indicating a binary file
      int_array.fromlist([1])
      int_array.tofile(f)
      for mol_name in frame.keys():
        f.write(bytearray([len(mol_name)]))        # Number of bytes in the name
        for ni in range(len(mol_name)):
          f.write(bytearray([ord(mol_name[ni])]))  # Each byte of the name
        f.write(bytearray([0]))                    # Molecule Type, 1=Surface, 0=Volume?

        # Write out the total number of values for this molecule species
        int_array = array.array("I")
        #int_array.fromlist([3*len(m['instances'])])
        int_array.fromlist([3*len(frame[mol_name])])
        int_array.tofile(f)

        for mi in frame[mol_name]:
          x = float(mi[0])
          y = float(mi[1])
          z = float(mi[2])
          mol_pos = array.array("f")
          mol_pos.fromlist ( [ x, y, z ] )
          mol_pos.tofile(f)
      f.close()

    #__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
  print ( "Done postrocessing all Smoldyn runs" )


def use_cube():
  global parameter_dictionary
  size = float(parameter_dictionary['bounding_cube_size']['val']) / 2
  parameter_dictionary['x_bound_min']['val'] = -size
  parameter_dictionary['x_bound_max']['val'] =  size
  parameter_dictionary['y_bound_min']['val'] = -size
  parameter_dictionary['y_bound_max']['val'] =  size
  parameter_dictionary['z_bound_min']['val'] = -size
  parameter_dictionary['z_bound_max']['val'] =  size



# List of parameters as dictionaries - each with keys for 'name', 'desc', 'def', and optional 'as':
parameter_dictionary = {
  'Smoldyn Path': {'val': "//../../../../../smoldyn/smoldyn-2.51/cmake/smoldyn", 'as':'filename', 'desc':"Optional Path", 'icon':'SCRIPTWIN'},
  'Auto Boundaries': {'val': True, 'desc':"Compute boundaries from all geometric points"},
  'Set Cube Boundaries:': {'val': use_cube, 'desc':"Set Boundaries as cube"},
  'bounding_cube_size': {'val': 2, 'desc':"Cube Boundary Size"},
  'x_bound_min': {'val': -1.0, 'desc':"x boundary (minimum)"},
  'x_bound_max': {'val':  1.0, 'desc':"x boundary (maximum)"},
  'y_bound_min': {'val': -1.0, 'desc':"y boundary (minimum)"},
  'y_bound_max': {'val':  1.0, 'desc':"y boundary (maximum)"},
  'z_bound_min': {'val': -1.0, 'desc':"z boundary (minimum)"},
  'z_bound_max': {'val':  1.0, 'desc':"z boundary (maximum)"},
  'Graphics': {'val':  False, 'desc':"Show Smoldyn Graphics"},
  'Command Line': {'val': "", 'desc':"Additional Command Line Parameters"},
  'Output Detail (0-100)': {'val': 20, 'desc':"Amount of Information to Print (0-100)", 'icon':'INFO'},
  'Postprocess': {'val': postprocess, 'desc':"Postprocess the data for CellBlender"},
  'Reset': {'val': reset, 'desc':"Reset everything"}
}

parameter_layout = [
  ['Smoldyn Path'],
  ['Auto Boundaries', 'Set Cube Boundaries:', 'bounding_cube_size'],
  ['x_bound_min', 'y_bound_min', 'z_bound_min'],
  ['x_bound_max', 'y_bound_max', 'z_bound_max'],
  ['Graphics', 'Command Line'],
  ['Output Detail (0-100)'],
  ['Postprocess', 'Reset']
]

par_val_dict = {}

def convert_to_value ( expression ):
  global par_val_dict
  return eval(expression,globals(),par_val_dict)


def prepare_runs_data_model_full ( data_model, project_dir, data_layout=None ):
  # Return a list of run command dictionaries.
  # Each run command dictionary must contain a "cmd" key and a "wd" key.
  # The cmd key will refer to a command list suitable for popen.
  # The wd key will refer to a working directory string.
  # Each run command dictionary may contain any other keys helpful for post-processing.
  # The run command dictionary list will be passed on to the postprocess_runs function.

  # The data_layout should be a dictionary something like this:

  #  {
  #   "version": 2,
  #   "data_layout": [
  #    ["/DIR", ["output_data"]],
  #    ["dc_a", [1e-06, 1e-05]],
  #    ["nrel", [100.0, 200.0, 300.0]],
  #    ["/FILE_TYPE", ["react_data", "viz_data"]],
  #    ["/SEED", [100, 101]]
  #   ]
  #  }

  # That dictionary describes the directory structure that CellBlender expects to find on the disk

  command_list = []

  global smoldyn_files_dir
  global project_files_dir
  global start_seed
  global end_seed
  global par_val_dict

  project_files_dir = "" + project_dir



  ## Build a parameter/value dictionary

  for p in data_model['parameter_system']['model_parameters']:
    par_val_dict[p['par_name']] = p['_extras']['par_value']


  init = data_model['initialization']

  dm_mol_list = data_model['define_molecules']['molecule_list']
  for m in dm_mol_list:
    print ( "Mol: " + str(m) )

  dm_rxn_list = data_model['define_reactions']['reaction_list']
  for r in dm_rxn_list:
    print ( "Rxn: " + str(r) )

  dm_rel_list = data_model['release_sites']['release_site_list']
  for r in dm_rel_list:
    print ( "Rel: " + str(r) )

  print ( "Geometrical Objects:" )
  geo_obj_list = data_model['geometrical_objects']['object_list']
  for o in geo_obj_list:
    print ( "Obj: " + str(o['name']) )

  output_detail = parameter_dictionary['Output Detail (0-100)']['val']

  graphics_flag = parameter_dictionary['Graphics']['val']

  command_line_options = parameter_dictionary['Command Line']['val']

  if output_detail > 0: print ( "Inside smoldyn248 run_simulation, project_dir=" + project_dir )
  smoldyn_files_dir = os.path.join ( os.path.dirname(project_dir), "smoldyn" )
  if output_detail > 0: print ( "Inside smoldyn248 run_simulation, smoldyn_files_dir=" + smoldyn_files_dir )

  script_dir_path = os.path.dirname(os.path.realpath(__file__))
  
  smoldyn_path = str(parameter_dictionary['Smoldyn Path']['val'])
  if smoldyn_path.startswith('//'):
    # This path is relative to the .blend file, so make it absolute:
    blend_file_path = os.path.dirname(os.path.dirname(project_files_dir))
    smoldyn_path = os.path.abspath(os.path.join(blend_file_path, smoldyn_path[2:]))

  auto_bounds = parameter_dictionary['Auto Boundaries']['val']

  min_bounds = []
  max_bounds = []

  min_bounds.append ( float(parameter_dictionary['x_bound_min']['val']) )
  max_bounds.append ( float(parameter_dictionary['x_bound_max']['val']) )
  min_bounds.append ( float(parameter_dictionary['y_bound_min']['val']) )
  max_bounds.append ( float(parameter_dictionary['y_bound_max']['val']) )
  min_bounds.append ( float(parameter_dictionary['z_bound_min']['val']) )
  max_bounds.append ( float(parameter_dictionary['z_bound_max']['val']) )

  # Calculate the bounds and attach to each object (needed to get an inside "point" for Smoldyn)

  print ( "Calculating the bounds of the objects (might want to include releases as well?)" )
  #__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
  for o in geo_obj_list:
      # Calculate the bounds for this object
      vlist = o['vertex_list']
      loc = o['location']
      smoldyn_bounds = [ [0,0], [0,0], [0,0] ]  # Min and Max for each of three axes (assumes 3D!!)
      first_value = True
      for face in o['element_connections']:
          for vindex in face:
              p = vlist[vindex]
              i = 0
              for coord in p:
                  if first_value:
                      smoldyn_bounds[i][0] = coord + loc[i]
                      smoldyn_bounds[i][1] = smoldyn_bounds[i][0]
                      first_value = False
                  else:
                      if smoldyn_bounds[i][0] > coord + loc[i]:
                        smoldyn_bounds[i][0] = coord + loc[i]
                      if smoldyn_bounds[i][1] < coord + loc[i]:
                        smoldyn_bounds[i][1] = coord + loc[i]
                  i = ( i + 1 ) % len(loc)

      print ( "Object " + o['name'] + " has bounds " + str(smoldyn_bounds) )

      # Attach the bounds to the object

      o['smoldyn_bounds'] = smoldyn_bounds

  if auto_bounds:
      # Calculate the global bounds from the bounds stored in each object
      print ( "Calculating simulation bounds from objects" )
      first_object = True
      for o in geo_obj_list:
          smoldyn_bounds = o['smoldyn_bounds']
          print ( "  Current Simulation Bounds: %s<x<%s, %s<y<%s, %s<z<%s" % (min_bounds[0], max_bounds[0], min_bounds[1], max_bounds[1], min_bounds[2], max_bounds[2], ) )
          print ( "    Object " + o['name'] + " has bounds " + str(smoldyn_bounds) )

          i = 0
          for bound in smoldyn_bounds:
              if first_object:
                  min_bounds[i] = bound[0]
                  max_bounds[i] = bound[1]
              else:
                  if min_bounds[i] > bound[0]:
                    min_bounds[i] = bound[0]
                  if max_bounds[i] < bound[1]:
                    max_bounds[i] = bound[1]
              i = ( i + 1 ) % len(loc)
          first_object = False

  print ( "Simulation Bounds: %s<x<%s, %s<y<%s, %s<z<%s" % (min_bounds[0], max_bounds[0], min_bounds[1], max_bounds[1], min_bounds[2], max_bounds[2], ) )


  if not os.path.exists(smoldyn_path):
      print ( "\n\nUnable to run, file does not exist: " + str(parameter_dictionary['Smoldyn Path']['val']) + " (" + smoldyn_path + ")\n\n" )
  else:

      # Create a subprocess for each simulation
      start = 1
      end = 1
      try:
        start = int(convert_to_value(data_model['simulation_control']['start_seed']))
        end = int(convert_to_value(data_model['simulation_control']['end_seed']))
      except Exception as e:
        print ( "Unable to find the start and/or end seeds in the data model" )
        pass
      start_seed = start
      end_seed = end

      for sim_seed in range(start,end+1):
          if output_detail > 0: print ("Running with seed " + str(sim_seed) )
          
          run_path = os.path.join(smoldyn_files_dir,"run"+str(sim_seed))

          if os.path.exists(run_path):
              shutil.rmtree(run_path,ignore_errors=True)
          if not os.path.exists(run_path):
              os.makedirs(run_path)

          run_file = os.path.join(run_path,"commands.txt")

          if output_detail > 0: print ( "Saving model to Smoldyn file: " + run_file )

          f = open ( run_file, 'w' )
          f.write ( "# Smoldyn Simulation Exported from CellBlender\n" )

          f.write ( "\n" )

          if graphics_flag:
              f.write ( "graphics opengl\n" )
          else:
              f.write ( "graphics none\n" )

          f.write ( "dim 3\n" )
          f.write ( "random_seed " + str(sim_seed) + "\n" )

          f.write ( "\n" )

          # Smoldyn gives an error: "simulation dimensions or boundaries are undefined" followed by "Simulation skipped" without boundaries:
          f.write ( "boundaries x " + str(min_bounds[0]) + " " + str(max_bounds[0]) + " r\n" )
          f.write ( "boundaries y " + str(min_bounds[1]) + " " + str(max_bounds[1]) + " r\n" )
          f.write ( "boundaries z " + str(min_bounds[2]) + " " + str(max_bounds[2]) + " r\n" )

          f.write ( "\n" )

          f.write ( "species" )
          for m in dm_mol_list:
            f.write ( " " + str(m['mol_name']) )
          f.write ( "\n" )

          f.write ( "\n" )

          for m in dm_mol_list:
            mcell_diffusion_constant = convert_to_value(m['diffusion_constant'])
            smoldyn_diffusion_constant = mcell_diffusion_constant * 10000  # Convert due to units difference
            f.write ( "difc " + str(m['mol_name']) + " " + str(smoldyn_diffusion_constant) + "\n" )

          f.write ( "\n" )

          for m in dm_mol_list:
            color = m['display']['color']
            f.write ( "color " + str(m['mol_name']) + " " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + "\n" )

          f.write ( "\n" )
          rnum = 1
          for r in dm_rxn_list:
              # TODO Rates may need scaling
              if r['products'] == 'NULL':
                  f.write ( "reaction R" + str(rnum) + " " + str(r['reactants']) + " -> " +         "0"        + " " + str(convert_to_value(r['fwd_rate'])) + "\n" )
              else:
                  f.write ( "reaction R" + str(rnum) + " " + str(r['reactants']) + " -> " + str(r['products']) + " " + str(convert_to_value(r['fwd_rate'])) + "\n" )
              rnum += 1

          f.write ( "\n" )

          smoldyn_time_step = 0.01  # TODO Needs to use CellBlender time step
          iterations = int(convert_to_value(init['iterations']))
          f.write ( "time_start 0\n" )
          f.write ( "time_step " + str(smoldyn_time_step) + "\n" )
          f.write ( "time_stop " + str(iterations * smoldyn_time_step) + "\n" )

          f.write ( "\n" )

          for o in geo_obj_list:
              f.write ( "start_surface " + str(o['name']) + "\n" )
              f.write ( "action both all reflect\n" )
              f.write ( "color both 0.5 0.5 0.5\n" )
              f.write ( "polygon both edge\n" )
              vlist = o['vertex_list']
              loc = o['location']
              for face in o['element_connections']:
                  f.write ( "panel tri" )
                  for vindex in face:
                      p = vlist[vindex]
                      i = 0
                      for coord in p:
                          f.write ( " " + str(coord + loc[i]) )
                          i = ( i + 1 ) % len(loc)
                  f.write ( "\n" )
              f.write ( "end_surface\n" )
              f.write ( "\n" )
              f.write ( "start_compartment " + str(o['name']) + "_comp\n" )
              f.write ( "surface " + str(o['name']) + "\n" )
              print ( "Calculate Center Point for " + o['name'] + " from " + str(o['smoldyn_bounds']) )
              center_point = [ (o['smoldyn_bounds'][0][0] + o['smoldyn_bounds'][0][1] ) / 2,
                               (o['smoldyn_bounds'][1][0] + o['smoldyn_bounds'][1][1] ) / 2,
                               (o['smoldyn_bounds'][2][0] + o['smoldyn_bounds'][2][1] ) / 2 ]
              f.write ( "point " + str(center_point[0]) + " " + str(center_point[1]) + " " + str(center_point[2]) + "\n" )
              f.write ( "end_compartment\n" )
              f.write ( "\n" )

          f.write ( "\n" )

          for r in dm_rel_list:
              if r['shape'] == 'OBJECT':
                  f.write ( "compartment_mol " + str(convert_to_value(r['quantity'])) + " " + str(r['molecule']) + " " + r['object_expr'] + "_comp" + "\n" )
              else:
                  f.write ( "mol " + str(convert_to_value(r['quantity'])) + " " + str(r['molecule']) + " " + str(convert_to_value(r['location_x'])) + " " + str(convert_to_value(r['location_y'])) + " " + str(convert_to_value(r['location_z'])) + "\n" )

          f.write ( "\n" )

          f.write ( "output_files viz_data.txt viz_data2.txt\n" )
          f.write ( "output_precision 6\n" )

          f.write ( "\n" )

          f.write ( "cmd E listmols  viz_data.txt\n" )
          f.write ( "cmd E listmols2 viz_data2.txt\n" )

          f.write ( "\n" )

          f.write ( "end_file\n" )
          f.close()

          if output_detail > 0: print ( "Done saving Smoldyn file." )

          command_dict = { 'cmd': smoldyn_path,
                           'args': [ run_file ],
                           'wd': project_dir
                         }
          if len(command_line_options) > 0:
            command_dict['args'].append(command_line_options)

          command_list.append ( command_dict )
          if output_detail > 0: print ( str(command_dict) )

  return ( command_list )


if __name__ == "__main__":
    print ( "Called with __name__ == __main__" )
    pass
