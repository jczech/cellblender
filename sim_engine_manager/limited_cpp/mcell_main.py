# file: mcell_main.py

import sys
import os
import pickle
import math
import random
import array
import shutil
from libMCell import *
print ( "\n\nMCell Python Prototype using libMCell %d arguments:\n" % len(sys.argv) )
print ( "Running from " + os.getcwd() )
proj_path = ""
data_model_file_name = ""
data_model_full_path = ""
for arg in sys.argv:
  print ( "   " + str(arg) )
  if arg[0:10] == "proj_path=":
    proj_path = arg[10:]
  if arg[0:11] == "data_model=":
    data_model_file_name = arg[11:]
print ( "\n\n" )


if len(data_model_file_name) > 0:
  data_model_full_path = os.path.join ( proj_path, data_model_file_name )

print ( "Project path = \"%s\", data_model_file_name = \"%s\"" % (proj_path, data_model_full_path) )

##### Read in the data model itself

dm = None
if len(data_model_full_path) > 0:
  print ( "Loading data model from file: " + data_model_full_path + " ..." )
  f = open ( data_model_full_path, 'r' )
  pickle_string = f.read()
  f.close()
  dm = pickle.loads ( pickle_string.encode('latin1') )

print ( "Done loading CellBlender model." )

if dm is None:
  print ( "ERROR: Unable to use data model" )
  sys.exit(1)

#print ( str(dm) )


##### Use the Data Model to initialize a libMCell model

mcell_sim = MCellSimulation()

mcell_sim.num_iterations = eval(dm['mcell']['initialization']['iterations'])
mcell_sim.time_step = eval(dm['mcell']['initialization']['time_step'])

mol_defs = dm['mcell']['define_molecules']['molecule_list']
mols = {}

for m in mol_defs:
  print ( "Molecule " + m['mol_name'] + " is a " + m['mol_type'] + " molecule diffusing with " + str(m['diffusion_constant']) )
  mol = MCellMoleculeSpecies()
  mol.name = str(m['mol_name']) # This str() appears to be needed because of "uName" kinds of problems (Unicode?)
  mol.diffusion_constant = eval(m['diffusion_constant'])
  mcell_sim.add_molecule_species(mol)
  mols[mol.name] = mol

rel_defs = dm['mcell']['release_sites']['release_site_list']
rels = {}

for r in rel_defs:
  print ( "Release " + str(r['quantity']) + " of " + r['molecule'] + " at (" + str(r['location_x']) + "," + str(r['location_y']) + "," + str(r['location_z']) + ")"  )
  rel = MCellReleaseSite()
  rel.x = eval(r['location_x'])
  rel.y = eval(r['location_y'])
  rel.z = eval(r['location_z'])
  rel.quantity = eval(r['quantity'])
  rel.molecule_species = mols[r['molecule']]
  mcell_sim.add_molecule_release_site(rel)

# This is a temporary way of defining fake reactions if there are any reactions requested
num_defined_reactions = 0
if 'define_reactions' in dm['mcell']:
  if 'reaction_list' in dm['mcell']['define_reactions']:
    num_defined_reactions = len(dm['mcell']['define_reactions']['reaction_list'])

# This is a temporary way of defining fake reactions if there are any reactions requested
if num_defined_reactions > 0:
  mcell_sim.has_reactions = True

mcell_sim.dump_state()

#__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

print ( "\nStarting Python simulation using libMCell ...\n" )

mcell_sim.run_simulation(proj_path)

print ( "\nPython simulation using libMCell is complete.\n" )

