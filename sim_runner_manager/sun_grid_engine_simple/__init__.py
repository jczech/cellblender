# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
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
import subprocess
import sys
import time

plug_code = "SGE"
plug_name = "Sun Grid Engine"

def term_all():
    print ( "Terminating all jobs ..." )

def info():
    print ( "Print SGE Information" )

def fetch():
    # Move files as required by parameters
    submit_host = parameter_dictionary['Submit Host']['val']
    project_dir = parameter_dictionary['project_dir']['val']


parameter_dictionary = {
  'Submit Host': {'val': "", 'desc':"Host for SGE Job Submission"},
  'Email': {'val': "", 'desc':"Email address for notification"},
  'Required Memory (G)': {'val': 2, 'desc':"Required Memory for Host Selection"},
  'Best Nodes': {'val': "", 'desc':"List of best nodes to use"},
  'Terminate All': {'val': term_all, 'desc':"Terminate All Jobs"},
  'Information': {'val': info, 'desc':"Print Information"},

  'project_dir': {'val': "", 'desc':"INTERNAL: project directory storage"}
}

parameter_layout = [
  ['Submit Host', 'Email'],
  ['Required Memory (G)', 'Best Nodes'],
  ['Terminate All', 'Information']
]

def find_in_path(program_name):
    for path in os.environ.get('PATH','').split(os.pathsep):
        full_name = os.path.join(path,program_name)
        if os.path.exists(full_name) and not os.path.isdir(full_name):
            return full_name
    return None


def run_engine ( engine_module, data_model, project_dir ):
    command_list = None
    dm = None
    print ( "Calling prepare_runs... in engine_module" )
    if 'prepare_runs_no_data_model' in dir(engine_module):
        command_list = engine_module.prepare_runs_no_data_model ( project_dir )
    elif 'prepare_runs_data_model_no_geom' in dir(engine_module):
        command_list = engine_module.prepare_runs_data_model_no_geom ( data_model, project_dir )
    elif 'prepare_runs_data_model_full' in dir(engine_module):
        command_list = engine_module.prepare_runs_data_model_full ( data_model, project_dir )

    return run_commands ( command_list )


def run_commands ( commands ):
    sp_list = []

    print ( "run_commands" )
    for cmd in commands:
      print ( "  CMD: " + str(cmd['cmd']) + " " + str(cmd['args']) )
      """
      CMD: {
        'args': ['print_detail=20',
                 'proj_path=/.../intro/2017/2017_07/2017_07_11/queue_runner_tests_files/mcell',
                 'seed=1',
                 'data_model=dm.json'],
        'cmd': '/.../blender/2.78/scripts/addons/cellblender/sim_engines/limited_cpp/mcell_main',
        'wd':  '/.../intro/2017/2017_07/2017_07_11/queue_runner_tests_files/mcell',
        'stdout': '',
        'stderr': ''
      }
      """

    # Convert parameter_dictionary entries to convenient local variables
    submit_host = parameter_dictionary['Submit Host']['val']
    email = parameter_dictionary['Email']['val']

    best_nodes = None
    if len ( parameter_dictionary['Best Nodes']['val'] ) > 0:
        best_nodes = parameter_dictionary['Best Nodes']['val']

    min_memory = parameter_dictionary['Required Memory (G)']['val']



    # Figure out a "project_dir" from the common path of the working directories
    project_dir = ""
    paths_list = []
    for cmd in commands:
        if type(cmd) != type({'a':1}):
            print ( "Error: SGE Runner requires engines that produce dictionary commands containing a working directory ('wd') entry" )
            return sp_list
        elif not 'wd' in cmd:
            print ( "Error: SGE Runner requires engines that produce dictionary commands containing a working directory ('wd') entry" )
            return sp_list
        else:
            paths_list.append ( cmd['wd'] )
    project_dir = os.path.commonpath ( paths_list )
    if os.path.split(project_dir)[-1] == 'output_data':
        # Remove the last "output_data" which should be at the end of the path
        project_dir = os.path.sep.join ( os.path.split(project_dir)[0:-1] )
    if os.path.split(project_dir)[-1] == 'mcell':
        # Remove the last "mcell" which should be at the end of the path
        project_dir = os.path.sep.join ( os.path.split(project_dir)[0:-1] )
    print ( "Project Directory = " + project_dir )

    parameter_dictionary['project_dir']['val'] = project_dir


    # Build 1 master qsub file and a job file for each MCell run

    master_job_list_name = os.path.join ( project_dir, "master_job_list.sh" )
    master_job_list = open ( master_job_list_name, "w" )
    master_job_list.write ( 'echo "Start of master job list"\n' )
    master_job_list.write ( "cd %s\n" % os.path.join(project_dir,"mcell","output_data") )
    job_index = 0
    for run_cmd in commands:

        job_filename = "job_%d.sh" % (job_index)
        job_filepath = os.path.join(project_dir, job_filename)

        log_filename = "log_%d.txt" % (job_index)
        log_filepath = os.path.join(project_dir, log_filename)

        error_filename = "error_%d.txt" % (job_index)
        error_filepath = os.path.join(project_dir, error_filename)

        job_file = open(job_filepath,"w")
        job_file.write ( "cd %s\n" % run_cmd['wd'] )
        full_cmd = run_cmd['cmd']
        if len(run_cmd['args']) > 0:
          full_cmd = full_cmd + " " + " ".join(run_cmd['args'])
        job_file.write ( full_cmd + "\n" )
        job_file.close()

        qsub_command = "qsub"
        # qsub_command += " -wd " + subprocess_cwd
        qsub_command += " -o " + log_filepath
        qsub_command += " -e " + error_filepath
        resource_list = []
        if best_nodes != None:
            resource_list.append ( "h=" + best_nodes[job_index%len(best_nodes)][0] )
        if min_memory > 0:
            resource_list.append ( "mt=" + str(min_memory) + "G" )
        if len(resource_list) > 0:
            qsub_command += " -l " + ",".join(resource_list)
        if len(email) > 0:
            qsub_command += " -m e"
            qsub_command += " -M " + email
        qsub_command += " " + job_filepath

        master_job_list.write ( qsub_command + "\n" )

        job_index += 1


    master_job_list.write ( 'echo "End of master job list"\n' )
    master_job_list.close()
    os.chmod ( master_job_list_name, 0o740 )  # Must make executable

    args = ['ssh', submit_host, master_job_list_name ]
    print ( "Args for Popen: " + str(args) )
    p = subprocess.Popen ( args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )

    pi = p.stdin
    po = p.stdout
    pe = p.stderr

    print ( "Waiting for something from subprocess ..." )
    count = 0
    while len(po.peek()) == 0:
        # Wait for something
        time.sleep ( 0.01 )
        count = count + 1
        if count > 100:
            break

    print ( "Waiting for pause from subprocess..." )
    count = 0
    while (len(po.peek()) > 0) and (count < 1000):
        # Wait for nothing
        # time.sleep ( 0.01 )
        if b'\n' in po.peek():
            line = str(po.readline())
            print ( "J: " + str(line) )
            count = 0
        count = count + 1
        # print ( "Count = " + str(count) )
        #if b"nothing" in po.peek():
        #  break
    #print ( "Terminating subprocess..." )
    #p.kill()

    return sp_list.append ( p )


if __name__ == "__main__":
    print ( "Called with __name__ == __main__" )
    pass
