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

#

import os
import subprocess


engine_code = "PUREPYTHON"
engine_name = "Pure Python"
engine_input = "dm"  # May be "dm", "dmg", or "blender"

def prepare_run_command_list ( data_model ):
    pass


def run_commands ( commands, cwd="" ):
    sp_list = []
    for cmd in commands:
        shared_path = os.path.dirname ( os.path.dirname ( os.path.dirname(os.path.realpath(__file__)) ) )
        command_list = [ "python3", os.path.join(shared_path,"sim_engines","libMCell","pure_python_sim.py") ]
        command_list.append ( "proj_path="+cwd )
        command_list.append ( "data_model=dm.txt" )
        
        print ( "Command List: " + str(command_list) )
        sp_list.append ( subprocess.Popen ( command_list, cwd=cwd, stdout=None, stderr=None ) )
    return sp_list


if __name__ == "__main__":
    print ( "Called with __name__ == __main__" )
    pass

