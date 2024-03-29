from hardware import *
import rospy
import sys, os
from std_msgs.msg import Float32, Int32, Int32MultiArray, Float32MultiArray, Bool, String
from terrabot_utils import time_since_midnight

#sensor data passed as a file
class ROSSensors(Sensors):

    light_level = 0
    temperature = 0
    humidity = 0
    weight = 0
    moisture = 0
    wlevel = 0
    light_level_raw = [0, 0]
    temperature_raw = [0, 0]
    humidity_raw = [0, 0]
    weight_raw = [0, 0]
    moisture_raw = [0, 0]
    wlevel_raw = 0

    def __init__(self):
        rospy.Subscriber('light_output', Int32MultiArray, self.light_callback)
        rospy.Subscriber('temp_output', Int32MultiArray, self.temp_callback)
        rospy.Subscriber('humid_output', Int32MultiArray, self.humid_callback)
        rospy.Subscriber('weight_output', Float32MultiArray, self.weight_callback)
        rospy.Subscriber('smoist_output', Int32MultiArray, self.moist_callback)
        rospy.Subscriber('level_output', Float32, self.level_callback)

    def getTime(self):
        return rospy.get_time()

    # Implement subscriber handlers here
    # BEGIN STUDENT CODE
    def light_callback(self, data):
    	ROSSensors.light_level_raw = data.data
    	ROSSensors.light_level = (data.data[0] + data.data[1]) / 2
    	return
    	
    def temp_callback(self, data):
    	ROSSensors.temperature_raw = data.data
    	ROSSensors.temperature = (data.data[0] + data.data[1]) / 2
    	return
    	
    def humid_callback(self, data):
    	ROSSensors.humidity_raw = data.data
    	ROSSensors.humidity = (data.data[0] + data.data[1]) / 2
    	return
    	
    def weight_callback(self, data):
    	ROSSensors.weight_raw = data.data
    	ROSSensors.weight = (data.data[0] + data.data[1]) / 2
    	return
    	
    def moist_callback(self, data):
    	ROSSensors.moisture_raw = data.data
    	ROSSensors.moisture = data.data
    	return
    	
    def level_callback(self, data):
    	ROSSensors.wlevel_raw = data.data
    	ROSSensors.wlevel = data.data
    # END STUDENT CODE

    def doSense(self):
        #update the dictionary to return your values
        return {"unix_time":rospy.get_time(),
                "midnight_time":time_since_midnight(rospy.get_time()),
                "light": self.light_level,
                "temp":self.temperature, "humid":self.humidity,
                "weight":self.weight,"smoist":self.moisture,
                "level":self.wlevel, "light_raw": self.light_level_raw,
                "temp_raw":self.temperature_raw, "humid_raw":self.humidity_raw,
                "weight_raw":self.weight_raw, "smoist_raw":self.moisture_raw,
                "level_raw":self.wlevel_raw}

#actuators commanded as a file
class ROSActuators(Actuators):

    actuators = {}
    actuator_state = {"fan":False, "wpump": False, "led": 0}

    def __init__(self):
        self.actuators['led'] = rospy.Publisher('led_input', Int32,
                                                latch=True, queue_size=1)
        self.actuators['fan'] = rospy.Publisher('fan_input', Bool,
                                                latch=True, queue_size=1)
        self.actuators['wpump'] = rospy.Publisher('wpump_input', Bool,
                                                  latch=True, queue_size=1)
        self.actuators['ping'] = rospy.Publisher('ping', Bool,
                                                  latch=True, queue_size=1)
        self.actuators['camera'] = rospy.Publisher('camera', String,
                                                  latch=True, queue_size=1)

    def doActions(self, actions_tuple):
        # Publish actuator commands here
        # BEGIN STUDENT CODE
        (behaviorName, time, act_dict) = actions_tuple
        for name in act_dict:
        	self.actuators[name].publish(act_dict[name])	# publish new commands
        	self.actuator_state[name] = act_dict[name]
        # END STUDENT CODE

if __name__ == '__main__':
    rospy.set_param('use_sim_time', True)
    rospy.init_node('test_ros_hardware_agent', anonymous = True)
    sensors = ROSSensors()
    actuators = ROSActuators()
    acts = {'fan' : False, 'wpump' : False, 'led' : 0}
    count = 0
    while not rospy.core.is_shutdown():
        if "-s" in sys.argv:
            print(sensors.doSense())
        if "-a" in sys.argv:
            acts["wpump"] = not acts["wpump"]
            if (count %2 == 0): acts["fan"] = not acts["fan"]
            if (count %3 == 0): acts["led"] = 200-acts["led"]
            actuators.doActions(('test', 0, acts))
            count += 1
        rospy.sleep(2)

