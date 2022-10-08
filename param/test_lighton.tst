 # Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

#lights on between 8 am and 10 pm
WHENEVER 1-08:00:00
  ENSURE led UNTIL 1-22:00:00

QUIT AT 3-23:59:59 # Run the test and simulator for 3 days