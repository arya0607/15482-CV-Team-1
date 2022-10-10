# GOAL: test pinging
# Since pings should be every 2-3 minutes, this test waits 3 minutes
# for a ping to occur. Then it resets the ping and waits for the next one.

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

WHENEVER True
  # Wait 3 minutes for a ping (pings should be every 2-3 minutes)
  WAIT ping FOR 360

# Reset the ping and wait until the next one
WHENEVER ping
  WAIT not ping FOR 10 # Don't want the current ping to confuse things
  ENSURE not ping FOR 120  # Not another ping for the next 2 minutes