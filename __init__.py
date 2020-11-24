from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import RPi.GPIO as GPIO

#GPIO Pins
LED = 27

class LightSwitchSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(LED, GPIO.OUT)
        except GPIO.error:
            self.log.warning("Can't initialize GPIO - skill will not load")
            self.speak_dialog("error.initialise")
            
        my_setting = self.settings.get('my_setting')

    @intent_handler(IntentBuilder('TurnLightOnIntent').require('TurnLightOnKeyword'))
    def handle_turn_light_on_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        GPIO.output(LED, GPIO.HIGH)
        self.log.info("Light turned on")
        self.speak_dialog("light.on")
        
    @intent_handler(IntentBuilder('TurnLightOffIntent').require('TurnLightOffKeyword'))
    def handle_turn_light_off_intent(self, message):
        """ Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        GPIO.output(LED, GPIO.LOW)
        self.log.info("Light turned off")
        self.speak_dialog("light.off")

    @intent_handler('SwitchLights.intent')
    def handle_switch_lights_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        if GPIO.input(LED):
            GPIO.output(LED,GPIO.LOW)
            self.speak_dialog("light.off")
        else:
            GPIO.output(LED,GPIO.HIGH)
            self.speak_dialog("light.on")
            
    def stop(self):
        pass


def create_skill():
    return LightSwitchSkill()
