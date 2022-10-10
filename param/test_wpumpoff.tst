# GOAL: to test that pump is off according to scheduler
# Wait a bit before starting, to give agent a chance to initialize
DELAY FOR 600

#pump off between 9 am and 12:30 pm
WHENEVER 1-09:00:00
  ENSURE not wpump UNTIL 1-12:30:00

#pump off between 13 am and 16:30 pm
WHENEVER 1-13:00:00
  ENSURE not wpump UNTIL 1-16:30:00

#pump off between 17 am and 20:30 pm
WHENEVER 1-17:00:00
  ENSURE not wpump UNTIL 1-20:30:00