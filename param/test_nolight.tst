 # Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

#lights off between 12 am and 13 pm
WHENEVER 1-12:00:00
  ENSURE not led UNTIL 1-13:00:00

#lights on between 16 am and 17 pm
WHENEVER 1-16:00:00
  ENSURE not led UNTIL 1-17:00:00

#lights on between 20 am and 21 pm
WHENEVER 1-20:00:00
  ENSURE led UNTIL 1-21:00:00