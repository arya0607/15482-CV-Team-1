from behavior import *
from transitions import Machine
from vision import classifyFoliage, measureHeight
import sys
import os.path as op

# Nathan: This line was here when I found it VVV , probably need to uncomment if converting to absolute path
# sys.path.append(op.dirname(op.dirname(op.abspath(__file__)))+"/../lib/")

from terrabot_utils import clock_time
import cv2

'''
The behavior should adjust the lights to a reasonable level (say 400-600),
wait a bit for the light to stabilize, and then request an image.
It should check to be sure the image has been recorded and, if so, process
the image; if not, try again for up to 3 times before giving up
'''


class TakeImage(Behavior):
    def __init__(self):
        super(TakeImage, self).__init__("TakeImageBehavior")
        # Your code here
        # Initialize the FSM and add transitions
        # BEGIN STUDENT CODE
        ### SEE FSM IMAGE IN REPO TO SEE THE STATE TRANSITIONS ###
        self.pathname = ""  # pathname to image, initially empty, filled once an image is taken

        self.initial = 'halt'
        self.lastState = self.initial
        self.states = [self.initial, 'init', 'light',
                       'firstcheck', "secondcheck", "thirdcheck"]

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)
        # END STUDENT CODE

        ### TRANSITIONS ###
        # TODO: Clarify whether we are to use an enable/disable, or just use doStep.
        #  Even though starter file did not come with enable disable functions.
        #  Layers.py seems to use Behavior.enable for all behaviors, so
        #  current implementation assumes we are to use enable/disable,

        self.fsm.add_transition(trigger='enable', source='halt', dest='init')

        self.fsm.add_transition(trigger='doStep', source='init', dest='light')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')

        # Transitions from Light
        self.fsm.add_transition(trigger='doStep', source='light', dest='firstcheck', conditions=[
                                "light_perfect"], after=["take_picture", "set_timer_10"])
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', conditions=[
                                "should_decrease_light"], after=["decrease_light"])
        self.fsm.add_transition(trigger='doStep', source='light', dest='light', conditions=[
                                "should_increase_light"], after=["increase_light"])

        # Transitions from First Check
        self.fsm.add_transition(trigger='doStep', source='firstcheck', dest='halt', conditions=[
                                "time_is_up", "pic_exists"], after=["process_image", "turn_off_light"])
        self.fsm.add_transition(trigger='doStep', source='firstcheck', dest='secondcheck', conditions=[
                                "time_is_up", "no_pic_exists"], after=["take_picture", "set_timer_20"])

        # Transitions from Second Check
        self.fsm.add_transition(trigger='doStep', source='secondcheck', dest='halt', conditions=[
                                "time_is_up", "pic_exists"], after=["process_image", "turn_off_light"])
        self.fsm.add_transition(trigger='doStep', source='secondcheck', dest='thirdcheck', conditions=[
                                "time_is_up", "no_pic_exists"], after=["take_picture", "set_timer_20"])

        # Transitions from Third Check
        self.fsm.add_transition(trigger='doStep', source='thirdcheck', dest='halt', conditions=[
                                "time_is_up", "pic_exists"], after=["process_image", "turn_off_light"])
        self.fsm.add_transition(trigger='doStep', source='thirdcheck', dest='halt', conditions=[
                                "time_is_up", "no_pic_exists"], after=["print_warning", "turn_off_light"])

    # Add the condition and action functions
    #  Remember: if statements only in the condition functions;
    #            modify state information only in the action functions
    # BEGIN STUDENT CODE

    ### CONDITIONS ###

    def light_perfect(self):
        return 450 <= self.light < 550

    def should_increase_light(self):
        return self.light < 450

    def should_decrease_light(self):
        return self.light >= 550

    def time_is_up(self):
        return self.time >= self.waittime

    def pic_exists(self):
        return op.exists(self.pathname)

    def no_pic_exists(self):
        return not op.exists(self.pathname)

    ### ACTION FUNCTIONS ###

    def increase_light(self):
        self.setLED(self.led+20)

    def decrease_light(self):
        self.setLED(self.led-20)

    # TODO: Should we turn off light when we halt, how does this affect other behaviors??
    def turn_off_light(self):
        self.setLED(0)

    # action wrapper to take picture
    def take_picture(self):
        # relative pathname from TerraBot.py, TODO: might want to make absolute in the future
        self.pathname = "agents/CV_HW/greenhouse_images/" + str(self.time)
        self.takePicture(self.pathname)

    def print_warning(self):
        print("WARNING: Image Capture Failed")

    # action wrapper to process image
    def process_image(self):
        self.process_image(self.pathname)

    def set_timer(self, wait):
        self.waittime = self.time + wait
        print("setTimer: %d (%d)" % (self.waittime, wait))

    def set_timer_10(self): self.set_timer(10)
    def set_timer_20(self): self.set_timer(20)

    # END STUDENT CODE

    # Added, not originally in starter file
    def setInitial(self):
        self.led = 0
        self.setLED(self.led)

    # Added, not originally in starter file
    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        self.setInitial()
        self.trigger("enable")

    # Added, not originally in starter file
    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.setInitial()
        self.trigger("disable")

    def perceive(self):
        self.time = self.sensordata['unix_time']
        # Add any sensor data variables you need for the behavior
        # BEGIN STUDENT CODE
        self.light = self.sensordata["light"]
        # END STUDENT CODE

    def act(self):
        self.trigger("doStep")
        if (self.lastState != self.state):
            print("Transitioning to %s" % self.state)
            self.lastState = self.state

    def takePicture(self, path_name):
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"camera": path_name}))

    def setLED(self, level):
        self.led = max(0, min(255, level))
        self.actuators.doActions((self.name, self.sensors.getTime(),
                                  {"led": self.led}))

    def processImage(self, image):
        foliage_mask = classifyFoliage(image)
        size = image.shape[0]*image.shape[1]
        percentage = cv2.countNonZero(foliage_mask)/size
        height = measureHeight(foliage_mask)
        print("As of %s, %.1f%% of pixels are foliage; plant height is %.1fcm"
              % (clock_time(self.time), 100*percentage,
                 (0 if not height else height)))
