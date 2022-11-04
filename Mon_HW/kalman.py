import numpy as np
import pickle

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
        # END STUDENT CODE
        pass

    def update(self, obs, obs_var):
        # BEGIN STUDENT CODE
        # END STUDENT CODE
        pass

    def estimate(self, now, prev_state, humidity0, humidity1,
                 outlier_rejection=False):
        # BEGIN STUDENT CODE
        # END STUDENT CODE
        pass 
