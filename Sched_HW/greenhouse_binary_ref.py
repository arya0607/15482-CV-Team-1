# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model
import visualize_solution as vs
import os,sys,ortools
import dill
import schedule as sched
grader_files = "grader_files/"

#Default is in here

if(os.path.isdir(os.path.join(grader_files, "-".join(sys.version.split(".")[:2])))):
    grader_files=os.path.join(grader_files, "-".join(sys.version.split(".")[:2]))

if(os.path.isdir(os.path.join(grader_files, "-".join(ortools.__version__.split(".")[:2])))):
    grader_files=os.path.join(grader_files,"-".join(ortools.__version__.split(".")[:2]))


class Greenhouse_Binary:

    # name is the name of the schedule to be written to
    # behaviors_info contains for each behavior, a tuple of
    #    0: the least cumulative amount of time in minutes that the behavior needs to be run
    #    1: the spacing between the behaviors in minutes (min, max) s.t. <= 1 run in min time and >= 1 in max time
    #       This is only used for some behaviors: ["LowerTemp","LowerHumid","LowerSMoist","Camera","RaiseTemp","RaiseSMoist"]
    #       and not for any other
    #    2: the maximum amount of time the behavior should run at night between [20,24) U [0,8)
    # minutes_per_chunk is the number of minutes that we break the day into

    def __init__(self, name, behaviors_info, minutes_per_chunk, print=True):
        f = open(grader_files+"/RefSol.pkl", "rb")
        self.GB = dill.load(f)
        f.close()
        self.GB.init(name, behaviors_info, minutes_per_chunk, print)

    # This is the function to call to test the problem being solved.
    # It takes the requirements from init and
    def solveProblem(self, visualize=False):
        return self.GB.solveProblem(visualize)
