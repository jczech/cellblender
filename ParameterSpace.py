#!/usr/bin/env python
from math import *
from random import uniform, gauss
import parser
import re
import token
import symbol
import sys
import time
# from pdb import set_trace as debug # Debug help from Lee

# from math import *
#from math import sqrt, exp, log, log10, sin, cos, tan, asin, acos, atan, ceil, floor  # abs, max, and min are not from math?
#from random import uniform, gauss


####################### Start of Profiling Code #######################

# Adapted from: http://wiki.blender.org/index.php/User:Z0r/PyDevAndProfiling

prof = {}

# Defines a dictionary associating a call name with a list of 3 (now 4) entries:
#  0: Name
#  1: Duration
#  2: Count
#  3: Start Time (for non-decorated version)
#  4: Min
#  5: Max
PROF_NAME = 0
PROF_DURATION = 1
PROF_COUNT = 2
PROF_START = 3
PROF_MIN = 4
PROF_MAX = 5

class profile:
    ''' Function decorator for code profiling.'''

    def __init__(self,name):
        self.name = name

    def print_call_stack(self):
        frame = inspect.currentframe()
        call_list_frames = inspect.getouterframes(frame)
        filtered_frames = [ {"function":f.function, "line":f.lineno, "file":f.filename} for f in call_list_frames if not ( f.function in ("execute", "print_frame", "profile_fun", "draw", "draw_self", "draw_layout") ) ]

        if len(filtered_frames) > 0:
            filtered_frames.reverse()
            s = ""
            last_call = ""
            num_repeat = 0
            sep = " ->  "
            for f in filtered_frames:
                # this_call = str(f["function"]) + '[' + str(f["line"]) + ' in ' + str(f["file"].split('/')[-1].split('.')[0]) + ']'
                this_call = str(f["function"]).strip()
                if this_call == last_call:
                    num_repeat += 1
                else:
                    repeat_str = num_repeat * "*"
                    #if len(repeat_str) > 0:
                    #    repeat_str = " " + repeat_str + " "
                    s += last_call + repeat_str + sep
                    num_repeat = 0
                    last_call = this_call
                # print ( "    Frame: " + str(f.function) + " at " + str(f.lineno) + " in "  + str(f.filename.split('/')[-1].split('.')[0]) )
            if num_repeat > 0:
                s += last_call + (num_repeat * "*") + sep
            s = s[len(sep):-len(sep)]
            if len(s) > 0:
                print ( s )

        del filtered_frames
        del call_list_frames
        del frame

    def __call__(self,fun):
        def profile_fun(*args, **kwargs):
            #self.print_call_stack()               # This will print the call stack as each function is called
            start = time.clock()
            try:
                return fun(*args, **kwargs)
            finally:
                duration = time.clock() - start
                if fun in prof:
                    prof[fun][PROF_DURATION] += duration
                    prof[fun][PROF_COUNT] += 1
                    if duration < prof[fun][PROF_MIN]:
                        prof[fun][PROF_MIN] = duration
                    if duration > prof[fun][PROF_MAX]:
                        prof[fun][PROF_MAX] = duration
                else:
                    prof[fun] = [self.name, duration, 1, 0, duration, duration]
        return profile_fun

# Builds on the previous profiling code with non-decorated versions (needed by some Blender functions):
#  0: Name
#  1: Duration
#  2: Count
#  3: Start Time (for non-decorated version)

def start_timer(fun):
    start = time.clock()
    if fun in prof:
        prof[fun][PROF_COUNT] += 1
        prof[fun][PROF_START] = start
    else:
        prof[fun] = [fun, 0, 1, start, 1e9, 0]

def stop_timer(fun):
    stop = time.clock()
    if fun in prof:
        duration = stop - prof[fun][PROF_START]   # Duration = Stop - Start
        prof[fun][PROF_DURATION] += duration
        if duration < prof[fun][PROF_MIN]:
            prof[fun][PROF_MIN] = duration
        if duration > prof[fun][PROF_MAX]:
            prof[fun][PROF_MAX] = duration
        # prof[fun][PROF_COUNT] += 1
    else:
        print ( "Timing Error: stop called without start!!" )
        pass

def print_statistics():
    '''Prints profiling results to the console.'''

    def timekey(stat):
        return stat[1] / float(stat[2])

    stats = sorted(prof.values(), key=timekey, reverse=True)

    print ( '{:<55} {:>7} {:>7} {:>8} {:>8} {:>8}'.format('FUNCTION', 'CALLS', 'SUM(ms)', 'AV(ms)', 'Min(ms)', 'Max(ms)'))
    for stat in stats:
        print ( '{:<55} {:>7} {:>7.0f} {:>8.2f} {:>8.2f} {:>8.2f}'.format(stat[0],stat[2],stat[1]*1000,(stat[1]/float(stat[2]))*1000,stat[4],stat[5]))



####################### End of Profiling Code #######################


print ( "ParameterSpace.py being processed ..." )

class ParameterSpace:

    """ Encapsulate a parameter space with mutable parameter names associated with parameter expressions:

        IDs currently run from 1 to n, with negative IDs typically indicating an error. ID 0 is unused.
        The expression for each parameter is always valid (default is "0"). It cannot contain any negative ids.
        When an invalid expression is defined, the original expression remains in effect, and the invalid
          expression is stored and displayed along with the original (current) expression.
        It is not allowable to delete a parameter which is used in other parameter expressions.
        
    """

    @profile('ParameterSpace.__init__')
    def __init__ ( self ):
        """ Initialize a new ParameterSpace """
        #print ( "ParameterSpace.__init__() called" )
        self.VERSION = self.get_version()
        self.EXPRESSION_KEYWORDS = { '^': '**', 'SQRT': 'sqrt', 'EXP': 'exp', 'LOG': 'log', 'LOG10': 'log10', 'SIN': 'sin', 'COS': 'cos', 'TAN': 'tan', 'ASIN': 'asin', 'ACOS':'acos', 'ATAN': 'atan', 'ABS': 'abs', 'CEIL': 'ceil', 'FLOOR': 'floor', 'MAX': 'max', 'MIN': 'min', 'RAND_UNIFORM': 'uniform', 'RAND_GAUSSIAN': 'gauss', 'PI': 'pi', 'SEED': '1' }
        self.UNDEFINED_NAME = "   (0*1111111111*0)   "
        self.init_param_space()

    @profile('ParameterSpace.get_version')
    def get_version ( self ):
        return ( 0.002 )  # N O T E: This constant is in the function to keep it from being saved when pickling!!!
    
    @profile('ParameterSpace.version_match')
    def version_match ( self ):
        if self.VERSION == self.get_version():
            return True
        else:
            return False

    @profile('ParameterSpace.init_param_space')
    def init_param_space ( self ):
        #print ( "Init_param_space called" )
        self.name_ID_dict = {}  # Maps string names to integer IDs
        self.ID_name_dict = {}  # Maps IDs to string names
        self.ID_expr_dict = {}  # Maps IDs to expression list containing either string literals or integer IDs
        self.ID_value_dict = {}  # Maps IDs to their current value as a string
        self.ID_error_dict = {}  # When not None this contains an expression that needs further editing because it is in error
        self.ID_valid_dict = {}  # Boolean value for each parameter indicating that it's value is valid with respect to all other parameters - This is NOT an indication of the validity of the expression!!!
        self.next_available_id = 1
        # self.next_id = 1

    @profile('ParameterSpace.delete_all')
    def delete_all ( self ):
        """ Delete all parameters """
        self.init_param_space()


    @profile('ParameterSpace.num_parameters')
    def num_parameters ( self ):
        return ( len(self.ID_name_dict) )

    #@profile('ParameterSpace.get_next_id')
    #def get_next_id ( self ):
    #    return self.next_id

    @profile('ParameterSpace.get_id_list')
    def get_id_list ( self ):
        return self.ID_name_dict.keys()


    @profile('ParameterSpace.dump')
    def dump ( self, prnt=False ):
        # For right now, this function defaults to silence (an easy way to turn it on and off globally)
        if prnt:
            print ( " Parameter space:" )
            print ( "  next_available_id = " + str(self.next_available_id) )
            print ( "  name->ID = " + str(self.name_ID_dict) )
            print ( "  ID->name = " + str(self.ID_name_dict) )
            print ( "  ID->expr = " + str(self.ID_expr_dict) )
            print ( "  ID->valu = " + str(self.ID_value_dict) )
            print ( "  ID->erro = " + str(self.ID_error_dict) )
            print ( "  ID->vali = " + str(self.ID_valid_dict) )
            for i in self.ID_name_dict:
                #print ( "    " + str(self.ID_name_dict[i]) + " = " + str(self.ID_value_dict[i]) + " = " + self.get_expr(i) + " = " + self.get_expr(i,to_py=True) + " = " + str(self.ID_expr_dict[i]) )

                print ( "    " + str(i) + ": name  = " + str(self.ID_name_dict[i])  )
                print ( "    " + str(i) + ": value = " + str(self.ID_value_dict[i]) )
                print ( "    " + str(i) + ": expr  = " + self.get_expr(i) )
                print ( "    " + str(i) + ": pyexp = " + self.get_expr(i,to_py=True) )
                print ( "    " + str(i) + ": idexp = " + str(self.ID_expr_dict[i]) )
                print ( "    " + str(i) + ": error = " + str(self.ID_error_dict[i]) )
                print ( "    " + str(i) + ": valid = " + str(self.ID_valid_dict[i]) )

                #print ( "    " + str(self.ID_name_dict[i]) + " = " + self.get_expr(i) + " = " + self.get_expr(i,to_py=True) + " = " + str(self.ID_expr_dict[i]) )
            self.eval_all(True)


    @profile('ParameterSpace.print_keywords')
    def print_keywords ( self ):
        for mdl_keyword in self.EXPRESSION_KEYWORDS:
            print ( "  " + mdl_keyword + " = " + self.EXPRESSION_KEYWORDS[mdl_keyword] )


    """
    The following functions (define, set_expr, and get_expr) provide the core functionality
      for setting and getting expressions.
    """

    @profile('ParameterSpace.define')
    def define ( self, name, expr ):
        """ Define a parameter ... may be new or may overwrite an existing parameter"""
        """ Return the ID of this parameter whether it's new or not """
        # print "Define: " + str(name) + " = " + str(expr)

        #next_available_id = 1;
        #while next_available_id in self.ID_name_dict:
        #    # print ( "Can't use ", next_available_id )
        #    next_available_id += 1
        # self.next_id = next_available_id

        if name == None:
            # Try to choose a name (P#) with this next ID if possible, but search further as needed
            next_unused_number = self.next_available_id
            while self.get_id( "P%d" % (next_unused_number) ) != None:
                # This name is in use ... possibly by explicit declaration: P999 = 5
                next_unused_number += 1
            name = "P%d" % (next_unused_number)
            #if next_unused_number == self.next_available_id:
            #    # The next_available_id has been used:
            #    self.next_available_id += 1

        this_id = -1
        if name in self.name_ID_dict:
            # This parameter already exists, so just update its expression
            # print ( "Parameter " + name + " already exists, so just update the expression" )
            this_id = self.get_id(name)
            self.set_expr ( this_id, expr )
        else:
            # This is a new name, so make a new entry
            # print ( "Parameter " + name + " is new, so make new name/ID entries as well as update the expression" )
            this_id = self.next_available_id
            self.next_available_id += 1
            self.name_ID_dict[name] = this_id
            self.ID_name_dict[this_id] = name
            # Always set the default ("original") value to 0
            self.ID_expr_dict[this_id] = "0"
            # Now try to set the expression
            # Note that set_expr will validate the expression before replacing the current one.
            #  If the new expression is not valid, it will not replace the current expression and
            #  instead, it will update the error expression.
            self.set_expr ( this_id, expr )
            """
            # self.next_id += 1
            # This would be a place to search for the first unused id rather than simply incrementing the next_id
            next_available_id = 1;
            while next_available_id in self.ID_name_dict:
                print ( "Can't use ", next_available_id )
                next_available_id += 1
            self.next_id = next_available_id
            """
        return this_id


    @profile('ParameterSpace.set_expr')
    def set_expr ( self, parid, expr, reeval_all=True ):
        """ Store original text and parse and store the expression for the specified parameter ID """
        # self.ID_error_dict[parid] = expr  # This may be redundant, but is here for clarity
        parsed_expr = self.parse_param_expr ( expr )


        # Try parsing a second time to catch forward references?  Is this still needed with newer code?
        # parsed_expr = self.parse_param_expr ( expr )

        if (parsed_expr == None) or (-1 in parsed_expr):
            # There was an error in the string expression, so save the error version and don't change anything else
            self.ID_error_dict[parid] = expr
        else:
            # The expression parsed fine, so set error version to None, update the expression, and evaluate it's value
            self.ID_error_dict[parid] = None
            self.ID_expr_dict[parid] = parsed_expr
            self.ID_valid_dict[parid] = False
            if reeval_all:
                self.eval_all()
            self.ID_value_dict[parid] = self.get_value(parid)


    @profile('ParameterSpace.get_expr')
    def get_expr ( self, parid, to_py=False ):
        """ Construct a string representation of the expression by substituting symbols for IDs """
        exp_list = self.ID_expr_dict[parid]
        expr = ""
        for token in exp_list:
            if type(token) == int:
                # This is an integer parid, so look up the variable name to concatenate
                if token in self.ID_name_dict:
                    expr = expr + self.ID_name_dict[token]
                else:
                    # In previous versions, this case might have defined a new parameter here.
                    # In this version, it should never happen, but appends an undefined name ... just in case!!
                    expr = expr + self.UNDEFINED_NAME
            else:
                # This is a string so simply concatenate it after translation as needed
                if to_py and (token in self.EXPRESSION_KEYWORDS):
                    expr = expr + self.EXPRESSION_KEYWORDS[token]
                else:
                    expr = expr + token
        return expr



    """
    These functions (get_dependents_list and get_dependents_names) find parameters
    that reference the requested ID.
    """

    @profile('ParameterSpace.get_dependents_list')
    def get_dependents_list ( self, parid ):
        """ Return a list of all parameter ids that reference this parameter id directly """
        dependents = []
        for test_id in self.ID_expr_dict:
            exp_list = self.ID_expr_dict[test_id]
            for token in exp_list:
                if type(token) == int:
                    if token == parid:
                        dependents = dependents + [ test_id ]
                        break
        return dependents


    @profile('ParameterSpace.get_dependents_names')
    def get_dependents_names ( self, parid ):
        """ Return a list of all parameter names that reference this parameter id directly """
        dlist = self.get_dependents_list(parid)
        if len(dlist) > 0:
            dlist = [self.get_name(i) for i in dlist]
        return dlist



    """
    These functions (get_depend_list and get_depend_dict) find parameters that
    are referenced by the requested id.
    """

    @profile('ParameterSpace.get_depend_list')
    def get_depend_list ( self, parid ):
        """ Construct a list of ids that this id depends upon (or is a function of) """
        exp_list = self.ID_expr_dict[parid]
        depends_on = set ( [] )
        for token in exp_list:
            if type(token) == int:
                depends_on.add ( token )
        return [ x for x in depends_on ]


    @profile('ParameterSpace.get_depend_dict')
    def get_depend_dict ( self, parid ):
        """ Construct a dictionary of ids and names that this id depends upon (or is a function of) """
        exp_list = self.ID_expr_dict[parid]
        depends_on = {}
        for token in exp_list:
            if type(token) == int:
                depends_on.update ( {token : self.get_name(token)} )
        return depends_on


    @profile('ParameterSpace.all_valid')
    def all_valid ( self ):
        # Check to see if all values are currently valid
        valid = True
        for parid in self.ID_name_dict:
            if self.ID_error_dict[parid] != None:
                valid = False
                break
            if not self.ID_valid_dict[parid]:
                valid = False
                break
        return ( valid )


    """
    These functions delete parameters.
    """    

    @profile('ParameterSpace.absolute_delete')
    def absolute_delete ( self, parid ):
        """ Delete a parameter """
        name = self.get_name ( parid )
        if name != None:
            self.name_ID_dict.pop(name)
            self.ID_name_dict.pop(parid)
            self.ID_expr_dict.pop(parid)
            self.ID_value_dict.pop(parid)
            self.ID_error_dict.pop(parid)
            self.ID_valid_dict.pop(parid)
            if len(self.name_ID_dict) <= 0:
                # Reset the ID numbers when the list becomes empty
                self.next_available_id = 1

    @profile('ParameterSpace.delete')
    def delete ( self, parid ):
        """ Delete a parameter only if it has no dependencies """
        dependents = self.get_dependents_list(parid)
        if len(dependents) == 0:
          self.absolute_delete ( parid )
          return True
        else:
          return False


    """
    These are general purpose "get" and "set" functions that don't do
       much processing.
    """

    @profile('ParameterSpace.get_id')
    def get_id ( self, name ):
        """ Get the ID of a parameter by name """
        #Speed: This checking and then getting is a double access ... might be better with try/except?
        if (len(self.name_ID_dict) > 0) and (name in self.name_ID_dict):
            return self.name_ID_dict[name]
        else:
            return None

    @profile('ParameterSpace.get_name')
    def get_name ( self, parid ):
        """ Get the name of the parameter with the specified ID """
        if parid in self.ID_name_dict:
            return self.ID_name_dict[parid]
        else:
            return None

    @profile('ParameterSpace.get_error')
    def get_error ( self, parid ):
        """ Get the text expression that is currently in error for the specified parameter ID """
        if parid in self.ID_error_dict:
            return self.ID_error_dict[parid]
        else:
            return None

    @profile('ParameterSpace.get_value')
    def get_value ( self, parid ):
        """ Get the current value for the specified parameter ID """
        if parid in self.ID_value_dict:
            return self.ID_value_dict[parid]
        else:
            return None

    @profile('ParameterSpace.set_name')
    def set_name ( self, parid, name ):
        """ Change the name of the parameter for the specified ID returning a boolean success value"""
        old_name = self.get_name ( parid )
        if old_name != None:
            self.ID_name_dict[parid] = name
            self.name_ID_dict[name] = self.name_ID_dict.pop(old_name)
            return True
        return False


    @profile('ParameterSpace.rename')
    def rename ( self, old_name, new_name, illegal_names=None ):
        """ Rename a parameter returning a boolean success value """
        if illegal_names != None:
          if new_name in illegal_names:
              # Can't rename to an illegal name
              return False
        parid = self.get_id ( old_name )
        if parid < 0:
            # Old name doesn't exist so it can't be renamed
            return False
        else:
            new_id = self.get_id ( new_name )
            if new_id != None:
                # New name already exists so a duplicate name can't be created
                return False
            else:
                # It's ok to rename, so update the two dictionaries that associate names and IDs
                self.ID_name_dict[parid] = new_name
                self.name_ID_dict[new_name] = self.name_ID_dict.pop(old_name)
                return True



    """
    These are the parsing and evaluation functions.
    These functions currently rely on the python parsing and evaluation capabilities.
    """



    @profile('ParameterSpace.eval_all')
    def eval_all ( self, prnt=False, requested_id=None, expression=None ):
    
        # Re-parse any parameters that remain unparsed

        for parid in self.ID_name_dict:
            if self.ID_error_dict[parid] != None:
                self.set_expr ( parid, self.ID_error_dict[parid], reeval_all=False )

        # Evaluate assuming either ordered or unordered parameters    

        # (requested_val, valid) = self.eval_all_ordered ( self, prnt=prnt, requested_id=requested_id, expression=expression )
        (requested_val, valid) = self.eval_all_any_order ( prnt=prnt, requested_id=requested_id, expression=expression )

        if prnt:
            if (requested_id == None) or (requested_id == -1):
                print ( "==============================================================================" )

            for parid in self.ID_name_dict:
                if (requested_id == None) or (requested_id == -1) or (requested_id == parid):
                    error_string = ""
                    if self.get_error(parid) != None:
                        error_string = ", *** Error Pending: " + self.get_error(parid)
                    print ( str(parid) + ": " + self.get_name(parid) + 
                            " = " + str(self.get_value(parid)) + 
                            " = \'" + self.get_expr ( parid, to_py=True ) + "\'" +
                            " = \"" + self.get_expr ( parid, to_py=False ) + "\"" +
                            ", " + self.get_name(parid) + 
                            " depends on " + str(self.get_depend_list(parid)) + 
                            ", " + self.get_name(parid) + 
                            " is referenced by " + str(self.get_dependents_list(parid)) + error_string )

            if (requested_id == None) or (requested_id == -1):
                print ( "==============================================================================" )

        if prnt:
            if not self.all_valid():
                print ( "!!!!!!!!! WARNING: ERROR OR CIRCULAR REFERENCE !!!!!!!!!!!!" )

        if expression != None:
            # Only return the valid flag for expressions because the information is in the database for parameters
            return (requested_val, valid)

        return requested_val


    @profile('ParameterSpace.eval_all_ordered')
    def eval_all_ordered ( self, prnt=False, requested_id=None, expression=None ):
        """ Evaluate all parameters in order, printing either a requested ID or all (-1) when prnt is True """

        # from math import *
        #from math import sqrt, exp, log, log10, sin, cos, tan, asin, acos, atan, ceil, floor  # abs, max, and min are not from math?
        #from random import uniform, gauss

        requested_val = 0
        valid = True

        if requested_id == None:
            requested_id = -1   # This eliminated the need to check the type for NoneType all the time!!
        
        # Loop through as many times as IDs to ensure catching all non-circular dependencies (forward references):

        for pass_num in self.ID_name_dict:

            something_changed = False

            for parid in self.ID_name_dict:
                py_statement = self.get_name(parid) + " = " + self.get_expr ( parid, to_py=True )
                #py_statement = "{0} = {1}".format( self.get_name(parid), self.get_expr ( parid, to_py=True ) )
                #debug() # help from Lee
                try:
                    exec ( py_statement )
                    val = eval ( self.get_name(parid), locals() )
                    
                    # Check for changes ...
                    if parid in self.ID_value_dict:
                        # The parameter is already there, so check if it's different
                        if str(val) != self.ID_value_dict[parid]:
                            something_changed = True
                    else:
                        # If it wasn't there, then this is a change!!
                        something_changed = True

                    self.ID_value_dict[parid] = str(val)
                    if (requested_id == parid):
                        requested_val = val
                except:
                    valid = False
                    print ( "==> Evaluation Exception: " + str ( sys.exc_info() ) )
                    if prnt:
                        print ( "  Error in statement:   " + self.get_name(parid) + " = " + self.get_error(parid) )
                        print ( "    ... interpreted as: " + py_statement )

            if something_changed == False:
                break

        if expression != None:
            # Evaluate the requested expression in the context of the variables that have already been evaluated:
            try:
                val = eval ( expression, locals() )
                requested_val = val
            except:
                valid = False
                print ( "==> Evaluation Exception: " + str ( sys.exc_info() ) )
                if prnt:
                    print ( "  Error in statement:   " + expression )
            
        return (requested_val, valid)



    @profile('ParameterSpace.eval_all_any_order')
    def eval_all_any_order ( self, prnt=False, requested_id=None, expression=None ):
        """ Evaluate all parameters based on dependencies. """

        # from math import *
        #from math import sqrt, exp, log, log10, sin, cos, tan, asin, acos, atan, ceil, floor  # abs, max, and min are not from math?
        #from random import uniform, gauss
        
        requested_val = 0
        valid = True

        # Start by marking all parameters as invalid

        for parid in self.ID_name_dict:
            self.ID_valid_dict[parid] = False
        
        # Loop through all parameters over and over evaluating those parameters with valid dependencies
        
        num_passes = 0

        while (num_passes <= len(self.ID_name_dict)) and (self.all_valid() == False):

            num_passes = num_passes + 1

            # Visit each parameter
            for parid in self.ID_name_dict:

                # Only need to update parameters with invalid values
                if not self.ID_valid_dict[parid]:

                    # Check to see if this parameter can be updated based on ALL of its dependencies being valid
                    dep_list = self.get_depend_list ( parid )
                    dep_satisfied = True
                    for dep_id in dep_list:
                        if not self.ID_valid_dict[dep_id]:
                            dep_satisfied = False
                            break
                    if dep_satisfied:
                        # It's OK to evaluate this parameter
                        
                        something_changed = False
                        py_statement = ""
                        try:
                            py_statement = str(str(self.get_name(parid))) + " = " + str(self.get_expr ( parid, to_py=True ))
                            exec ( py_statement )
                            val = eval ( self.get_name(parid), locals() )
                            
                            # Check for changes ...
                            if parid in self.ID_value_dict:
                                # The parameter is already there, so check if it's different
                                if str(val) != self.ID_value_dict[parid]:
                                    something_changed = True
                            else:
                                # If it wasn't there, then this is a change!!
                                something_changed = True

                            self.ID_value_dict[parid] = str(val)
                            if (requested_id == parid):
                                requested_val = val
                        except:
                            valid = False
                            print ( "==> Evaluation Exception: " + str ( sys.exc_info() ) )
                            if prnt:
                                print ( "  Error in statement:   " + self.get_name(parid) + " = " + self.get_error(parid) )
                                print ( "    ... interpreted as: " + py_statement )

                        self.ID_valid_dict[parid] = True

        # End While

        if expression != None:
            # Evaluate the requested expression in the context of the variables that have already been evaluated:
            try:
                val = eval ( expression, locals() )
                requested_val = val
            except:
                valid = False
                print ( "==> Evaluation Exception: " + str ( sys.exc_info() ) )
                if prnt:
                    print ( "  Error in statement:   " + expression )

        return ( requested_val, valid )





    @profile('ParameterSpace.parse_param_expr')
    def parse_param_expr ( self, param_expr ):
        """ Converts a string expression into a list expression with variable id's as integers and all others as strings
            Returns either a list (if successful) or None if there is an error
            Example:
              Expression: "A * (B + C)" becomes something like: [ 3, "*", "(", 22, "+", 5, ")", "" ]
                 where 3, 22, and 5 are the ID numbers for parameters A, B, and C respectively
              Note that the parsing may produce empty strings in the list which should not cause any problem.
        """
        param_expr = param_expr.strip()
        st = None
        pt = None
        try:
            st = parser.expr(param_expr)
            pt = st.totuple()
        except:
            print ( "==> Parsing Exception: " + str ( sys.exc_info() ) )

        parameterized_expr = None  # param_expr
        if pt != None:
        
            parameterized_expr = self.recurse_tree_symbols ( pt, [] )
            
            if parameterized_expr != None:
            
                # Remove trailing empty strings from parse tree - why are they there?
                while len(parameterized_expr) > 0:
                    if parameterized_expr[-1] != '':
                        break
                    parameterized_expr = parameterized_expr[0:-2]

        return parameterized_expr



    @profile('ParameterSpace.recurse_tree_symbols')
    def recurse_tree_symbols ( self, pt, current_expr ):
        """ Recurse through the parse tree looking for "terminal" items which are added to the list """

        # Strip off the outer layers that are not of interest
        while (type(pt) == tuple) and (len(pt) == 2) and (type(pt[1]) == tuple):
            # print ( "  changing " + str(pt) + " to " + str(pt[1]) )
            pt = pt[1]

        if type(pt) == tuple:
            # This is a tuple, so find out if it's a terminal leaf in the parse tree
            # Note: This code didn't use the token.ISTERMINAL function.
            # It might have been written as:
            #   terminal = False
            #   if len(pt) > 0:
            #     if token.ISTERMINAL(pt[0]):
            #       terminal = True
            # However, that doesn't check that the terminal is a 2-tuple containing a string

            #print ( "recurse_tree_symbols with a tuple (", current_expr, ")" )
            #print ( "  pt = ", str(pt) )

            terminal = False
            if len(pt) == 2:
                if type(pt[1]) == str:
                    terminal = True

            if terminal:
                # This is a 2-tuple with a type and value
                if pt[0] == token.NAME:
                    # This is a name (either a keyword or a user-defined name)
                    if pt[1] in self.EXPRESSION_KEYWORDS:
                        # This is a recognized name and not a user-defined symbol, so append the string itself
                        # return current_expr + [ pt[1] ]
                        return current_expr.append ( pt[1] )
                    else:
                        # This must be a user-defined symbol
                        par_id = self.name_ID_dict.setdefault(pt[1],-1)  # This statement takes the place of following 3:
                        #par_id = -1
                        #if pt[1] in self.name_ID_dict:
                        #    par_id = self.name_ID_dict[pt[1]]
                        return current_expr.append ( par_id )
                else:
                    # This is a non-name part of the expression
                    return current_expr.append ( pt[1] )
            else:
                # Break it down further
                for i in range(len(pt)):
                    next_segment = self.recurse_tree_symbols ( pt[i], current_expr )
                    if next_segment != None:
                        current_expr = next_segment
                return current_expr
        return None
    

###############   T E S T    C O D E   ##################
"""
To run in debugger:
$ python3
>>> import pdb
>>> import ParameterSpace
>>> pdb.run('ParameterSpace')
(Pdb) h

"""

@profile('generate_n_depending_on_all')
def generate_n_depending_on_all ( ps, count ):
    # Generate n parameters each depending on all previous
    print ( "Generating " + str(count) + " parameters each depending on all previous" )
    for i in range(count):
        name = ("p%s" % i)
        if i == 0:
            expr = "1.0"
        else:
            expr = "("
            for j in range(i):
                if j > 0:
                    expr = expr + "+"
                expr = expr + ("p%s" % j)
            expr = expr + ")"
        # print ( "Defining parameter \"" + str(name) + "\" with expression: " + str(expr) )
        ps.define ( name, expr )


if __name__ == "__main__":

    import traceback
    import sys
    import pickle

    ps = ParameterSpace()

    s = "?" # Initialize with the command for help
    while True:
        try:
            s = s.strip()
            if s == '?':
                print ( "" )
                print ( " Expression Keywords: MDL = Python" )
                ps.print_keywords()
                print ( "" )
                print ( " Commands:" )
                print ( "  ? : Print help" )
                print ( "  >> : Enter Python interactive mode" )
                print ( "  Enter : Print All Parameters ... one line each" )
                print ( "  \ : Dump All Parameters ... in great detail" )
                print ( "  ! : Dump Parameters object as a pickled string" )
                print ( "  expression : Evaluate expression" )
                print ( "  param = expression : Assign expression to parameter" )
                print ( "  old @ new : Rename parameter old to new" )
                print ( "  # n [m]: Generate n parameters where each is the sum of the all previous [or m previous]" )
                print ( "  .par : Delete Parameter par" )
                print ( "  . : Delete All Parameters" )
                print ( "  % : Print Profiling" )
                print ( "  %% : Clear Profiling" )
                print ( "  $ : Run a test case" )
                print ( "  Control-C or Control-D : Exit program" )
                print ( "" )
            elif s.strip().startswith ( ">>" ):
                __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

            elif '=' in s:
                # Perform an assignment
                sparts = s.split('=')
                lhs = sparts[0].strip()
                rhs = sparts[1].strip()
                if len(lhs) == 0:
                    lhs = None
                parid = ps.define ( lhs, rhs )
                ps.eval_all(True, parid)
                    
            elif s == '\\':
                # Dump all parameters
                ps.dump(True)
            elif s == '!':
                # Dump all parameters as a pickled object
                s = pickle.dumps(ps,protocol=0)
                print ( "Length = " + str(len(s)) + ", String = ", s )
            elif s == '.':
                # Delete all parameters
                print ( "Deleting all" )
                ps.delete_all()
            elif (len(s) > 0) and (s.strip().startswith ( "#" )):  # This case should come after the "##" case
                # Generate n parameters each depending on previous 3
                pars = [ p for p in s.strip()[1:].split(' ') if len(p) > 0 ]
                count = int(pars[0])
                if len(pars) > 1:
                    offset = int(pars[1])
                    print ( "Generating " + str(count) + " parameters each depending on previous " + str(offset) )
                    for i in range(count):
                        name = ("p%s" % i)
                        if i == 0:
                            expr = "1.0"
                        else:
                            expr = "("
                            n = min(i,offset)  # Constant value limits the number of parameters in each expression
                            for j in range(n):
                                if j > 0:
                                    expr = expr + "+"
                                expr = expr + ("p%s" % (j+i-n))
                            expr = expr + ") / (" + pars[1] + ")"
                        ps.define ( name, expr )
                else:
                    generate_n_depending_on_all ( ps, count )
                print ( "Evaluating all..." )
                ps.eval_all(False)
            elif (len(s) > 0) and (s[0] == '.'):
                # Delete selected parameter
                name = s[1:].strip()
                print ( "Deleting " + name )
                parid = ps.get_id ( name )
                if parid < 0:
                    print ( "Unable to delete " + name + " because it is not a valid parameter name" )
                else:
                    ok = ps.delete ( parid )
                    if not ok:
                        print ( "Unable to delete " + name + " because it is used by " + str(ps.get_dependents_names(parid)) )
            elif (len(s) > 0) and ("@" in s):
                # Rename old to new
                old,new = s.split("@")
                old = old.strip()
                new = new.strip()
                print ( "Renaming " + old + " to " + new )
                ok = ps.rename ( old, new )
                if not ok:
                    print ( "Unable to rename " + old + " to because it is not a valid parameter name" )
            elif (len(s) > 0) and (s == "%%"):
                # Clear profiling
                prof.clear()
            elif (len(s) > 0) and (s == "%"):
                # Print profiling
                print_statistics()
            elif (len(s) > 0) and (s == "$"):
                # Run a test case
                ps.define ( 'a', '3' )
                ps.delete ( ps.get_id('a') )
                ps.define ( 'a', '4' )
                ps.define ( 'b', '5' )
                ps.define ( 'cc', 'a+b' )
                ps.rename ( 'cc', 'c' )
                ps.define ( 'a', '3' )
                ps.delete ( 'a' )  # This should not be allowed
                ps.rename ( 'a', 'A' )
                print ( "A,b,c = " + str(ps.get_value(ps.get_id('A'))) + "," + str(ps.get_value(ps.get_id('b'))) + "," + str(ps.get_value(ps.get_id('c'))) )
            elif s != '':
                # Assume s is an expression to evaluate and print
                (value,valid) = ps.eval_all ( expression=s )
                if valid:
                    print ( "  = " + str ( value ) )
                else:
                    print ( "  = " + str ( value ) + " ... with Error" )
            else:
                # Print all parameters
                ps.eval_all(True)
        except KeyboardInterrupt:
            print ( "Exiting" )
            sys.exit(0)
        except:
            print ( "Error: " + str(sys.exc_info()) )
            print ( traceback.format_exc() )
        # The following is a work around for Python 3 which no longer has raw_input!!!!
        try:
            # In pre-python 3, raw_input is defined
            input = raw_input
        except NameError:
            # In python 3, raw_input is NOT defined, but now has an "input" function to use instead
            pass
        s = input ( "Enter a parameter statement > " )


