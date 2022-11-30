from behavior import *
from limits import *
from transitions import Machine

# sensor data passed into greenhouse behaviors:
#  [time, lightlevel, temperature, humidity, soilmoisture, waterlevel]
# actuators are looking for a dictionary with any/all of these keywords:
#  {"led":val, "fan":True/False, "pump": True/False}


'''
The combined ambient and LED light level between 8am and 10pm should be 
in the optimal['light_level'] range;
Between 10pm and 8am, the LEDs should be off (set to 0).
'''


class Light(Behavior):

    def __init__(self):
        super(Light, self).__init__("LightBehavior")
        self.optimal_level = optimal['light_level']

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'light', 'dark']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transition
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')

        self.fsm.add_transition(trigger='doStep', source='init', dest='light', conditions=[
                                "light_on"], after="increase_light")
        self.fsm.add_transition(trigger='doStep', source='init', dest='dark', conditions=[
                                "light_off"], after="turn_off_light")
        self.fsm.add_transition(trigger='disable', source='light', dest='halt')
        self.fsm.add_transition(trigger='disable', source='dark', dest='halt')

        self.fsm.add_transition(trigger='doStep', source='light', dest='dark', conditions=[
                                "light_off"], after="turn_off_light")

        self.fsm.add_transition(trigger='doStep', source='dark', dest='light', conditions=[
                                "light_on", "should_increase_light"], after="increase_light")
        self.fsm.add_transition(
            trigger='doStep', source='dark', dest='light', conditions=["light_on"])
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', conditions=[
                                "light_on", "should_increase_light"], after="increase_light")
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', conditions=[
                                "light_on", "should_decrease_light"], after="decrease_light")
        self.fsm.add_transition(
            trigger='doStep', source='light', dest='light', conditions=["light_on"])

        # END STUDENT CODE

    def setInitial(self):
        self.led = 0
        self.setLED(self.led)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.mtime = self.sensordata["midnight_time"]
        self.time = self.sensordata["unix_time"]
        self.light = self.sensordata["light"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE

    def light_on(self):
        # true if not between 10pm and 8am
        hour = (self.mtime//3600) % 24
        return hour >= 8 and hour < 22

    def light_off(self):

        # true if between 10pm and 8am
        hour = (self.mtime//3600) % 24
        return not (hour >= 8 and hour < 22)

    def should_increase_light(self):
        return self.light < self.optimal_level[0]

    def should_decrease_light(self):
        return self.light >= self.optimal_level[1]

    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE

    def increase_light(self):
        self.setLED(self.led+20)

    def decrease_light(self):
        self.setLED(self.led-20)

    def turn_off_light(self):
        self.setLED(0)
    # END STUDENT CODE

    def setLED(self, level):
        self.led = max(0, min(255, level))
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"led": self.led}))


"""
The temperature should be greater than the lower limit
"""


class RaiseTemp(Behavior):

    def __init__(self):
        super(RaiseTemp, self).__init__("RaiseTempBehavior")

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'toolow', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(trigger='doStep', source='init', dest='toolow', conditions=[
                                "temp_toolow"], after="raise_temp")
        self.fsm.add_transition(trigger='doStep', source='init', dest='perfect', conditions=[
                                "temp_perfect"], after="off_temp")
        self.fsm.add_transition(trigger='doStep', source='toolow', dest='perfect', conditions=[
                                "temp_perfect"], after="off_temp")
        self.fsm.add_transition(trigger='doStep', source='perfect', dest='toolow', conditions=[
                                "temp_toolow"], after="raise_temp")
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def setInitial(self):
        self.setLED(0)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.temp = self.sensordata["temp"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def temp_toolow(self):
        return self.temp < limits['temperature'][0]

    def temp_perfect(self):
        return self.temp >= optimal['temperature'][0]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def raise_temp(self):
        self.setLED(200)

    def off_temp(self):
        self.setLED(0)
    # END STUDENT CODE

    def setLED(self, level):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"led": level}))


"""
The temperature should be less than the upper limit
"""


class LowerTemp(Behavior):

    def __init__(self):
        super(LowerTemp, self).__init__("LowerTempBehavior")

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.LowerTempActivationCount = 0
        self.LowerTempEnableCount = 0
        self.has_been_activated = False
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'toohigh', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(trigger='doStep', source='init', dest='toohigh', conditions=[
                                "temp_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='doStep', source='toohigh', dest='perfect', conditions=[
                                "temp_perfect"], after="fan_off")
        self.fsm.add_transition(trigger='doStep', source='perfect', dest='toohigh', conditions=[
                                "temp_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def setInitial(self):
        self.setFan(False)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.LowerTempEnableCount += 1
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.temp = self.sensordata["temp"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def temp_toohigh(self):
        return self.temp >= limits['temperature'][1]

    def temp_perfect(self):
        return self.temp <= optimal['temperature'][1]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def fan_on(self):
        if not self.has_been_activated:
            self.LowerTempActivationCount += 1
            self.has_been_activated == True
        self.setFan(True)

    def fan_off(self):
        self.setFan(False)
    # END STUDENT CODE

    def setFan(self, act_state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"fan": act_state}))


"""
Humidity should be less than the limit
"""


class LowerHumid(Behavior):

    def __init__(self):
        super(LowerHumid, self).__init__("LowerHumidBehavior")
        self.LowerHumidActivationCount = 0
        self.LowerHumidEnableCount = 0
        self.has_been_activated = False

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'toohumid', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(trigger='doStep', source='init', dest='toohumid', conditions=[
                                "humid_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='doStep', source='toohumid', dest='perfect', conditions=[
                                "humid_perfect"], after="fan_off")
        self.fsm.add_transition(trigger='doStep', source='perfect', dest='toohumid', conditions=[
                                "humid_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def setInitial(self):
        self.setFan(False)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.LowerHumidEnableCount += 1
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        if self.humidEstimate == None:
            self.humid = self.sensordata["humid"]
        else:
            self.humid = self.humidEstimate
        #self.humid = self.sensordata["humid"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    def setHumidValue(self, update):
        self.humidEstimate = update

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def humid_toohigh(self):
        return self.humid >= limits['humidity'][1]

    def humid_perfect(self):
        return self.humid <= optimal['humidity'][1]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def fan_on(self):
        if not self.has_been_activated:
            Behavior.LowerHumidActivationCount += 1
            self.has_been_activated == True
        self.setFan(True)

    def fan_off(self):
        self.setFan(False)
    # END STUDENT CODE

    def setFan(self, act_state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"fan": act_state}))


"""
Soil moisture should be greater than the lower limit
"""


class RaiseSMoist(Behavior):

    def __init__(self):
        super(RaiseSMoist, self).__init__("RaiseMoistBehavior")
        self.wlevel_est = 0
        self.wlevel_window = []
        self.smoist0_est = 0
        self.smoist0_window = []
        self.smoist1_est = 0
        self.smoist1_window = []
        self.total_water = 0
        self.waterlevel = 0
        self.in_progress = False
        self.last_time = 24*60*60  # Start with the prior day
        self.daily_limit = 100

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'done',
                       'watering', 'stabilizing', 'soakingup', 'testing']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')

        self.fsm.add_transition(trigger='doStep', source='init', dest='init', conditions=[
                                'next_day'], after=['reset_total_water'])
        self.fsm.add_transition(trigger='doStep', source='init', dest='done', conditions=[
                                'watered_enough'], after=['print_watered_enough'])
        self.fsm.add_transition(trigger='doStep', source='init', dest='watering', conditions=[
                                'soil_too_dry'], after=['set_pump_true', 'set_water_level', 'set_timer_10', 'set_in_progress'])
        self.fsm.add_transition(trigger='doStep', source='init', dest='watering', conditions=[
                                'is_in_progress'], after=['set_pump_true', 'print_in_progress', 'set_water_level', 'set_timer_10'])

        self.fsm.add_transition(trigger='doStep', source='watering', dest='stabilizing', conditions=[
                                'time_is_up'], after=['set_pump_false', 'set_timer_30'])

        self.fsm.add_transition(trigger='doStep', source='stabilizing', dest='soakingup', conditions=[
                                'time_is_up'], after=['calc_total_water', 'set_timer_300'])

        self.fsm.add_transition(trigger='doStep', source='soakingup', dest='testing', conditions=[
                                'time_is_up'], after=['print_testing'])

        self.fsm.add_transition(trigger='doStep', source='testing', dest='done', conditions=[
                                'watered_enough'], after=['print_watered_enough'])
        self.fsm.add_transition(trigger='doStep', source='testing', dest='done', conditions=[
                                'moist_enough'], after=['print_moist_enough', 'set_not_in_progress'])
        self.fsm.add_transition(trigger='doStep', source='testing', dest='watering', conditions=[
                                'too_dry_still'], after=['set_pump_true', 'set_water_level', 'set_timer_10'])
        self.fsm.add_transition(trigger='doStep', source='testing', dest='watering', conditions=[
                                'is_in_progress'], after=['set_pump_true', 'print_in_progress', 'set_water_level', 'set_timer_10'])

        # END STUDENT CODE

    def setInitial(self):
        self.set_pump_false()
        pass

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.set_pump_false()
        self.set_last_time()
        self.trigger("disable")

    def sliding_window(self, window, item, length=4):
        if (len(window) == length):
            window = window[1:]
        window.append(item)
        return window, sum(window)/float(len(window))

    def perceive(self):
        self.smoist = self.sensordata["smoist"]
        self.time = self.sensordata["unix_time"]
        self.mtime = self.sensordata["midnight_time"]
        self.wlevel = self.sensordata["level"]
        self.wlevel_window, self.wlevel_est = self.sliding_window(
            self.wlevel_window, self.wlevel)
        self.smoist0_window, self.smoist0_est = self.sliding_window(
            self.smoist0_window, self.smoist[0])
        self.smoist1_window, self.smoist1_est = self.sliding_window(
            self.smoist1_window, self.smoist[1])

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def next_day(self):
        return self.last_time > self.mtime

    def watered_enough(self):
        return self.total_water >= self.daily_limit

    def soil_too_dry(self):
        return self.smoist0_est < limits['moisture'][0]

    def is_in_progress(self):
        return self.in_progress

    def time_is_up(self):
        return self.time >= self.waittime

    def moist_enough(self):
        return self.smoist1_est >= optimal['moisture'][0]

    def too_dry_still(self):
        return self.smoist0_est < limits['moisture'][0]

    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE

    def set_timer(self, wait):
        self.waittime = self.time + wait
        print("setTimer: %d (%d)" % (self.waittime, wait))

    def set_timer_10(self): self.set_timer(10)
    def set_timer_30(self): self.set_timer(30)
    def set_timer_300(self): self.set_timer(300)

    def set_water_level(self):
        print("Set water level: %d" % self.wlevel_est)
        self.waterlevel = self.wlevel_est

    def set_last_time(self): self.last_time = self.mtime

    def reset_total_water(self):  # Reset total water each day
        print("Resetting total water")
        self.total_water = 0
        self.set_last_time()

    def set_in_progress(self): self.in_progress = True
    def set_not_in_progress(self): self.in_progress = False

    def calc_total_water(self):
        dwater = (self.waterlevel - self.wlevel_est)*(100/4.5)
        self.total_water += dwater
        print("calcTotalWater: %.1f (%.1f)" % (self.total_water, dwater))

    def print_watered_enough(self): print(
        "Watered Enough: %.1f" % self.total_water)

    def print_moist_enough(self): print(
        "Moist Enough: %.1f" % self.smoist1_est)

    def print_in_progress(self): print("In progress: %.1f" % self.smoist1_est)
    def print_testing(self): print("Testing")

    def set_pump_false(self):
        self.setPump(False)

    def set_pump_true(self):
        self.setPump(True)

    # END STUDENT CODE

    def setPump(self, state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"wpump": state}))


"""
Soil moisture below the upper limit
"""


class LowerSMoist(Behavior):

    def __init__(self):
        super(LowerSMoist, self).__init__("LowerMoistBehavior")

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, 'init', 'toomoist', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(trigger='doStep', source='init', dest='toomoist', conditions=[
                                "moist_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='doStep', source='toomoist', dest='perfect', conditions=[
                                "moist_perfect"], after="fan_off")
        self.fsm.add_transition(trigger='doStep', source='perfect', dest='toomoist', conditions=[
                                "moist_toohigh"], after="fan_on")
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def setInitial(self):
        self.setFan(False)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.smoist = self.sensordata["smoist"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def moist_toohigh(self):
        return self.smoist[1] >= limits['moisture'][1]

    def moist_perfect(self):
        return self.smoist[1] <= optimal['moisture'][1]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def fan_on(self):
        self.setFan(True)

    def fan_off(self):
        self.setFan(False)
    # END STUDENT CODE
    #

    def setFan(self, act_state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"fan": act_state}))
