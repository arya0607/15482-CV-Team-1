from monitor import *
from kalman import *

class HumidityEstimator(Monitor):

    def __init__(self, period=1):
        super(HumidityEstimator, self).__init__("HumidityEstimator", period)
        self.current_state = dict()

    def activate(self):
        # BEGIN STUDENT CODE
        (mu0, var0) = self.sensors.humidity,2
        self.kf  = KalmanFilter(mu0,var0)
        self.sensordata = self.sensors.doSense()
        self.previous_state = dict()
        self.previous_state.update(self.sensordata)
        self.previous_state.update(self.executive.behavioral.behaviors[0].actuators.actuator_state)
        self.previous_state["m_time"] = self.previous_state["midnight_time"]
	
	#i = [1,2]
	#l = i[9]
	        
        self.current_state = dict()
   
        # END STUDENT CODE
        pass

    def perceive(self):
        # BEGIN STUDENT CODE
        sensordata = self.sensordata
        actuators = self.executive.behavioral.behaviors[0].actuators.actuator_state
        self.current_state.update(actuators)
        self.current_state.update(sensordata)
        self.current_state["m_time"] = self.current_state["midnight_time"]
        # END STUDENT CODE
        pass
        
    def monitor(self):
        # BEGIN STUDENT CODE
        self.smoist = self.sensordata["smoist"]
        humidity0, humidity1 = self.smoist[0], self.smoist[1]
        now,prev_state = self.sensors.getTime(), self.previous_state
        outlier_rejection = False
        
        self.kf.estimate(now, prev_state, humidity0, humidity1, outlier_rejection)
       
        self.executive.behavioral.getBehavior("LowerHumidBehavior").setHumidValue(self.kf.mu)
        
        self.previous_state = self.current_state
        
        
        # END STUDENT CODE
        pass

	

