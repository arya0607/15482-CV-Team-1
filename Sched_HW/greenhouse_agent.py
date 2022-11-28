import rospy
import ros_hardware
import layers
import sys
import os
from terrabot_utils import time_since_midnight

import greenhouse_behaviors as gb
import ping_behavior as ping
import camera_behavior as camera_behavior
import light_monitor as light_monitor
import humidity_estimator as hm


class BehavioralGreenhouseAgent:

    def __init__(self, sim):
        if sim:
            rospy.set_param('use_sim_time', True)
        rospy.init_node('greenhouseagent_behavioral', anonymous=True)

        # Initialize ROSSensors, ROSActuators, BehavioralLayer, and behaviors
        # BEGIN STUDENT CODE
        sensors = ros_hardware.ROSSensors()
        actuators = ros_hardware.ROSActuators()
        behaviors = [gb.Light(), gb.RaiseTemp(), gb.LowerTemp(
        ), gb.LowerHumid(), gb.RaiseSMoist(), gb.LowerSMoist(), ping.Ping()]
        self.behavioral = layers.BehavioralLayer(sensors, actuators, behaviors)
        self.behavioral.startAll()
        # added after
        # self.executiveLayer.setMonitors(sensors, [light_monitor.Light_Monitor])
        # END STUDENT CODE

    def main(self):
        rospy.sleep(2)
        while rospy.get_time() == 0:
            rospy.sleep(1)
        while not rospy.core.is_shutdown():
            # Run a step of the behavioral architecture
            self.behavioral.doStep()
            rospy.sleep(1)


class LayeredGreenhouseAgent:

    def __init__(self, sim, schedulefile):
        if sim:
            rospy.set_param('use_sim_time', True)
        rospy.init_node('greenhouseagent_layered', anonymous=True)

        # Initialize the architecture
        # BEGIN STUDENT CODE
        sensors = ros_hardware.ROSSensors()
        actuators = ros_hardware.ROSActuators()
        behaviors = [gb.Light(), gb.RaiseTemp(), gb.LowerTemp(
        ), gb.LowerHumid(), gb.RaiseSMoist(), gb.LowerSMoist(), ping.Ping(), camera_behavior.TakeImage()]
        self.behavioral = layers.BehavioralLayer(sensors, actuators, behaviors)
        self.planning = layers.PlanningLayer(schedulefile)

        self.executive = layers.ExecutiveLayer()
        self.planning.setExecutive(self.executive)
        self.executive.setPlanningLayer(self.planning)
        self.executive.setBehavioralLayer(self.behavioral)
        self.executive.setSchedule(schedulefile)
        self.planning.getNewSchedule()
        # END STUDENT CODE
        # added after
        #self.executive.setMonitors(sensors, [hm.HumidityEstimator()])
        self.executive.setMonitors(sensors, [light_monitor.LightMonitor(), hm.HumidityEstimator()])
    def main(self):
        rospy.sleep(2)
        while rospy.get_time() == 0:
            rospy.sleep(1)
        while not rospy.core.is_shutdown():
            t = time_since_midnight(rospy.get_time())
            # Run a step of each layer of the architecture
            # BEGIN STUDENT CODE
            self.behavioral.doStep()
            self.planning.doStep(t)
            self.executive.doStep(t)
            print("main testing")
            # END STUDENT CODE
            rospy.sleep(1)


if __name__ == '__main__':
    sim = False
    if "-m" in sys.argv and "sim" in sys.argv:
        sim = True
    if "-B" in sys.argv:
        print("Starting Behavioral Agent")
        agent = BehavioralGreenhouseAgent(sim)
        agent.main()
    elif "-L" in sys.argv:
        print("Starting Layered Agent")
        agent = LayeredGreenhouseAgent(sim, "greenhouse_schedule.txt")
        agent.main()
