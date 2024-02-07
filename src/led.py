import micropython
import utime

def led_setup():
     """! 
        Sets up the pin, timer, and channel to control the LED via pwm
        @returns ch1: the channel that the timer is using to send data to the pin
        """
    pinA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    tim2 = pyb.Timer(2, freq=20000)
    ch1 = tim2.channel(1, pyb.Timer.PWM_INVERTED, pin=pinA0)
    return ch1
    
    
def led_brightness(channel, brightness):
    """! 
        Changes the LED brightness based on the input channel and the brightness parameter
        @param channel: the channel that is sending the PWM signal from the timer to the pin
        @param brightness: the percentage brightness to set the LED to
        """
    channel.pulse_width_percent(brightness)
    
if __name__ == "__main__":
    # set up the led controller and store the channel
    channel = led_setup()
    # how long to ramp the led for in seconds
    ramp_time = 5
    # how long to wait before changing led to next percentage in ms
    wait_time = ramp_time*1000/100
    # infinite loop
    while True:
        # ramp up the  led
        for i in range(100):
            # i is the percentage to se the led to, pass it and the channel to change the brightness
            led_brightness(channel, i)
            # wait a bit
            utime.sleep_ms(int(wait_time))
        # ramping down, same process just backwards
        for i in reversed(range(100)):
            led_brightness(channel, i)
            utime.sleep_ms(int(wait_time))
            
            