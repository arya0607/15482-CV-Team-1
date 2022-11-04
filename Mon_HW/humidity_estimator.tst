BASELINE = high_humid_baseline.bsl
INTERFERENCE = broken_humidity.inf

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

# When the temperature is high, ensure that the fan turns on and stays on,
# unless the humidity is low enough
WHENEVER LowerHumidActive and (max(humidity[0], humidity[1]) > 90)
  #PRINT "HERE0: %s" %(humidity,)
  WAIT fan or (not LowerHumidActive) FOR 60 # Give fan a bit of time to turn on
  # The fans should stay on until the humidity is below optimal or 
  # the behavior is disabled
  WAIT (not LowerHumidActive) or (not fan and min(humidity[0], humidity[1]) <= 80) FOR 1800
  #PRINT "HERE1: %s %s" %(humidity, fan)

# Indicate all the times the LowerHumid behavior runs, 
#  starting at 7am, which is when the baseline file begins

WHENEVER 1-07:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-08:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-09:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-10:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-11:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-12:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-13:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-14:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-15:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-16:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-17:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-18:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-19:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-20:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-21:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-22:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False

WHENEVER 1-23:00:00
  SET LowerHumidActive = True
  WAIT FOR 1800
  SET LowerHumidActive = False


QUIT AT 1-23:59:59

