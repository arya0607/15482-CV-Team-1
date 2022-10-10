# GOAL: Test that the fan is working
# The fan is turned on when temp is too high, when humid is too high, and when
# moisture is too high
# This test will check for temperature and humidity
# It should always pass

BASELINE = high_everything_baseline.bsl

WHENEVER temperature >= 29  # When the temperature is too high
    WAIT fan FOR 60
    ENSURE fan

WHENEVER temperature <= 27  # When the temperature has lowered enough
    WAIT not fan FOR 60
    ENSURE not fan

WHENEVER humidity >= 90 # When the humidity is too high
    WAIT fan FOR 60
    ENSURE fan

WHENEVER humidity <= 80 # When the humidity has lowered enough
    WAIT not fan FOR 60
    ENSURE not fan