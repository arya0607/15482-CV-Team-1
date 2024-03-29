from monitor import *
from terrabot_utils import clock_time, time_since_midnight

class LightMonitor(Monitor):
    ambient_data = []
    lighting_intervals = []
    insolation = 0 # Per hour
    target = 8500 # Default value

    def __init__(self, period=5):
        super(LightMonitor, self).__init__("LightMonitor", period)
        self.reset()

    def reset(self):
        self.insolation = 0
        # self.current_optimal = 900

    def setTarget(self, target):
        self.target = target

    def read_log_file(self, filename):
        self.ambient_data = []
        with open(filename) as log_file:
            for line in log_file:
                sline = line.split(" ")
                time = float(sline[0])
                data = float(sline[1].strip(' \n'))
                self.ambient_data.append((time, data))

    def activate(self):
        self.read_log_file("autograder_files/ambient.log")
        self.lightBehavior = self.executive.behavioral.getBehavior("LightBehavior")
        schedule = self.executive.schedule
        self.lighting_intervals = [(start*60, end*60)
                                   for start, end in schedule['LightBehavior']]
        self.current_optimal = 900 # Arbitrary value - will be reset once the monitor begins

    def perceive(self):
        # BEGIN STUDENT CODE
        print("HELLOWOOOWOW perceive should set sensor data")
        self.mtime = self.sensordata["midnight_time"]
        self.time = self.sensordata["unix_time"]
        self.light = self.sensordata["light"]
        print("time", self.mtime)
        print("light level", self.light)
        # print("led level", self.lightBehavior.led)
        # END STUDENT CODE

    def monitor(self):
        # print("INSOLATION: %.1f %d" %(self.mtime/3600.0, self.insolation))
        if (self.mtime < time_since_midnight(self.last_time)):
            print("INSOLATION TODAY: %.1f" %self.insolation)
            self.reset()
        else:
            # Calculate the optimal light level to reach the target value,
            #  given the amount of time the LightBehavior will be running and
            #  the amount of ambient light expected to be received when
            #  the LightBehavior is not running.  Set the optimal limits
            #  for the LightBehavior based on this calculation

            # BEGIN STUDENT CODE
            # add the ambient light and TerraBot light
            self.insolation += (self.light * self.dt) / 3600.0
            print("insolation HERE", self.insolation)
            ambient = self.non_lighting_ambient_insolation(self.mtime, 86399)
            #print(self.integrate_ambient(0, 86399))
            #assert(False)
            remaining_light = self.target - self.insolation - ambient
            time_left = self.lighting_time_left(self.mtime)
            
            # set optimal limit
            if time_left != 0:
            	self.current_optimal = (remaining_light  * 3600 / float(time_left))
            	self.executive.behavioral.getBehavior("LightBehavior").set_optimal(
            	    self.current_optimal)
            else:
            	print("time left is 0")
            # END STUDENT CODE
            

    def integrate_ambient(self, ts, te):
        ambient_insolation = 0
        t1, v1 = self.ambient_data[0]
        for index in range(1, len(self.ambient_data)):
            t2, v2 = self.ambient_data[index]
            if (ts < t2 and te > t1):
                if (ts > t1): # Starts within an interval
                    v1 = v1 + ((v2 - v1)*(ts - t1)/(t2 - t1))
                    t1 = ts
                if (te < t2): # Ends within an interval
                    v2 = v1 + ((v2 - v1)*(te - t1)/(t2 - t1))
                    t2 = te
                mval = (v1 + v2)/2.0
                ambient_insolation += mval*(t2 - t1)/3600.0
            t1, v1 = self.ambient_data[index]
        return ambient_insolation

    # Helper function:
    # How much ambient light will there be when LightBehavior is not running
    #  between start time (ts) and end time (te)
    def non_lighting_ambient_insolation(self, ts, te):
        ambient_light = 0
        t, t_last = (ts, 0)
        for interval in self.lighting_intervals:
            if (te <= interval[0]): break
            elif (t < interval[0]):
                t = max(t, t_last)
                ambient_light += self.integrate_ambient(t, min(te, interval[0]))
                t = interval[1]
            t_last = interval[1]

        if (te > t):
            ambient_light += self.integrate_ambient(t, te)
        #print("AMBIENT INSOLATION: (%d, %d) %.1f" %(ts/3600, te/3600, ambient_light))
        return ambient_light

    # Helper function:
    # How much time is left in the schedule for LightBehavior to run
    def lighting_time_left(self, time):
        time_left = 0
        for interval in self.lighting_intervals:
            if (interval[0] <= time and time < interval[1]):
                time_left = interval[1] - time
            elif (time < interval[0]):
                time_left += interval[1] - interval[0]

        return time_left

