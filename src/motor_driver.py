import pyb
import utime
import micropython

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer, ch1,ch2):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety.
        @param en_pin: enabling pin for the motor
        @param in1pin: where the PWM is being sent for 1
        @param in2pin: where the PWM is being sent for 2
        @param timer: timer that the motor uses for the PWM
        @param ch1: where the timer is being channeled to send to pin1
        @param ch2: where the timer is being channeled to send to pin2
        """
        print ("Creating a motor driver")
        #defining parameters needed to characterize motor
        self.en_pin = en_pin 
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer
        self.en_pin.low() #disable the motor (for safety)
        self.ch1 = ch1
        self.ch2 = ch2

    
        
    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        #setting the duty cycle
        try:
            level = float(level)
            if -100 <=level <0: #for negative in range
                print (f"Setting duty cycle to {level}")
                print('negative in range') #debugging
                self.en_pin.high() #enable the motor
                self.ch2.pulse_width_percent(0) #set in2 to zero
                self.ch1.pulse_width_percent(abs(level)) #set in1 to pwm
            elif 0< level <=100: #for positive in range
                print (f"Setting duty cycle to {level}")
                print('positive in range') #debugging
                self.en_pin.high() #enable the motor
                self.ch1.pulse_width_percent(0) #set in2 to zero
                self.ch2.pulse_width_percent(abs(level)) #set in1 to pwm
            elif level == 0:
                print (f"Setting duty cycle to {level}")
                self.ch1.pulse_width_percent(0)
                self.ch2.pulse_width_percent(0)
                self.en_pin.low() #disable the motor
            else:
                print('invalid level value')
        except:
            print('invalid level value')
        
if __name__ == "__main__":
    #power the motor for five seconds 
    en_pin =  pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value=1)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3, freq=5000) #setting frequency for motor 
    ch1 = timer.channel(1, pyb.Timer.PWM, pin=in1pin) #setting in1 for PWM
    ch2 = timer.channel(2, pyb.Timer.PWM, pin=in2pin) #setting in2 for PWM
    motor = MotorDriver(en_pin,in1pin,in2pin,timer,ch1,ch2) #call to the motor class you just made!
    motor.set_duty_cycle(50) #set duty cycle, in range -100 to 100 (not including 0)
    utime.sleep(5)
    motor.set_duty_cycle(0)
    


