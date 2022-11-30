from greenhouse_binary import Greenhouse_Binary
from monitor import *
from terrabot_utils import clock_time, time_since_midnight


class ActuatorMonitor(Monitor):

    def __init__(self, period=5):
        super(ActuatorMonitor, self).__init__("ActuatorMonitor", period)
        self.reset()

    def reset(self):
        self.minutes = 30
        self.behaviors_info = {}

        self.behaviors_info["Light"] = (10*60, (self.minutes, 4*60), 3*60)
        self.behaviors_info["LowerHumid"] = (8*60, (self.minutes, 60), 12*60)
        self.behaviors_info["LowerTemp"] = (2*60, (2*60, 4*60), 12*60)
        self.behaviors_info["RaiseTemp"] = (2*60, (2*60, 4*60), 12*60)
        self.behaviors_info["LowerSMoist"] = (2*60, (2*60, 4*60), 12*60)
        self.behaviors_info["RaiseSMoist"] = (2*60, (2*60, 4*60), 12*60)
        self.behaviors_info["Camera"] = (1*60, (3*60, 6*60), 0)

    def activate(self):
        self.LowerTempBehavior = self.executive.behavioral.getBehavior(
            "LowerTempBehavior")
        self.LowerHumidBehavior = self.executive.behavioral.getBehavior(
            "LowerHumidBehavior")

    def perceive(self):
        self.mtime = self.sensordata["midnight_time"]

    def monitor(self):
        # if we are past midnight, update a new schedule
        if (self.mtime < time_since_midnight(self.last_time)):
            # humid_blocks and lower_temp blocks give the total number of blocks
            # that each behavior was scheduled for, regardless if they actually
            # got activated in that block
            current_lower_humid_blocks = self.LowerHumidBehavior.LowerHumidEnableCount
            current_lower_temp_blocks = self.LowerTempBehavior.LowerTempEnableCount

            # activations give the actual amount of times a behavior actuator was
            # activated, and can be less than the number of blocks scheduled
            lower_humid_activations = self.LowerHumidBehavior.LowerHumidActivationCount
            lower_temp_activations = self.LowerTempBehavior.LowerTempActivationCount

            # update the time frame of LowerHumid
            (oldHumidTime, (_, _), _) = self.behaviors_info["LowerHumid"]
            # if we activated for less blocks than scheduled, decrease time
            if lower_humid_activations < current_lower_humid_blocks:
                newOldTime = max(0, oldHumidTime-60)
            # if we activated for all blocks of time, increase time
            else:
                newOldTime = min(12*60, oldHumidTime+60)
            # print("current_lower_humid_blocks: ", current_lower_humid_blocks)
            # print("lower_humid_activations: ", lower_humid_activations)
            # print("oldHumidTime: ", oldHumidTime)
            # print("newOldTime: ", newOldTime)
            self.behaviors_info["LowerHumid"] = (
                newOldTime, (self.minutes, 60), 12*60)

            # update the time frame of LowerTemp
            (oldTempTime, (_, _), _) = self.behaviors_info["LowerTemp"]
            # if we activated for less blocks than scheduled, decrease time
            if lower_temp_activations < current_lower_temp_blocks:
                newOldTime = max(0, oldTempTime-60)
            # if we activated for all blocks of time, increase time
            else:
                newOldTime = min(4*60, oldTempTime+60)
            # print("current_lower_temp_blocks: ", current_lower_temp_blocks)
            # print("lower_temp_activations: ", lower_temp_activations)
            # print("oldTempTime: ", oldTempTime)
            # print("newOldTime: ", newOldTime)
            self.behaviors_info["LowerTemp"] = (
                newOldTime, (2*60, 4*60), 12*60)
            # print("updating schedule")

            new_binary = Greenhouse_Binary(
                "greenhouse_schedule.txt", self.behaviors_info, self.minutes)
            sol = new_binary.solveProblem(visualize=False)
            # print(sol)

            self.LowerHumidBehavior.LowerHumidActivationCount = 0
            self.LowerHumidBehavior.LowerHumidEnableCount = 0
            self.LowerHumidBehavior.has_been_activated = False

            self.LowerTempBehavior.LowerTempActivationCount = 0
            self.LowerTempBehavior.LowerTempEnableCount = 0
            self.LowerTempBehavior.has_been_activated = False

            self.executive.setSchedule("greenhouse_schedule.txt")
            self.executive.requestNewSchedule()

            self.reset()
