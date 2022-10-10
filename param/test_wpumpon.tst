# GOAL: to test that pump is on according to scheduler
# Wait a bit before starting, to give agent a chance to initialize
DELAY FOR 600

# Create an environment that is cold and dry
BASELINE = cold_and_dry.bsl

#pump on between 8:30 am and 9 am
WHENEVER 1-08:30:00
  ENSURE smoist[0] < 601  #making sure not overwatering
  WHENEVER smoist[0] > 650 #make sure the pump doesn't turn on if the moisture level is high
    WAIT not wpump FOR 360
  ENSURE wpump UNTIL 1-09:00:00

#pump on between 12:30 pm and 13 pm
WHENEVER 1-12:30:00
  ENSURE smoist[0] < 601  #making sure not overwatering
  WHENEVER smoist[0] > 650 #make sure the pump doesn't turn on if the moisture level is high
    WAIT not wpump FOR 360
  ENSURE wpump UNTIL 1-13:00:00

#pump on between 16:30 pm and 17 pm
WHENEVER 1-16:30:00
  ENSURE smoist[0] < 601  #making sure not overwatering
  WHENEVER smoist[0] > 650 #make sure the pump doesn't turn on if the moisture level is high
    WAIT not wpump FOR 360
  ENSURE wpump UNTIL 1-17:00:00

#pump on between 20:30 pm and 21 pm
WHENEVER 1-20:30:00
  ENSURE smoist[0] < 601  #making sure not overwatering
  WHENEVER smoist[0] > 650 #make sure the pump doesn't turn on if the moisture level is high
    WAIT not wpump FOR 360
  ENSURE wpump UNTIL 1-21:00:00