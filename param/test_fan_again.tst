# GOAL: Test that the fan is working
# The fan is turned on when temp is too high, when humid is too high, and when
# moisture is too high
# This test will check for moisture
# It should always pass

BASELINE = high_everything_baseline.bsl

WHENEVER smoist >= 650
    WAIT fan FOR 60 # Give some time for the fan to turn on
    ENSURE fan

WHENEVER smoist <= 600
    WAIT not fan FOR 60
    ENSURE not fan