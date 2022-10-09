# GOAL: to test that the camera is taking photos according to the scheduler
# Should always pass the test, despite high OR low light levels to begin
BASELINE = high_light_baseline.bsl

WHENEVER camera != None # Testing that light level is between 400 and 600
  SET light_level = (light[0] + light[1) / 2
  ENSURE light_level >= 400 and light_level <= 600

WHENEVER camera != None
  SET image = camera
  WAIT os.path.exists(image) FOR 30
  SET num_pics = num_pics + 1

# Ensures that pictures are being taken according to the scheduler
WHENEVER 1-09:30:00 # give 30 minutes buffer
  ENSURE num_pics >= 1

WHENEVER 1-13:30:00
  ENSURE num_pics >= 2

WHENEVER 1-17:30:00
  ENSURE num_pics >= 3

WHENEVER 1-21:30:00
  ENSURE num_pics >= 4