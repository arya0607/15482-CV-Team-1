import numpy as np
import pickle
import math
linreg = None

def regression(now, state):
    global linreg
    if (linreg == None):
        linreg = pickle.load(open("autograder_files/model_humid_linreg.pkl", 'rb'))

    # Features are humid, future_time, led, pump, fan
    features = [state['humid'], now - state['m_time'],
                state['led'], state['wpump'], state['fan']]
    return linreg.predict(np.array([features]))[0]

class KalmanFilter():
    mu = 0
    var = 1

    def __init__(self, mu0, var0):
        self.mu = mu0
        self.var = var0
        
    def __str__(self): return "[KF: %.2f %.2f]" %(self.mu, self.var)

    def predict(self, prediction, process_var):
        # BEGIN STUDENT CODE
        tempMu = self.mu
        alpha = prediction/tempMu
        self.mu = prediction
        self.var = (alpha**2)*self.var + process_var
        # END STUDENT CODE

    def update(self, obs, obs_var):
        # BEGIN STUDENT CODE
        k = self.var*((self.var + obs_var)**(-1))
        self.mu = self.mu + k*(obs - self.mu)
        self.var = (1-k)*self.var
        # END STUDENT CODE

    def estimate(self, now, prev_state, humidity0, humidity1,
                 outlier_rejection=False):
        # BEGIN STUDENT CODE
        if outlier_rejection == False:
        	prediction = regression(now, prev_state)
        	self.predict(prediction, 1)
        	self.update(humidity0, 4)
        	self.update(humidity1, 4)
        else:
        	prediction = regression(now, prev_state)
        	self.predict(prediction, 1)
        	
        	stddev0 = abs(self.mu - humidity0)/math.sqrt(self.var)
        	if stddev0 < 2:
        		self.update(humidity0, 4)
        	stddev1 = abs(self.mu - humidity1)/math.sqrt(self.var)
        	if stddev1 < 2:
        		self.update(humidity1, 4)
        		
        # END STUDENT CODE
        
