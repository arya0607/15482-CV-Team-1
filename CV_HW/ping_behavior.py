from behavior import *
from transitions import Machine

'''
The behavior should ping once every 2-3 minutes
'''


class Ping(Behavior):

    def __init__(self):
        super(Ping, self).__init__("PingBehavior")
        self.initial = 'halt'
        # STUDENT CODE: Modify these lines to add all your FSM states
        self.states = [self.initial, 'init']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(
            trigger='doStep', source='init', dest='init', conditions=['update_ping'], after='ping')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def setInitial(self):
        self.last_ping = -10000

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.time = self.sensordata["unix_time"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger('doStep')

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def update_ping(self):
        return self.time - self.last_ping >= 120
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def ping(self):
        self.actuators.doActions((self.name, self.time, {"ping": True}))
        self.last_ping = self.time
    # END STUDENT CODE

    def ping(self):
        self.actuators.doActions((self.name, self.time, {"ping": True}))
        self.last_ping = self.time
