"""
todo -0- add power led indicator, color states for rgb for each strips on webpage
/todo/ -1- Make circuit fit on 1 breadboard
/todo/ -2- Make sure circuit 1 breadboard is working
/todo/ -3- Make circuit fit on solder breadboard
/todo/ -4- Make sure circuit 2 breadboard is working
/todo/ -5- solder
/todo/ -6- test soldered circuit
todo -7- hope it works
"""


import json
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = 'BossNetwork'
password = 'PswdWiFi01'

connectionLed = machine.Pin(14, machine.Pin.OUT)
powerled = machine.Pin(15, machine.Pin.OUT)
powerled.on()

strip1R = machine.PWM(machine.Pin(18))
strip1R.freq(1000)      # Set the frequency value
strip1RVal = 0     #initial value of the red of strip 1

strip1G = machine.PWM(machine.Pin(16))
strip1G.freq(1000)      # Set the frequency value
strip1GVal = 0     #initial value of the green of strip 1

strip1B = machine.PWM(machine.Pin(21))
strip1B.freq(1000)      # Set the frequency value
strip1BVal = 0     #initial value of the blue of strip 1



strip2R = machine.PWM(machine.Pin(19))
strip2R.freq(1000)      # Set the frequency value
strip2RVal = 0     #initial value of the red of strip 2

strip2G = machine.PWM(machine.Pin(17))
strip2G.freq(1000)      # Set the frequency value
strip2GVal = 0     #initial value of the green of strip 2

strip2B = machine.PWM(machine.Pin(20))
strip2B.freq(1000)      # Set the frequency value
strip2BVal = 0     #initial value of the blue of strip 2




def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        connectionLed.toggle()
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection




def webpage():
    """generates the html file for the webpage

    Returns:
        str: string with the html information
    """
    
    if powerled.value() == 1:
        pwrLedState = 'ON'
    else:
        pwrLedState = 'OFF'
    
    if connectionLed.value() == 1:
        connLedState = 'ON'
    else:
        connLedState = 'OFF'
    temperature = pico_temp_sensor.temp
    with open('index.html', 'r') as f:
        html = f.read()
    html = html.replace('{temperature}', str(temperature))
    html = html.replace('{pwrLedState}', pwrLedState)
    html = html.replace('{ConnectLedState}', connLedState)
    html = html.replace('{strip1RVal}',str(strip1RVal))
    html = html.replace('{strip1GVal}',str(strip1GVal))
    html = html.replace('{strip1BVal}',str(strip1BVal))
    html = html.replace('{strip2RVal}',str(strip2RVal))
    html = html.replace('{strip2GVal}',str(strip2GVal))
    html = html.replace('{strip2BVal}',str(strip2BVal))
    return str(html)



class request_handler:
    def __init__(self, request):
        self.request = request
        print("raw request: ")
        print(self.request)

        self.extract_data()

    def extract_data(self):
        requestSplit = self.request.split()
        if (requestSplit[0] == "b'GET"):
            self.requestData = requestSplit[1]
            self.methode = "GET"
        else: #elif (requestSplit[0] == "b'POST"):
            self.requestData = requestSplit[-1]
            self.methode = "POST"
        print("requestData: ")
        print(self.requestData)
        self.requestDataList = self.requestData.split("/")
        print(self.requestDataList)
        self.requestDataList.pop(0)
        if self.methode == "POST":
            self.requestDataList.pop(0)
            self.requestDataList[-1] = self.requestDataList[-1][:len(self.requestDataList[-1]) - len("'")]
        print("requestDataList: ")
        print(self.requestDataList)

    def extract_params(self):
        self.stripStates = {"strip1": {"update":False, "valR": 0, "valG": 0, "valB": 0}, "strip2": {"update":False,"valR": 0, "valG": 0, "valB":0}}
        try:
            if self.requestDataList[1] == "1":
                self.stripStates["strip1"]["update"] = True
                self.stripStates["strip1"]["valR"] = int(self.requestDataList[3])
                self.stripStates["strip1"]["valG"] = int(self.requestDataList[5])
                self.stripStates["strip1"]["valB"] = int(self.requestDataList[7])
            elif self.requestDataList[1] == "2":
                self.stripStates["strip2"]["update"] = True
                self.stripStates["strip2"]["valR"] = int(self.requestDataList[3])
                self.stripStates["strip2"]["valG"] = int(self.requestDataList[5])
                self.stripStates["strip2"]["valB"] = int(self.requestDataList[7])
            else:
                self.stripStates = False
        except IndexError:
            self.stripStates = False
 




def serve(connection):
    global strip1RVal, strip1GVal, strip1BVal, strip2RVal, strip2GVal, strip2BVal
    #Start a web server
    state = "off"
    pico_led.off()
    pico_led.on()
    sleep(1)
    pico_led.off()
    sleep(1)
    pico_led.on()
    sleep(1)
    pico_led.off()
    temperature = 0
    while True:
        client, addr = connection.accept()
        print(f'Connection from {addr} accepted')

        request = client.recv(1024)
        request = str(request)

        answer = request_processing(request)
        client.send(answer)
        client.close()


def update_rgb(request):
    """updates the rgb values of the specified strip

    Args:
        request (request_handler): the handled request object
    Returns:
        Nan: returns nothing
    """
    global strip1RVal, strip1GVal, strip1BVal, strip2RVal
    if request.stripStates["strip1"]["update"]:
        print("update strip1")
        strip1R.duty_u16(int(request.stripStates["strip1"]["valR"]*500))
        strip1RVal = request.stripStates["strip1"]["valR"]
        strip1G.duty_u16(int(request.stripStates["strip1"]["valG"]*500))
        strip1GVal = request.stripStates["strip1"]["valG"]
        strip1B.duty_u16(int(request.stripStates["strip1"]["valB"]*500))
        strip1BVal = request.stripStates["strip1"]["valB"]
    if request.stripStates["strip2"]["update"]:
        print("update strip2")
        strip2R.duty_u16(int(request.stripStates["strip2"]["valR"]*500))
        strip2RVal = request.stripStates["strip2"]["valR"]
        strip2G.duty_u16(int(request.stripStates["strip2"]["valG"]*500))
        strip2GVal = request.stripStates["strip2"]["valG"]
        strip2B.duty_u16(int(request.stripStates["strip2"]["valB"]*500))
        strip2BVal = request.stripStates["strip2"]["valB"]
# end def


def request_processing(request):
    """process the request to determine what would be necesary to do

    Args:
        request (str): the request to be processed

    Returns:
        request_handler, bool: a request_handler object or a boolean indicating the action necessary
    """
    request = request_handler(request)

    #-------------------------------------------------------------------------------------------------------------------------------
    #*Section that checks if the request is for an led toggle or to reset the machine

    #-------------------------------------------------------------------------------------------------------------------------------
    #*section that determines what action to take

    request.extract_params()

    if request.methode == "GET":
        answer = get_request_processing(request)
    elif request.methode == "POST":
        answer = post_request_processing(request)
    return answer


    return request

def get_request_processing(request):
    """determines what action to take if the request is a GET request

    Args:
        request (request_handler): handled request object
    """
    if request.requestData == "/stop/":
        machine.reset()
        return
    elif request.requestData == "/togglePwrLed/": 
        powerled.toggle()
        return webpage()
    
    elif request.requestData == "/toggleConnectLed/":
        connectionLed.toggle()
        return webpage()


    if request.stripStates != False:
        print(request.stripStates)
        update_rgb(request)
    if request.requestData == "/getRgbValue":
        vals= {
            "strip1": {
                "valR": strip1RVal,
                "valG": strip1GVal,
                "valB": strip1BVal
            },
            "strip2": {
                "valR": strip2RVal,
                "valG": strip2GVal,
                "valB": strip2BVal
            }
        }
        return json.dumps(vals)
    elif request.requestData == "/getPwrLedState/":
        if powerled.value() == 1:
            state = {"PwrLedState": "ON"}
            return json.dumps(state)
        else:
            state = {"PwrLedState": "OFF"}
            return json.dumps(state)
    elif request.requestData == "/getConnectLedState/":
        if connectionLed.value() == 1:
            state = {"ConnectLedState": "ON"}
            return json.dumps(state)
        else:
            state = {"ConnectLedState": "OFF"}
            return json.dumps(state)
    elif request.requestData == "/getTemperature/":
        temp = {"temp": pico_temp_sensor.temp}
        return json.dumps(temp)
    elif request.requestData == "/":
        return webpage()
    elif request.requestData == "/requestList/":
        possibleRequest = {
            "GET": {
                "stop": {
                    "description": "stops the machine",
                    "requestCommand": "/stop/"
                },
                "togglePwrLed": {
                    "description": "toggles the power led",
                    "requestCommand": "/togglePwrLed/",
                    "answer": "Html page"
                },
                "toggleConnectLed": {
                    "description": "toggles the connection led",
                    "requestCommand": "/toggleConnectLed/",
                    "answer": "Html page"
                },
                "getRgbValue": {
                    "description": "gets the rgb values of the specified strip",
                    "requestCommand": "/getRgbValue",
                    "answer": "dict containing rgb values"
                },
                "getPwrLedState": {
                    "description": "gets the power led state",
                    "requestCommand": "/getPwrLedState",
                    "answer": "state of the power led"
                },
                "getConnectLedState": {
                    "description": "gets the connection led state",
                    "requestCommand": "/getConnectLedState",
                    "answer": "state of the connection led"
                },
                "getTemperature": {
                    "description": "gets the temperature",
                    "requestCommand": "/getTemperature",
                    "answer": "temperature"
                },
            },
            "POST": {
                "changeRBGValue": {
                    "description": "changes the rgb values of the specified strip",
                    "requestCommand": "/strip/PARAM1/valR/PARAM2/valG/PARAM3/valB/PARAM4",
                    "params": {
                        "PARAM1": "int specifying the strip to change",
                        "PARAM2": "int specifying the red value",
                        "PARAM3": "int specifying the green value",
                        "PARAM4": "int specifying the blue value",
                    },
                    "answer": "None"
                },
                "togglePwrLed": {
                    "description": "toggles the power led",
                    "requestCommand": "/togglePwrLed/",
                    "answer": "new state of the power led"
                },
                "toggleConnectLed": {
                    "description": "toggles the connection led",
                    "requestCommand": "/toggleConnectLed/",
                    "answer": "new state of the connection led"
                }
            }
        }
        return json.dumps(possibleRequest)
    else:
        answer = {"answer": "Invalid request"}
        return json.dumps(answer)



def post_request_processing(request):
    """determines what action to take if the request is a POST request

    Args:
        request (request_handler): handled request object
    """
    
    if request.stripStates!= False:
        print(request.stripStates)
        update_rgb(request)
    
    if request.requestData == "/togglePwrLed/":
        powerled.toggle()
        if powerled.value() == 1:
            state = "ON"
        else:
            state = "OFF"
        answer = {"pwrLedState": state}
        return json.dumps(answer)
    
    elif request.requestData == "/toggleConnectLed/":
        connectionLed.toggle()
        if connectionLed.value() == 1:
            state = "ON"
        else:
            state = "OFF"
        answer = {"connectLedState": state}
        return json.dumps(answer)
    else:
        answer = {"answer": "Invalid request"}
        return json.dumps(answer)

    





try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except:
    machine.reset()
