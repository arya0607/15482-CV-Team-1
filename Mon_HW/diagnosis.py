from cnf import *
from ortools.sat.python import cp_model

objects = ['Outlet', 'Rasp-Pi', 'Power-Board',
           'Arduino', 'Sensor-Board0', 'Sensor-Board1']
actuators = ['Fans', 'LEDs', 'Pump']
sensors = ['H-T0', 'Light0', 'Moisture0', 'H-T1', 'Light1', 'Moisture1',
           'Wlevel']
relations = ['working', 'connected', 'powered', 'signal', 'expected-result']

def powered(comp): return 'powered(%s)' %comp
def working(comp): return 'working(%s)' %comp
def connected(from_comp, to_comp):
    return 'connected(%s, %s)' %(from_comp, to_comp)
def signal(signal, component): return 'signal(%s, %s)' %(signal, component)
def rasp_pi_signal(the_signal): return signal(the_signal, 'Rasp-Pi')
def expected_result(actuator): return 'expected-result(%s)' %actuator

def create_relation(name, model, variables):
    variables[name] = model.NewBoolVar(name)

def create_relations(relations, model, variables):
    for relation in relations: create_relation(relation, model, variables)

def create_working_relations(model, variables):
    create_relations([working(comp) for comp in objects + actuators + sensors],
                     model, variables)

def create_connected_relations(model, variables):
    # BEGIN STUDENT CODE
    create_relations([connected(sensor, objects[-2]) for sensor in sensors[:3]], model, variables)
    create_relations([connected(sensor, objects[-1]) for sensor in sensors[3:6]], model, variables)
    create_relation(connected(sensors[-1], objects[3]), model, variables)
    create_relation(connected(objects[0], objects[2]), model, variables)
    create_relation(connected(objects[0], objects[1]), model, variables)
    create_relation(connected(objects[1], objects[3]), model, variables)
    create_relation(connected(objects[3], objects[1]), model, variables)

    create_relation(connected(objects[2], actuators[0]), model, variables)
    create_relation(connected(objects[2], actuators[1]), model, variables)
    create_relation(connected(objects[2], actuators[2]), model, variables)

    create_relation(connected(objects[3], objects[2]), model, variables)
    
    create_relation(connected(objects[-2], objects[-3]), model, variables)
    create_relation(connected(objects[-1], objects[-3]), model, variables)

    # 17

    # END STUDENT CODE
    pass

def create_powered_relations(model, variables):
    # BEGIN STUDENT CODE
    create_relations([powered(act) for act in objects[:3] + actuators], model, variables)
    # END STUDENT CODE

def create_signal_relations(model, variables):
    # BEGIN STUDENT CODE
    create_relations([signal(sens, sens) for sens in sensors], model, variables) # generates
    create_relations([signal(sensor, objects[-2]) for sensor in sensors[:3]], model, variables)
    create_relations([signal(sensor, objects[-1]) for sensor in sensors[3:6]], model, variables)
    create_relations([signal(sens, objects[3]) for sens in sensors], model, variables)
    create_relations([signal(sens, objects[1]) for sens in sensors], model, variables)
    create_relations([signal(act, objects[1]) for act in actuators], model, variables) # generates
    create_relations([signal(act, objects[3]) for act in actuators], model, variables)
    create_relations([signal(act, objects[2]) for act in actuators], model, variables)
    

    # END STUDENT CODE
    pass

def create_expected_result_relations(model, variables):
    # BEGIN STUDENT CODE
    create_relations([expected_result(act) for act in actuators], model, variables)
    # END STUDENT CODE

def create_relation_variables(model):
    variables = {}
    create_working_relations(model, variables)
    create_connected_relations(model, variables)
    create_powered_relations(model, variables)
    create_signal_relations(model, variables)
    create_expected_result_relations(model, variables)
    return variables

def add_constraint_to_model(constraint, model, variables):
    for disj in (eval(constraint) if isinstance(constraint, str) else constraint):
        for lit in disj:
            # print('89', lit)
            if is_negated(lit) and not lit[1] in variables:
                print('91 here', lit)
            elif not is_negated(lit) and not lit in variables:
                print('93 here', lit)
        conv_disj = [variables[lit] if not is_negated(lit) else
                     variables[lit[1]].Not() for lit in disj]
        model.AddBoolOr(conv_disj)

def create_powered_constraint(from_comp, to_comp, model, variables):
    constraint = "IFF('%s', AND('%s', '%s'))" %(powered(to_comp),
                                                connected(from_comp, to_comp),
                                                working(from_comp))
    add_constraint_to_model(constraint, model, variables)

def create_powered_actuator_constraint(actuator, model, variables):
    constraint = ("IFF('%s', AND('%s', AND('%s', AND('%s', '%s'))))"
                  %(powered(actuator), connected('Power-Board', actuator),
                    powered('Power-Board'), working('Power-Board'),
                    signal(actuator, 'Power-Board')))
    print(constraint)
    add_constraint_to_model(constraint, model, variables)

def create_powered_constraints(model, variables):
    add_constraint_to_model(LIT(powered('Outlet')), model, variables)
    create_powered_constraint('Outlet', 'Rasp-Pi', model, variables)
    create_powered_constraint('Outlet', 'Power-Board', model, variables)
    for actuator in actuators:
        create_powered_actuator_constraint(actuator, model, variables)

def create_signal_constraint(sensors, to_comp, from_comp, model, variables):
    for sensor in sensors:
        x = sensor if from_comp is None else from_comp
        constraint = (f"IFF('{signal(sensor, to_comp)}', AND('{connected(x, to_comp)}', AND('{working(x)}', '{signal(sensor, x)}')))"  )
        print('122', constraint)
        add_constraint_to_model(constraint, model, variables)

def create_signal_actuator_constraint(actuators, to_comp, from_comp, model, variables):
    for act in actuators:
        constraint = (f"IFF('{signal(act, to_comp)}', AND('{connected(from_comp, to_comp)}', AND('{working(from_comp)}', '{signal(act, from_comp)}')))"  )
        print('129', constraint)
        add_constraint_to_model(constraint, model, variables)

#[0 - 'Outlet', 1 - 'Rasp-Pi', 2 - 'Power-Board',
 #   3 - 'Arduino', -2 - 'Sensor-Board0', -1 - 'Sensor-Board1']
def create_signal_constraints(model, variables):
    # BEGIN STUDENT CODE
    create_signal_constraint(sensors[:3], objects[-2], None, model, variables)
    create_signal_constraint(sensors[3:6], objects[-1], None, model, variables)

    create_signal_constraint(sensors[:3], objects[3], objects[-2], model, variables)
    create_signal_constraint(sensors[3:6], objects[3], objects[-1], model, variables)

    create_signal_constraint(sensors[-1:], objects[3], None, model, variables)

    create_signal_constraint(sensors, objects[1], objects[3], model, variables)

    create_signal_actuator_constraint(actuators, objects[3], objects[1], model, variables)
    print('141')
    create_signal_actuator_constraint(actuators, objects[2], objects[3], model, variables)
    # END STUDENT CODE
    pass

def create_sensor_generation_constraints(model, variables):
    # BEGIN STUDENT CODE
    for sensor in sensors:
        constraint = (f"IFF('{signal(sensor, sensor)}', '{working(sensor)}')"  )
        add_constraint_to_model(constraint, model, variables)
    # END STUDENT CODE
    pass

def create_expected_result_constraints(model, variables):
    # BEGIN STUDENT CODE
    mapping = {'Fans' : ['H-T0', 'H-T1'], 'LEDs' : ['Light0', 'Light1'], 'Pump' : ['Moisture0', 'Moisture1', 'Wlevel']}
    for act in actuators:
        constraint = (f"IFF('{expected_result(act)}', AND( OR('{signal(mapping[act][0], 'Rasp-Pi')}', OR('{signal(mapping[act][1], 'Rasp-Pi')}', '{signal(mapping[act][-1], 'Rasp-Pi')}')) , AND( '{powered(act)}', '{working(act)}')))")
        add_constraint_to_model(constraint, model, variables)
    # END STUDENT CODE
    pass

def create_constraints(model, variables):
    create_powered_constraints(model, variables)
    create_signal_constraints(model, variables)
    create_sensor_generation_constraints(model, variables)
    create_expected_result_constraints(model, variables)

def create_greenhouse_model():
    model = cp_model.CpModel()
    variables = create_relation_variables(model)
    create_constraints(model, variables)
    return (model, variables)
    
def collect_diagnosis(solver, variables):
    return set([var for var in variables
                if ((var.startswith('connected') or var.startswith('working')) and
                    solver.BooleanValue(variables[var]) == False)])

class DiagnosesCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        # BEGIN STUDENT CODE
        self.__variables = variables
        self.__solution_count = 0
        self.solutions = []
        # END STUDENT CODE

    def OnSolutionCallback(self):
        # Extract the connected and working relations that are False
        # BEGIN STUDENT CODE
        self.__solution_count += 1
        l = []
        for v in self.__variables:
            # print('204')
            vx = self.__variables[v]
            val = self.BooleanValue(vx)
            # print('%s=%i' % (v, val))
            if val == False:
                l.append((v, val))
        self.solutions.append(l)
        # print()
        # END STUDENT CODE
        pass

    def getSolutions(self):
        return self.solutions
        

def diagnose(observations):
    model, variables = create_greenhouse_model()
    add_constraint_to_model(observations, model, variables)
    print(220)
    collector = DiagnosesCollector(variables)
    diagnoses = []
    solver = cp_model.CpSolver()
    solver.SearchForAllSolutions(model, collector)
    # Remove all redundant diagnoses (those that are supersets
    #   of other diagnoses).
    # BEGIN STUDENT CODE
    sol = collector.getSolutions()
    for assigns in sol:
        s = set()
        for val in assigns:
            name = val[0]
            if 'working' in name or 'connected' in name:
                s.add(name)
        diagnoses.append(s)
    # END STUDENT CODE
    new = []
    for d in diagnoses:
        check = True
        for p in diagnoses:
            if d is not p and p.issubset(d):
                check = False
                break
        if check:
            new.append(d)

    sorted(new, key=len)
    return new
