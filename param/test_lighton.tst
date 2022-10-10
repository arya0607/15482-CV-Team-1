 # Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

#lights on between 9 am and 12 pm
WHENEVER 1-09:00:00
  ENSURE led UNTIL 1-12:00:00

#lights on between 13 am and 16 pm
WHENEVER 1-13:00:00
  ENSURE led UNTIL 1-16:00:00

#lights on between 17 am and 20 pm
WHENEVER 1-17:00:00
  ENSURE led UNTIL 1-20:00:00

#lights on between 21 am and 22 pm
WHENEVER 1-21:00:00
  ENSURE led UNTIL 1-22:00:00