from behavior import *
from limits import *
from transitions import Machine

#sensor data passed into greenhouse behaviors:
#  [time, lightlevel, temperature, humidity, soilmoisture, waterlevel]
#actuators are looking for a dictionary with any/all of these keywords:
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
        self.initial = 'off'
        self.states = [self.initial, 'on', 'light', 'dark']
        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)
        
        # Add FSM transitions and actions
        # BEGIN STUDENT CODE

        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'dark', 'light'], self.initial, after='setInitial')

        self.fsm.add_transition('doStep', ['on', 'dark', 'light'], 'light', conditions = ['shouldLightsOn'], after = 'turnLightsOn')
        self.fsm.add_transition('doStep', ['on', 'light'], 'dark', conditions = ['shouldBeDark'], after = 'setDark')


        # self.fsm.add_transition('doStep', [self.initial, 'dim'], 'bright', conditions = ['shouldBeBright'], after = 'setBright')
        # self.fsm.add_transition('doStep', [self.initial, 'bright'], 'dim', conditions = ['shouldBeDim'], after = 'setDim')
        # self.fsm.add_transition('doStep', ['bright', 'dim'], self.initial, conditions = ['shouldBeDark'], after = 'setDark')
        # END STUDENT CODE
        
    def setInitial(self):
        self.led = 0
        self.setLED(self.led)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")

    def disable(self):
        # Use 'disable' trigger to transition the FSM into the 'initial' state
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
       
    def shouldLightsOn(self):
        return 8 <= ((self.mtime//3600)%24) < 22
    def shouldBeDark(self):
        return not (8 <= ((self.mtime//3600)%24) < 22)        

    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def turnLightsOn(self):
        if self.light < self.optimal_level[0]:
            self.setLED(self.led + 20)
        elif self.light >= self.optimal_level[1]:
            self.setLED(self.led - 20)
    def setDark(self):
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
        self.initial = 'off'
        self.states = [self.initial, 'on', 'toolow', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'toolow', 'perfect'], self.initial, after='setInitial')
        
        self.fsm.add_transition('doStep', ['on', 'perfect'], 'toolow', conditions='isTooLow', after='setTooLow')
        self.fsm.add_transition('doStep', ['toolow'], 'perfect', conditions='isPerfect', after='setPerfect')
        # END STUDENT CODE

    def setInitial(self):
        self.setLED(0)
        
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def perceive(self):
        self.temp = self.sensordata["temp"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def isPerfect(self):
        return self.temp >= optimal['temperature'][0]
    def isTooLow(self):
        return self.temp < limits['temperature'][0]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def setPerfect(self):
        self.setLED(0)
    def setTooLow(self):
        self.setLED(200)
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
        self.initial = 'off'
        self.states = [self.initial, 'on', 'tooHigh', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'tooHigh', 'perfect'], self.initial, after='setInitial')
        
        self.fsm.add_transition('doStep', ['on', 'perfect'], 'tooHigh', conditions='isTooHigh', after='setTooHigh')
        self.fsm.add_transition('doStep', ['tooHigh'], 'perfect', conditions='isPerfect', after='setPerfect')

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        # END STUDENT CODE

    def setInitial(self):
        self.setFan(False)
        
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def perceive(self):
        self.temp = self.sensordata["temp"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def isPerfect(self):
        return self.temp <= optimal['temperature'][1]
    def isTooHigh(self):
        return self.temp >= limits['temperature'][1]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def setPerfect(self):
        self.setFan(False)
    def setTooHigh(self):
        self.setFan(True)
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

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'off'
        self.states = [self.initial, 'on', 'tooHigh', 'perfect']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'tooHigh', 'perfect'], self.initial, after='setInitial')
        
        self.fsm.add_transition('doStep', ['on', 'perfect'], 'tooHigh', conditions='isTooHigh', after='setTooHigh')
        self.fsm.add_transition('doStep', ['tooHigh'], 'perfect', conditions='isPerfect', after='setPerfect')

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        # END STUDENT CODE

    def setInitial(self):
        self.setFan(False)
        
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def perceive(self):
        self.humid = self.sensordata["humid"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def isPerfect(self):
        return self.humid <= optimal['humidity'][1]
    def isTooHigh(self):
        return self.humid >= limits['humidity'][1]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def setPerfect(self):
        self.setFan(False)
    def setTooHigh(self):
        self.setFan(True)
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
        self.last_time = 24*60*60 # Start with the prior day
        self.daily_limit = 100


        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'off'
        self.states = [self.initial, 'on', 'watering', 'stabilizing', 'done', 'soakingup', 'testing']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'watering', 'stabilizing', 'done', 'soakingup', 'testing'], self.initial, 
        after = ['setInitial', 'setLastTime'])
        
        self.fsm.add_transition('doStep', 'on', 'on', conditions = ['nextDay'], before='resetTotalWater')

        self.fsm.add_transition('doStep', ['on'], 'done', conditions = ['isWateredEnough'], unless=['nextDay'],
        before = 'printWateredEnough')

        self.fsm.add_transition('doStep', ['on'], 'watering', conditions = ['tooDry'], unless=['isWateredEnough', 'nextDay'], 
        after=['setPumpTrue', 'setWlevel', 'setTimer10', 'setInProgress'])

        self.fsm.add_transition('doStep', 'on', 'watering', conditions = ['inProgress'],  unless=['isWateredEnough', 'tooDry', 'nextDay'], 
        after=['setPumpTrue', 'setWlevel', 'setTimer10', 'printInProgress'])

        self.fsm.add_transition('doStep', 'watering', 'stabilizing', conditions = ['timeUp'], 
        after=['setPumpFalse', 'setTimer30'])

        self.fsm.add_transition('doStep', 'stabilizing', 'soakingup', conditions = ['timeUp'], 
        before=['calcTotalWater', 'setTimer300'])

        self.fsm.add_transition('doStep', 'soakingup', 'testing', conditions = ['timeUp'], 
        after=['printTesting'])

        self.fsm.add_transition('doStep', ['testing'], 'done', conditions = ['isWateredEnough'],
        before = 'printWateredEnough')

        self.fsm.add_transition('doStep', 'testing', 'done', conditions = ['moistEnough'], unless=['isWateredEnough'],
        after=['printMoistEnough', 'setNotInProgress'])

        self.fsm.add_transition('doStep', ['testing'], 'watering', conditions = ['tooDry'], unless=['isWateredEnough', 'moistEnough'],
        after=['setPumpTrue', 'setWlevel', 'setTimer10'])

        self.fsm.add_transition('doStep', 'testing', 'watering', conditions = ['inProgress'], unless=['isWateredEnough', 'moistEnough', 'tooDry'],
        after=['setPumpTrue', 'setWlevel', 'setTimer10', 'printInProgress'])
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        # self.fsm.add_transition('doStep', '', '', conditions = [''], after='')
        print('moisture: ', optimal['moisture'][0])
        print('water daily', self.daily_limit)
        print('tooDry', limits['moisture'][0])
    
        # END STUDENT CODE
    def p():
        print('wassup')
    def setInitial(self):
        self.setPumpFalse()
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def sliding_window(self, window, item, length=4):
        if (len(window) == length): window = window[1:]
        window.append(item)
        return window, sum(window)/float(len(window))
    
    def perceive(self):
        self.smoist = self.sensordata["smoist"]
        self.time = self.sensordata["unix_time"]
        self.mtime = self.sensordata["midnight_time"]
        self.wlevel = self.sensordata["level"]
        self.wlevel_window, self.wlevel_est = self.sliding_window(self.wlevel_window, self.wlevel)
        self.smoist0_window, self.smoist0_est = self.sliding_window(self.smoist0_window, self.smoist[0])
        self.smoist1_window, self.smoist1_est = self.sliding_window(self.smoist1_window, self.smoist[1])

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def nextDay(self):
        return self.last_time > self.mtime
    def isWateredEnough(self):
        return self.total_water >= self.daily_limit
    def moistEnough(self):
        return self.smoist1_est >= optimal['moisture'][0]
    def tooDry(self):
        return self.smoist0_est < limits['moisture'][0]
    def timeUp(self):
        return self.time >= self.waittime 
    def inProgress(self):
        return self.in_progress
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE

    def setTimer(self, wait):
        self.waittime = self.time + wait
        print("setTimer: %d (%d)" %(self.waittime, wait))
    def setTimer10(self): self.setTimer(10)
    def setTimer30(self): self.setTimer(30)
    def setTimer300(self): self.setTimer(300)
    def setWlevel(self):
        print("Set water level: %d" %self.wlevel_est)
        self.waterlevel = self.wlevel_est
    def setLastTime(self): self.last_time = self.mtime
    def resetTotalWater(self): # Reset total water each day
        print("Resetting total water")
        self.total_water = 0
        self.setLastTime()

    def setInProgress(self): self.in_progress = True
    def setNotInProgress(self): self.in_progress = False

    def calcTotalWater(self):
        dwater = (self.waterlevel - self.wlevel_est)*(100/4.5)
        self.total_water += dwater
        print("calcTotalWater: %.1f (%.1f)" %(self.total_water, dwater))
        
    def printWateredEnough(self): print("Watered Enough: %.1f" %self.total_water)
    def printMoistEnough(self): print("Moist Enough: %.1f" %self.smoist1_est)
    def printInProgress(self): print("In progress: %.1f" %self.smoist1_est)
    def printTesting(self): print("Testing")
    def setPumpTrue(self): self.setPump(True)
    def setPumpFalse(self): self.setPump(False)
    def setPump(self,state): self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"wpump": state}))

    # END STUDENT CODE

"""
Soil moisture below the upper limit
"""
class LowerSMoist(Behavior):

    def __init__(self):
        super(LowerSMoist, self).__init__("LowerMoistBehavior")


        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'initial'
        self.states = [self.initial, 'tooMoist', 'perfect', 'on']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', self.initial, 'on', after='setInitial')
        self.fsm.add_transition('disable', ['on', 'perfect', 'tooMoist'], self.initial, 
        after = ['setInitial'])
        
        self.fsm.add_transition('doStep', ['on', 'perfect'], 'tooMoist', conditions = ['isTooMoist'], after='setFanTrue')
        self.fsm.add_transition('doStep', ['tooMoist'], 'perfect', conditions = ['isPerfect'], after='setFanFalse')


        # END STUDENT CODE
        
    def setInitial(self):
        self.setFan(False)
        
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def perceive(self):
        self.smoist = self.sensordata["smoist"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE

    def isTooMoist(self):
        return self.smoist[1] >= limits["moisture"][1]
    def isPerfect(self):
        return self.smoist[1] <= optimal['moisture'][1]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    # END STUDENT CODE
    def setFanTrue(self):
        self.setFan(True)
    def setFanFalse(self):
        self.setFan(False)
    def setFan(self, act_state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"fan": act_state}))

