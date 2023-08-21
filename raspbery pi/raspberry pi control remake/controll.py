import machine
from picozero import pico_temp_sensor, pico_led

#===============================================================================================================================

class rgb_strip:
    def __init__(self, pinR, pinG, pinB):
        #- RGB values
        self.vals = {"R": 0, "G": 0, "B": 0}
        #- RGB pin setup
        
        def pwm_pin_setup(pin:int, freq:int) -> machine.PWM:
            """makes a PWM pin

            Args:
                pin (int): what pin to use
                freq (int): frequency in wanted

            Returns:
                machine.PWM: a pwm object
            """
            pwm = machine.PWM(machine.Pin(pin)) # type: ignore
            pwm.freq(freq)
            return pwm

        stripR = pwm_pin_setup(pinR, 1000)
        stripG = pwm_pin_setup(pinG, 1000)
        stripB = pwm_pin_setup(pinB, 1000)
        self.pins = {"R": stripR, "G": stripG, "B": stripB}


    def update_rgb(self,R,G,B):
        print("updateing strip")
        print(R,G,B)
        print("updating R")
        self.update_pin(R, "R")
        print("updating G")
        self.update_pin(G, "G")
        print("updating B")
        self.update_pin(B, "B")

    def update_pin(self, val, name):
        print("updating pin")
        print("updating val")
        self.vals[name] = val
        print("updated val:"+str(self.vals[name]))
        print("updating pwm")
        self.pins[name].duty_u16(self.vals[name]*500)
        print("updated pwm")


#===============================================================================================================================


class led:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.state = False

    def on(self):
        self.pin.on()
        self.state = True

    def off(self):
        self.pin.off()
        self.state = False

    def toggle(self):
        self.pin.toggle() # type: ignore
        self.state = not self.state


#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

strip1 = rgb_strip(19, 17, 20)
strip2 = rgb_strip(18, 16, 21)

pwrLed = led(15)
connectLed = led(14)

#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

def update_rgb(stripStates):
    """updates the rgb values of the specified strip
    Args:
        request (request_handler): the handled request object
    Returns:
        Nan: returns nothing
    """
    try:
        if stripStates["strip_id"] == 1:
            print("updating strip 1")
            strip1.update_rgb(stripStates["value"]["R"], stripStates["value"]["G"], stripStates["value"]["B"])
            return {"strip_id" : 1, "vals" : {"R" : strip1.vals["R"], "G" : strip1.vals["G"], "B" : strip1.vals["B"]}}, 200
        elif stripStates["strip_id"] == 2:
            strip2.update_rgb(stripStates["value"]["R"], stripStates["value"]["G"], stripStates["value"]["B"])
            return {"strip_id" : 2, "vals" : {"R" : strip2.vals["R"], "G" : strip2.vals["G"], "B" : strip2.vals["B"]}}, 200
        else:
            return {"error": "invalid strip id"}, 400
    except:
        return {"error": "error occurred"}, 500
#===============================================================================================================================

def toggle_led(led):
    print("toggling led")
    if led == "pwr":
        print("toggleing pwr led")
        pwrLed.toggle()
        print("toggled pwr led")
    elif led == "connect":
        print("toggleing connect led")
        connectLed.toggle()

#===============================================================================================================================

def set_led(led, val):
    if led == "pwr":
        pwrLed.on() if val else pwrLed.off()
    elif led == "connect":
        connectLed.on() if val else connectLed.off()

#===============================================================================================================================

def get_led_state(led):
    if led == "pwr":
        return pwrLed.state
    elif led == "connect":
        return connectLed.state

#===============================================================================================================================

def get_all():
    val1R = strip1.vals["R"]
    val1G = strip1.vals["G"]
    val1B = strip1.vals["B"]

    val2R = strip2.vals["R"]
    val2G = strip2.vals["G"]
    val2B = strip2.vals["B"]

    val12RGB = {
        "strip1" : {
            "valR" : val1R,
            "valG" : val1G,
            "valB" : val1B
        },
        "strip2" : {
            "valR" : val2R,
            "valG" : val2G,
            "valB" : val2B
        }
    }


    temp = pico_temp_sensor.temp
    connectLedState = connectLed.pin.value() 
    pwrLedState = pwrLed.pin.value()


    data = {
        "rgbVal" : val12RGB,
        "temp" : temp,
        "connectLed" : connectLedState,
        "pwrLed" : pwrLedState
    }
    return data




#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

class temp_sensor:
    def __init__(self,pin) -> None:
        self.adc = machine.ADC(pin)
    def get_tempC(self):
        ADC_voltage = self.adc.read_u16() * (3.3 / (65535))
        temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
        print("Temperature: {}°C ".format(temperature_celcius))
        return temperature_celcius
    def get_tempF(self):
        ADC_voltage = self.adc.read_u16() * (3.3 / (65535))
        temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
        temp_fahrenheit=32+(1.8*temperature_celcius)
        print("Temperature: {}°F".format(temp_fahrenheit))
        return temp_fahrenheit

internal_temp_sensor = temp_sensor(4)
internal_temp_sensor.get_tempF()
