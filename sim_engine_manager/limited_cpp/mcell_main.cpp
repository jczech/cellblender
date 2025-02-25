#include <iostream>
#include <string>
#include <vector>
#include <sstream>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <math.h>
#include <time.h>

#include "libMCell.h"
#include "StorageClasses.h"
#include "rng.h"

extern "C" {
#include "JSON.h"
}

using namespace std;

typedef json_element data_model_element;

int print_detail = 0;

char *join_path ( char *p1, char sep, char *p2 ) {
  char *joined_path;
  if ((p1 == NULL) && (p2 == NULL) ) {
    joined_path = NULL;
  } else if ((p2 == NULL) || (strlen(p2) == 0) ) {
    joined_path = (char *) malloc ( strlen(p1) + 1 );
    strcpy ( joined_path, p1 );
  } else if ((p1 == NULL) || (strlen(p1) == 0) ) {
    joined_path = (char *) malloc ( strlen(p2) + 1 );
    strcpy ( joined_path, p2 );
  } else {
    joined_path = (char *) malloc ( strlen(p1) + 1 + strlen(p2) + 1 );
    strcpy ( joined_path, p1 );
    joined_path[strlen(p1)] = '/';
    strcpy ( &joined_path[strlen(p1)+1], p2 );
  }
  return ( joined_path );
}

// http://stackoverflow.com/questions/216823/whats-the-best-way-to-trim-stdstring
string trim(string& str) {
  str.erase(0, str.find_first_not_of(' '));       //prefixing spaces
  str.erase(str.find_last_not_of(' ')+1);         //surfixing spaces
  return str;
}

// http://ysonggit.github.io/coding/2014/12/16/split-a-string-using-c.html
vector<string> split(const string &s, char delim) {
    stringstream ss(s);
    string item;
    vector<string> tokens;
    while (getline(ss, item, delim)) {
        tokens.push_back(trim(item));
    }
    return tokens;
}

// These two functions look up names in the parameter dictionary when strings are found:

int get_int_from_par ( MapStore<double> par_dict, data_model_element *dm_element ) {
  int return_value = 0;
  if (dm_element->type == JSON_VAL_NUMBER) {
    if (print_detail >= 80) printf ( "get_int_from_par found a number\n" );
    return_value = json_get_int_value ( dm_element );
  } else if (dm_element->type == JSON_VAL_STRING) {
    if (print_detail >= 80) printf ( "get_int_from_par found a string\n" );
    char *s = json_get_string_value ( dm_element );
    // First try to see if it can be scanned as an integer:
    int num_scanned = sscanf ( s, " %d", &return_value );
    if (num_scanned > 0) {
      // The scan was good, so the value string was an integer
    } else {
      // The scan failed, so this should be a parameter name. Look it up:
      return_value = (int)(par_dict[s]);
    }
    free ( s );
  }
  if (print_detail >= 50) printf ( "get_int_from_par returning %d\n", return_value );
  return (return_value);
}

double get_float_from_par ( MapStore<double> par_dict, data_model_element *dm_element ) {
  double return_value = 0.0;
  if (dm_element->type == JSON_VAL_NUMBER) {
    if (print_detail >= 80) printf ( "get_float_from_par found a number\n" );
    return_value = json_get_float_value ( dm_element );
  } else if (dm_element->type == JSON_VAL_STRING) {
    if (print_detail >= 80) printf ( "get_float_from_par found a string\n" );
    char *s = json_get_string_value ( dm_element );
    // First try to see if it can be scanned as an double:
    int num_scanned = sscanf ( s, " %lg", &return_value );
    if (num_scanned > 0) {
      // The scan was good, so the value string was a float
    } else {
      // The scan failed, so this should be a parameter name. Look it up:
      return_value = (double)(par_dict[s]);
    }
    free ( s );
  }
  return (return_value);
}


int main ( int argc, char *argv[] ) {

  // Define data items to come from the command line arguments

  char *proj_path = NULL;
  char *data_model_file_name = NULL;
  char *data_model_full_path = "dm.json";
  unsigned int seed=1;
  
  int dump_data_model = 0;

  // Process the command line arguments

  for (int i=1; i<argc; i++) {
    if (print_detail > 10) printf ( "   Arg: %s\n", argv[i] );
    if (strcmp("test_rng",argv[i]) == 0) {
      int num_cases = 1000;
      double mean = 0.0;
      double variance = 0.0;
      double samp = 0.0;
      MCellRandomNumber_mrng *mcell_random = new MCellRandomNumber_mrng((uint32_t)(clock()));
      for (int i=0; i<num_cases; i++) {
        samp = mcell_random->rng_gauss();
        mean = mean + samp;
        variance = variance + (samp * samp);
      }
      mean = mean / num_cases;
      variance = variance / num_cases;
      printf ( "C++: mean=%g, var=%g\n", mean, variance );
      exit(0);
    }
    if (strncmp("proj_path=",argv[i],10) == 0) {
      proj_path = &argv[i][10];
    }
    if (strncmp("data_model=",argv[i],11) == 0) {
      data_model_file_name = &argv[i][11];
    }
    if (strncmp("print_detail=",argv[i],13) == 0) {
      sscanf ( &argv[i][13], "%d", &print_detail );
    }
    if (strncmp("seed=",argv[i],5) == 0) {
      sscanf ( &argv[i][5], "%d", &seed );
    }
    if (strcmp("dump",argv[i]) == 0) {
      dump_data_model = 1;
    }
  }
  if (print_detail > 10) printf ( "\n" );

  if (print_detail > 0) cout << "\n\n" << endl;
  if (print_detail > 0) cout << "******************************************" << endl;
  if (print_detail > 0) cout << "*   MCell C++ Prototype using libMCell   *" << endl;
  if (print_detail > 0) cout << "*      Updated: April 23rd, 2017         *" << endl;
  if (print_detail > 0) cout << "******************************************" << endl;
  if (print_detail > 0) cout << "\n" << endl;


  // Read the data model text from the input file

  data_model_full_path = join_path ( proj_path, '/', data_model_file_name );

  if (print_detail > 0) printf ( "Project path = \"%s\"\n", proj_path );
  if (print_detail > 0) printf ( "Data Model file = \"%s\"\n", data_model_full_path );
  if (print_detail > 0) printf ( "Seed = %d\n", seed );

  char *file_name = data_model_full_path;
  FILE *f = fopen ( file_name, "r" );

  if (print_detail > 10) printf ( "Loading data model from file: %s ...\n", file_name );

  long file_length;
  fseek (f, 0L, SEEK_END);
  file_length = ftell(f);

  char *file_text = (char *) malloc ( file_length + 2 );

  fseek (f, 0L, SEEK_SET);
  fread ( file_text, 1, file_length, f );

  fclose(f);
  
  if (print_detail > 10) printf ( "Done loading CellBlender model.\n" );

  file_text[file_length] = '\0'; // Be sure to null terminate!!


  // Parse the data model text into convenient structures

  if (print_detail > 10) printf ( "Parsing the JSON data model ...\n" );

  data_model_element *dm; // Data Model Tree
  dm = parse_json_text ( file_text );

  if (print_detail > 10) printf ( "Done parsing the JSON data model ...\n" );

  if (dump_data_model != 0) {
    dump_json_element_tree ( dm, 80, 0 ); printf ( "\n\n" );
  }


  // Extract various dictionaries and fields from the data model needed to run a minimal simulation:

  data_model_element *top_array = json_get_element_by_index ( dm, 0 );
  data_model_element *mcell = json_get_element_with_key ( top_array, "mcell" );

  // Blender version = ['mcell']['blender_version']
  data_model_element *blender_ver = json_get_element_with_key ( mcell, "blender_version" );
  data_model_element *vn = json_get_element_by_index ( blender_ver, 0 );
  if (print_detail > 10) printf ( "Blender API version = %ld", json_get_int_value ( vn ) );
  vn = json_get_element_by_index ( blender_ver, 1 );
  if (print_detail > 10) printf ( ".%ld", json_get_int_value ( vn ) );
  vn = json_get_element_by_index ( blender_ver, 2 );
  if (print_detail > 10) printf ( ".%ld\n", json_get_int_value ( vn ) );
  
  // API version = ['mcell']['api_version']
  data_model_element *api_ver = json_get_element_with_key ( mcell, "api_version" );

  if (print_detail > 10) printf ( "CellBlender API version = %d\n", json_get_int_value ( api_ver ) );


  // Start by collecting the parameters

  MapStore<double> par_dict;

  data_model_element *dm_parameter_system = json_get_element_with_key ( mcell, "parameter_system" );
  data_model_element *pars = json_get_element_with_key ( dm_parameter_system, "model_parameters" );

  if (print_detail > 10) printf ( "Finding parameters:\n" );
  int par_num = 0;
  data_model_element *this_par;
  while ((this_par=json_get_element_by_index(pars,par_num)) != NULL) {
    char *par_name;
    par_name = json_get_string_value ( json_get_element_with_key ( this_par, "par_name" ) );
    double par_val;
    data_model_element *extras = json_get_element_with_key ( this_par, "_extras" );
    par_val = json_get_float_value ( json_get_element_with_key ( extras, "par_value" ) );
    par_dict[par_name] = par_val;
    if (print_detail > 10) printf ( "  Parameter: %s = %f\n", par_name, par_dict[par_name] );
    par_num++;
  }

  // iterations = ['mcell']['initialization']['iterations']
  data_model_element *dm_init = json_get_element_with_key ( mcell, "initialization" );

  int iterations = get_int_from_par ( par_dict, json_get_element_with_key ( dm_init, "iterations" ) );
  //mcell_set_iterations ( iterations );

  double time_step = get_float_from_par ( par_dict, json_get_element_with_key ( dm_init, "time_step" ) );
  //mcell_set_time_step ( time_step );


  data_model_element *dm_define_molecules = json_get_element_with_key ( mcell, "define_molecules" );
  data_model_element *mols = json_get_element_with_key ( dm_define_molecules, "molecule_list" );

  data_model_element *dm_define_reactions = json_get_element_with_key ( mcell, "define_reactions" );
  data_model_element *rxns = json_get_element_with_key ( dm_define_reactions, "reaction_list" );

  data_model_element *dm_release_sites = json_get_element_with_key ( mcell, "release_sites" );
  data_model_element *rels = json_get_element_with_key ( dm_release_sites, "release_site_list" );


  // Finally build the actual simulation from the data extracted from the data model

  MCellSimulation *mcell_sim = new MCellSimulation();
  mcell_sim->set_seed ( seed );
  mcell_sim->print_detail = print_detail;


  // Define the molecules for this simulation by reading from the data model

  int mol_num = 0;
  data_model_element *this_mol;
  MCellMoleculeSpecies *mol;
  while ((this_mol=json_get_element_by_index(mols,mol_num)) != NULL) {
    mol = new MCellMoleculeSpecies();
    mol->name = json_get_string_value ( json_get_element_with_key ( this_mol, "mol_name" ) );
    mol->diffusion_constant = get_float_from_par ( par_dict, json_get_element_with_key ( this_mol, "diffusion_constant" ) );
    // This allows the molecule to be referenced by name when needed:
    mcell_sim->molecule_species[mol->name.c_str()] = mol;
    mol_num++;
  }
  int total_mols = mol_num;
  if (print_detail > 10) printf ( "Total molecules = %d\n", total_mols );


  // Define the reactions for this simulation by reading from the data model

  int rxn_num = 0;
  data_model_element *this_rxn;
  MCellReaction *reaction;
  while ((this_rxn=json_get_element_by_index(rxns,rxn_num)) != NULL) {
    mcell_sim->has_reactions = true;
    reaction = new MCellReaction();

    char *reactants_str;
    reactants_str = json_get_string_value( json_get_element_with_key ( this_rxn, "reactants" ) );
    char *products_str;
    products_str = json_get_string_value( json_get_element_with_key ( this_rxn, "products" ) );
    cout << "Reaction: " << reactants_str << " -> " << products_str << endl;
    vector<string> reactants_vec = split(string(reactants_str), '+');
    for (string s : reactants_vec) {
      cout << "  Reactant [" << s << "]" << endl;
      if ( s == "NULL" ) {
        cout << "    NULL is not added to reactants" << endl;
      } else {
        reaction->reactants.append ( mcell_sim->molecule_species [ s.c_str() ] );
      }
    }
    vector<string> products_vec = split(string(products_str), '+');
    for (string s : products_vec) {
      cout << "  Product [" << s << "]" << endl;
      if ( s == "NULL" ) {
        cout << "    NULL is not added to products" << endl;
      } else {
        reaction->products.append ( mcell_sim->molecule_species [ s.c_str() ] );
      }
    }
    
    if (reaction->reactants.get_size() != 1) {
      cout << "Warning for " << reactants_str << ": This implementation only supports single reactants ... others ignored" << endl;
    }
    if (reaction->products.get_size() != 0) {
      cout << "Warning for " << products_str << ": This implementation only supports NULL products ... others ignored" << endl;
    }

    reaction->rate = get_float_from_par ( par_dict, json_get_element_with_key ( this_rxn, "fwd_rate" ) );
    mcell_sim->reactions.append ( reaction );
    rxn_num++;
  }
  int total_rxns = rxn_num;
  if (print_detail > 10) printf ( "Total reactions = %d\n", total_rxns );


  // Define the release sites for this simulation by reading from the data model

  int rel_num = 0;
  data_model_element *this_rel;
  MCellReleaseSite *rel;
  while ((this_rel=json_get_element_by_index(rels,rel_num)) != NULL) {
    char *mname = json_get_string_value ( json_get_element_with_key ( this_rel, "molecule" ) );
    rel = new MCellReleaseSite();
    rel->x = get_float_from_par ( par_dict, json_get_element_with_key ( this_rel, "location_x" ) );
    rel->y = get_float_from_par ( par_dict, json_get_element_with_key ( this_rel, "location_y" ) );
    rel->z = get_float_from_par ( par_dict, json_get_element_with_key ( this_rel, "location_z" ) );
    rel->quantity = get_float_from_par ( par_dict, json_get_element_with_key ( this_rel, "quantity" ) );
    rel->molecule_species = mcell_sim->molecule_species[mname];
    mcell_sim->molecule_release_sites.append ( rel );
    rel_num++;
  }
  int total_rels = rel_num;
  if (print_detail > 10) printf ( "Total release sites = %d\n", total_rels );


  // Set final parameters needed to run simulation and Run it

  mcell_sim->num_iterations = iterations;
  mcell_sim->time_step = time_step;

  if (print_detail > 30) mcell_sim->dump_state();

  mcell_sim->run_simulation(proj_path);

  if (print_detail > 0) printf ( "\nDone running ... may still need to free some things ...\n\n" );

  return ( 0 );
}

