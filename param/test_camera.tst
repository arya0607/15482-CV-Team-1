# GOAL: to test that the camera is taking photos according to the scheduler
# Should always pass the test, despite high OR low light levels to begin
BASELINE = high_everything_baseline.bsl

WHENEVER camera != None
  SET image = camera
  WAIT os.path.exists(image) FOR 30
  SET num_pics = num_pics + 1
  PRINT "A picture was taken"

# Ensures that pictures are being taken according to the scheduler
WHENEVER 1-09:30:00 # give 30 minutes buffer
  ENSURE num_pics >= 1

WHENEVER 1-13:30:00
  ENSURE num_pics >= 2

WHENEVER 1-17:30:00
  ENSURE num_pics >= 3

WHENEVER 1-00:00:00
  SET daily_pics = num_pics
  WAIT UNTIL 1-23:59:59
  SET dpic = num_pics - daily_pics
  ENSURE 1 <= dpic and dpic <= 3
