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
        self.initial = 'initial'
        self.states = [self.initial]
        # BEGIN SANITIZE ALL
        self.initial = 'Halt'
        self.states = [self.initial,"Init","Lighting","Dark"]
        # END SANITIZE ALL

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition('enable', 'Halt', 'Init', after='printTime')
        self.fsm.add_transition('disable', ['Init','Lighting','Dark'], 'Halt')
        self.fsm.add_transition('doStep', 'Init', 'Lighting',
                                conditions=['daytime'], after='adjustUpLED')
        self.fsm.add_transition('doStep', 'Init', 'Dark', unless=['daytime'])
        self.fsm.add_transition('doStep', 'Dark', 'Lighting',
                                conditions=['daytime'], after='adjustUpLED')
        self.fsm.add_transition('doStep', 'Lighting', 'Dark', unless=['daytime'])
        self.fsm.add_transition('doStep', 'Lighting', '=',
                                conditions=['tooBright'], after=['adjustDownLED'])
        self.fsm.add_transition('doStep', 'Lighting', '=',
                                conditions=['tooDark'], after=['adjustUpLED'])
        self.fsm.on_enter_Dark('setInitial')
        self.fsm.on_enter_Init('setInitial')
        self.fsm.on_enter_Halt('setInitial')
        self.mtime=0
        # END STUDENT CODE
        
    def setInitial(self):
        self.led = 0
        self.setLED(self.led)

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
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
    def daytime(self):
        hour = (self.mtime//3600)%24
        return hour >= 8 and hour < 22
        
    def tooDark(self):
        print("optimal level 0", self.optimal_level[0])
        return self.light < self.optimal_level[0]
    
    def tooBright(self):
        return self.light >= self.optimal_level[1]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    # Use this to test that self.mtime can be accessed when behavior is enabled
    def printTime(self):
        print("Time after midnight: %s" %self.mtime)

    def adjustUpLED(self):
        print("Adjust Light Up")
        self.setLED(self.led+20)
        
    def adjustDownLED(self):
        #print("Adjust Light Down")
        self.setLED(self.led-20)
    # END STUDENT CODE

    def setLED(self, level):
        self.led = max(0, min(255, level))
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"led": self.led}))

# function that edits the optimal level
    def set_optimal(self, level):
    	print("levels", self.optimal_level[0], self.optimal_level[1])
    	print("OPTIMAL LEVEL", level)
    	self.optimal_level = [level - 10, level + 10]
    	# self.optimal_level[0] = level - 20
    	# self.optimal_level[1] = level + 20




#class Light(Behavior):

#    def __init__(self):
#        super(Light, self).__init__("LightBehavior")
#        self.optimal_level = optimal['light_level']

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
#        self.initial = 'halt'
#        self.states = [self.initial, "off", "on"]

#        self.fsm = Machine(self, states=self.states, initial=self.initial,
#                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        
#        self.fsm.add_transition("enable", self.initial, "on",
#        after="setInitial")
 #       self.fsm.add_transition("disable", "off", self.initial)
        
#        self.fsm.add_transition("disable", "on", self.initial,
 #       after="set_off")

        
        # self.fsm.add_transition("doStep", "off", "on",
        # conditions=["at_8am", "light_low"], after="set_led_high")
        # self.fsm.add_transition("doStep", "off", "on",
        # conditions=["at_8am", "light_high"], after="set_led_low")
        # self.fsm.add_transition("doStep", "off", "on",
        # conditions=["at_8am"])
        # self.fsm.add_transition("doStep", "on", "off",
        # conditions=["at_10pm"], after="set_off")
#        self.fsm.add_transition("doStep", "on", "on",
#        conditions=["light_low"], after="set_led_high")
#        self.fsm.add_transition("doStep", "on", "on",
#        conditions=["light_high"], after="set_led_low")
		
        # END STUDENT CODE
        
#    def setInitial(self):
        # print("initializing")
 #       self.led = 0
#        self.setLED(self.led)

#    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
#        self.trigger("enable")

 #   def disable(self):
        # Use 'disable' trigger to transition the FSM into the 'initial' state
  #      self.trigger("disable") 
        
   # def perceive(self):
    #    self.mtime = self.sensordata["midnight_time"]
     #   self.time = self.sensordata["unix_time"]
      #  self.light = self.sensordata["light"]
        # print("perceiving", self.light, self.led)
    
#    def act(self):
        # Use 'doStep' trigger for all other transitions
 #       self.trigger("doStep")
        
    # Add all your condition functions here
    # BEGIN STUDENT CODE
 #   def at_0(self):
    	# print("led level", self.led)
  #  	return self.led == 0
    
  #  def at_8am(self):
    	# print("8am", self.mtime, self.mtime >= 28800 and self.mtime < 79200)
   # 	return self.mtime >= 28800 and self.mtime < 79200 # 8am in seconds
    	
    #def at_10pm(self):
    	# print("10pm", self.mtime, self.mtime >= 79200)
    #	return self.mtime >= 79200 # 10pm in seconds
    	
    #def light_low(self):
  #  	print("light low", self.light < self.optimal_level[0])
    #	return self.light < self.optimal_level[0]
    	
#    def light_high(self):
 #   	return self.light >= self.optimal_level[1]
    	
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
   # def set_led_high(self):
    	# print("setting led higher")
    #	self.setLED(self.led+20)
    	# print("set_led_high", self.led, (self.mtime // 3600)%24)
    	
  #  def set_led_low(self):
   # 	self.setLED(self.led-20)
    	# print("set_led_low", self.led, (self.mtime // 3600)%24)
    	
  #  def set_off(self):
   # 	self.setLED(0)
    	# print("set_off", self.led, (self.mtime // 3600)%24)
    	
    # END STUDENT CODE

 #   def setLED(self, level):
  #      self.led = max(0, min(255, level))
   #     print("LED:",self.led)
    #    self.actuators.doActions((self.name, self.sensors.getTime(),
     #                             {"led": self.led}))
                            
                                  

"""
The temperature should be greater than the lower limit
"""
class RaiseTemp(Behavior):

    def __init__(self):
        super(RaiseTemp, self).__init__("RaiseTempBehavior")

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, "off", "low", "good"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        
        self.fsm.add_transition("enable", self.initial, "off", after="setInitial")
        self.fsm.add_transition("disable", "off", self.initial, after="set_off")
        self.fsm.add_transition("disable", "low", self.initial, after="set_off")
        self.fsm.add_transition("disable", "good", self.initial, after="set_off")
        
        self.fsm.add_transition("doStep", "off", "low",
        conditions=["temp_low"], after="set_led_high")
        self.fsm.add_transition("doStep", "low", "good",
        conditions=["temp_good"], after="set_off")
        self.fsm.add_transition("doStep", "good", "low",
        conditions=["temp_low"], after="set_led_high")
        # END STUDENT CODE

    def setInitial(self):
        self.setLED(0)
        
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.trigger("enable")
        
    def disable(self):
        # Use 'disable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")
        
    def perceive(self):
        self.temp = self.sensordata["temp"]

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger("doStep")

    # Add all your condition functions here
    # BEGIN STUDENT CODE
    def temp_low(self):
    	return self.temp < limits['temperature'][0]
    	
    def temp_good(self):
    	return self.temp >= optimal['temperature'][0]
    # END STUDENT CODE

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def set_led_high(self):
    	self.setLED(200)
    	
    def set_off(self):
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
        self.initial = 'halt'
        self.states = [self.initial, "off", "high", "good"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition("enable", self.initial, "off", after="setInitial")
        self.fsm.add_transition("disable", "off", self.initial, after="set_off")
        self.fsm.add_transition("disable", "high", self.initial, after="set_off")
        self.fsm.add_transition("disable", "good", self.initial, after="set_off")
        
        self.fsm.add_transition("doStep", "off", "high",
        conditions=["temp_high"], after="set_fan_on")
        self.fsm.add_transition("doStep", "high", "good",
        conditions=["temp_low"], after="set_off")
        self.fsm.add_transition("doStep", "good", "high",
        conditions=["temp_high"], after="set_fan_on")
        
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
    def temp_high(self):
    	return self.temp >= limits['temperature'][1]
    	
    def temp_low(self):
    	return self.temp <= optimal['temperature'][1]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def set_fan_on(self):
    	self.setFan(True)
    	
    def set_off(self):
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

        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, "off", "humid", "good"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition("enable", self.initial, "off", after="setInitial")
        self.fsm.add_transition("disable", "off", self.initial, after="set_off")
        self.fsm.add_transition("disable", "humid", self.initial, after="set_off")
        self.fsm.add_transition("disable", "good", self.initial, after="set_off")
        
        self.fsm.add_transition("doStep", "off", "humid",
        conditions=["humid_high"], after="set_on")
        self.fsm.add_transition("doStep", "humid", "good",
        conditions=["humid_low"], after="set_off")
        self.fsm.add_transition("doStep", "good", "humid",
        conditions=["humid_high"], after="set_on")
        
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
    def humid_high(self):
    	return self.humid >= limits["humidity"][1]
    	
    def humid_low(self):
    	return self.humid <= optimal['humidity'][1]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def set_on(self):
    	self.setFan(True)
    
    def set_off(self):
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
        self.last_time = 24*60*60 # Start with the prior day
        self.daily_limit = 100
        


        # STUDENT CODE: Modify these lines to use your own initial state name
        #               and add all your FSM states
        self.initial = 'halt'
        self.states = [self.initial, "off", "watering", "stabilizing", "soaking",
        "testing", "done"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition("enable", self.initial, "off", after="setInitial")
        self.fsm.add_transition("disable", "off", self.initial, after="end")
        self.fsm.add_transition("disable", "watering", self.initial, after="end")
        self.fsm.add_transition("disable", "stabilizing", self.initial, 
        after="end")
        self.fsm.add_transition("disable", "soaking", self.initial, after="end")
        self.fsm.add_transition("disable", "testing", self.initial, after="end")
        self.fsm.add_transition("disable", "done", self.initial, after="end")
        
        self.fsm.add_transition("doStep", "off", "off", 
        conditions=["is_next_day"], after="reset_water")
        self.fsm.add_transition("doStep", "off", "done", 
        conditions=["watered_enough"], after="print_water")
        self.fsm.add_transition("doStep", "off", "watering", 
        conditions=["soil_dry"], after="set_watering1")
        self.fsm.add_transition("doStep", "off", "watering", 
        conditions=["in_progress"], after="set_progress")
        
        self.fsm.add_transition("doStep", "watering", "stabilizing", 
        conditions=["time_up"], after="set_stable")
        self.fsm.add_transition("doStep", "stabilizing", "soaking", 
        conditions=["time_up"], after="set_soak")
        
        self.fsm.add_transition("doStep", "soaking", "testing", 
        conditions=["time_up"], after="set_testing")
        self.fsm.add_transition("doStep", "testing", "done", 
        conditions=["watered_enough"], after="print_water")
        self.fsm.add_transition("doStep", "testing", "done", 
        conditions=["moist_enough"], after="print_moist")
        self.fsm.add_transition("doStep", "testing", "watering", 
        conditions=["soil_dry"], after="set_watering2")
        self.fsm.add_transition("doStep", "testing", "watering", 
        conditions=["in_progress"], after="set_progress")
        
        
        
        # END STUDENT CODE

    def setInitial(self):
        self.setPump(False)  

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
    def is_next_day(self):
    	return self.last_time > self.mtime
    	
    def watered_enough(self):
    	return self.total_water >= self.daily_limit
    	
    def soil_dry(self):
    	return self.smoist0_est < limits['moisture'][0]
    	
    def in_progress(self):
    	return self.in_progress
    	
    def time_up(self):
    	return self.time >= self.waittime
    	
    def moist_enough(self):
    	return self.smoist1_est >= optimal['moisture'][0]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def end(self):
    	self.setPump(False)
    	self.setLastTime()  
    
    def reset_water(self):
    	self.resetTotalWater()
    	
    def print_water(self):
    	self.printWateredEnough()
    	
    def set_watering1(self):
    	self.setPump(True)
    	self.setWlevel()
    	self.setTimer10()
    	self.setInProgress()
    	
    def set_progress(self):
    	self.setPump(True)
    	self.printInProgress()
    	self.setWlevel()
    	self.setTimer10()
    	
    def set_stable(self):
    	self.setPump(False)
    	self.setTimer30()
    	
    def set_soak(self):
    	self.calcTotalWater()
    	self.setTimer300()
    
    def set_testing(self):
    	self.printTesting()
    	
    def print_moist(self):
    	self.printMoistEnough()
    	self.setNotInProgress()
    	
    def set_watering2(self):
    	self.state = "watering"
    	self.setPump(True)
    	self.setWlevel()
    	self.setTimer10()
    
    # END STUDENT CODE

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

    def setPump(self,state):
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
        self.initial = 'initial'
        self.states = [self.initial, "off", "moist", "good"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition("enable", self.initial, "off", after="setInitial")
        self.fsm.add_transition("disable", "off", self.initial, after="set_off")
        self.fsm.add_transition("disable", "moist", self.initial, after="set_off")
        self.fsm.add_transition("disable", "good", self.initial, after="set_off")
        
        self.fsm.add_transition("doStep", "off", "moist",
        conditions=["moist_high"], after="set_on")
        self.fsm.add_transition("doStep", "moist", "good",
        conditions=["moist_low"], after="set_off")
        self.fsm.add_transition("doStep", "good", "moist",
        conditions=["moist_high"], after="set_on")
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
    def moist_high(self):
    	return self.smoist[1] >= limits["moisture"][1]
    	
    def moist_low(self):
    	return self.smoist[1] <= optimal['moisture'][1]
    # END STUDENT CODE
        
    # Add all your before / after action functions here
    # BEGIN STUDENT CODE
    def set_on(self):
    	self.setFan(True)
    	
    def set_off(self):
    	self.setFan(False)
    # END STUDENT CODE
            
    def setFan(self, act_state):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"fan": act_state}))

