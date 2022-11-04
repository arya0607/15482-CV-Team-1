from monitor import *
from kalman import *

class HumidityEstimator(Monitor):

    def __init__(self, period=1):
        super(HumidityEstimator, self).__init__("HumidityEstimator", period)

    def activate(self):
        # BEGIN STUDENT CODE
        (mu0, var0) = self.sensors.humidity,2
        self.kf  = KalmanFilter(mu0,var0)
        self.current_state = dict()
        self.current_state.update(self.sensordata)
        self.current_state.update(self.actuators)
   
        # END STUDENT CODE
        pass

    def perceive(self):
        # BEGIN STUDENT CODE
        sensordata = self.sensordata


        # END STUDENT CODE
        pass
        
    def monitor(self):
        # BEGIN STUDENT CODE
        prevState = self.current_state
        #self.current_state = dict()
        #self.current_state.update(self.sensordata)
        #self.current_state.update(self.actuators)

        self.smoist = self.sensordata["smoist"]
        humidity0, humidity1 = self.smoist[0], self.smoist[1]
        now,prev_state = self.sensors.getTime(), prevState
        outlier_rejection = False
        self.kf.estimate(now, prev_state, humidity0, humidity1, outlier_rejection)
       
        self.executive.behavioral.getBehavior("lowerHumid").setHumidValue(self.kf.mu)

        # END STUDENT CODE
        pass

	

