import json, machine
from picozero import pico_led
from controll import update_rgb,  temp_sensor, toggle_led, get_led_state, get_all

# possibleRequest = {
#     "GET": {
#         "getRgbValue": {
#             "description": "gets the rgb values of the specified strip",
#             "requestCommand": "/getRgbValue",
#             "answer": "dict containing rgb values"
#         },
#         "getPwrLedState": {
#             "description": "gets the power led state",
#             "requestCommand": "/getPwrLedState",
#             "answer": "state of the power led"
#         },
#         "getConnectLedState": {
#             "description": "gets the connection led state",
#             "requestCommand": "/getConnectLedState",
#             "answer": "state of the connection led"
#         },
#         "getTemperature": {
#             "description": "gets the temperature",
#             "requestCommand": "/getTemperature",
#             "answer": "temperature"
#         },
#         "getAll" : {
#             "description": "gets all the data",
#             "requestCommand": "/getAll/",
#             "answer": "dict containing all the data"
#         }
#     },
#     "POST": {
#         "stop" : {
#             "description": "stops the machine",
#             "requestCommand": "/stop/"
#         },
#         "changeRBGValue": {
#             "description": "changes the rgb values of the specified strip",
#             "requestCommand": "/strip/PARAM1/valR/PARAM2/valG/PARAM3/valB/PARAM4",
#             "params": {
#                 "PARAM1": "int specifying the strip to change",
#                 "PARAM2": "int specifying the red value",
#                 "PARAM3": "int specifying the green value",
#                 "PARAM4": "int specifying the blue value",
#             },
#             "answer": "None"
#         },
#         "togglePwrLed": {
#             "description": "toggles the power led",
#             "requestCommand": "/togglePwrLed/",
#             "answer": "new state of the power led"
#         },
#         "toggleConnectLed": {
#             "description": "toggles the connection led",
#             "requestCommand": "/toggleConnectLed/",
#             "answer": "new state of the connection led"
#         }
#     }
# }


class request_handler:
    def __init__(self,request : str, data : dict) -> None:
        print("starting request handler")
        self.method = request.split()[0]
        print(self.method)
        self.data = data
        print(self.data)
        self.answer = {}
        self.status_code = 0
        #--------------------------------------------------
        if self.method == "GET":
            self.get_handler()
        elif self.method == "POST":
            self.post_handler()
    
    #===============================================================
    
    def get_handler(self):
        print("get request handler")
        if self.data["objective"] == "getTemp":
            try:
                temp = temp_sensor(4)
                temp = temp.get_tempC()
                status_code = 200
                self.answer = {"info": temp}
            except:
                self.status_code = 500
                self.answer = {"error": "Could not get the temperature"}
        if self.data["objective"] == "getAll":
            try:
                self.answer = {"info": get_all()}
                self.status_code = 200
            except:
                self.status_code = 500
                self.answer = {"error": "Could not get all the data"}
        else:
            self.status_code = 400
            self.answer = {"error": "Invalid objective"}
    #==================================================================
    
    def post_handler(self):
        print("post request handler")
        if self.data["objective"] == "stop":
            print("stopping the machine")
            try:
               machine.reset()
            except:
                self.status_code = 500
                self.answer = {"error": "Could not stop the machine"}
        elif self.data["objective"] == "togglePwrLed":
            print("toggle Pwr Led")
            try:
                toggle_led("pwr")
                print("pwr led was toggled")
                self.answer = {"info": get_led_state("pwr")}
                self.status_code = 200
                print("done")
            except:
                print("error")
                self.status_code = 500
                self.answer = {"error": "Could not toggle the power led"}
        elif self.data["objective"] == "toggleConnectLed":
            print("toggle Connect Led")
            try:
                toggle_led("connect")
                self.answer = {"info": get_led_state("connect")}
                self.status_code = 200
            except:
                self.status_code = 500
                self.answer = {"error": "Could not toggle the connection led"}
        elif self.data["objective"] == "changeRgbValue":
            print("change rgb value")
            try:
                if verif_rgb_strip_state(self.data["additional_info"]):
                    self.answer, self.status_code = update_rgb(self.data["additional_info"])
                else:
                    self.status_code = 400
                    self.answer = {"error": "Invalid additional information"}
            except:
                self.status_code = 500
                self.answer = {"error": "Could not change the rgb values"}
        print("post request handler done!")
    #==================================================================

#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦

def verif_rgb_strip_state(data:dict):
    #verification of if the request is valid or not
    #to do the verification we verify that there is both the objective and additional_info in the request
    #we then verify that those are the only keys being transmitted in the request
    print(data)
    if data.get("strip_id") != None and data.get("value")!= None and len(list(data.keys())) == 2:
        if data["value"].get("R") != None and data["value"].get("G")!= None and data["value"].get("B")!= None:
            if type(data["strip_id"]) == int and type(data["value"]["R"]) == int and type(data["value"]["G"]) == int and type(data["value"]["B"]) == int:
                if  1 <= data["strip_id"] <=2 and  0 <= data["value"]["R"] <= 133 and 0 <= data["value"]["G"] <= 133 and 0 <= data["value"]["B"] <= 133:
                    print("valid")
                    return True
                else:
                    print("invalid1")
                    return False
            else:
                print("invalid2")
                return False
        else:
            print("invalid3")
            return False
    else:
        print("invalid4")
        return False
