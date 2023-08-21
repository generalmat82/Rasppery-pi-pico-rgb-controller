"""
    todo - make so we return status code 200 or 400 or 500 and an answer 
"""

import requests

RASPBERRY_PI_IP_ADDRESS = "http://192.168.0.246:80"

fakeTemp = 12

class rgb_strip:
    def __init__(self):
        self.valR = 0
        self.valG = 0
        self.valB = 0
    def update_rgb(self, r, g, b):
        self.valR = r
        self.valG = g
        self.valB = b


strip1 = rgb_strip()
strip2 = rgb_strip()

pwrLedState = False
connectLedState = False


def make_post_request(data: dict):
    try:
        r = requests.post(RASPBERRY_PI_IP_ADDRESS, json=data)
        print("answer:")
        print(r.json())
        print("status code:")
        print(r.status_code)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"info" : "failed to connect to raspberry pi"}, 512


def stop():
    try:
        data = {"objective" : "stop", "additional_info" : ""}
        requests.post(RASPBERRY_PI_IP_ADDRESS,json=data)
    finally:
        print("restarted")

def toggle_pwr_led():
    global pwrLedState
    pwrLedState = not pwrLedState
    data = {"objective" : "togglePwrLed", "additional_info" : ""}
    answer = make_post_request(data)#- answer from server should be: {status_code : 200/400/500, info : {"newPwrLedState" : true/false}}
    # print(answer.json)
    status_code = 200
    return answer, status_code

def toggle_connect_led():
    global connectLedState
    connectLedState = not connectLedState
    data = {"objective" : "toggleConnectLed", "additional_info" : ""}
    answer = make_post_request(data) #- answer from server should be: {status_code : 200/400/500, info : {"newConnectLedState" : true/false}}
    print(answer)
    status_code = 200
    # answer = {"info" : answer.json}
    return answer, status_code

def send_change_rgb_value(info):
    """
        {
            "objective" : "changeRgbValue",
            "additional_info" : {
                "strip_id" : 1,
                "R" : 0-133,
                "G" : 0-133,
                "B" : 0-133
                }
            }
        }
    """
    print("info:")
    print(info)
    try:
        if info["strip_id"] == 1:
            strip1.update_rgb(info["R"], info["G"], info["B"])
            requestInfo = {
                "objective" : "changeRgbValue",
                "additional_info" : {
                    "strip_id" : 1,
                    "value" : {
                        "R" : strip1.valR,
                        "G" : strip1.valG,
                        "B" : strip1.valB
                    }
                }
            }
            r, Rstatus_code = make_post_request(requestInfo) #- answer from server should be: {status_code : 200/400/500, info : {strip_id : 1/2, "R" : 0-133, "G" : 0-133, "B" : 0-133}}
            if Rstatus_code == 500 or Rstatus_code == 400 :
                answer = {"info" : "error"}
                status_code = 500
            elif Rstatus_code == 512:
                answer = {"info" : "failed to connect to raspberry pi"}
                status_code = 500
            else:
                answer = {"info" : r}
                status_code= 200
        elif info["strip_id"] == 2:
            strip2.update_rgb(info["R"], info["G"], info["B"])
            requestInfo = {
                "objective" : "changeRgbValue",
                "additional_info" : {
                    "strip_id" : 2,
                    "value" : {
                        "R" : strip2.valR,
                        "G" : strip2.valG,
                        "B" : strip2.valB
                    }
                }
            }
            r, Rstatus_code = make_post_request(requestInfo) #- answer from server should be: {status_code : 200/400/500, info : {strip_id : 1/2, "R" : 0-133, "G" : 0-133, "B" : 0-133}}
            if Rstatus_code == 500 or Rstatus_code == 400 :
                answer = {"info" : "error"}
                status_code = 500
            elif Rstatus_code == 512:
                answer = {"info" : "failed to connect to raspberry pi"}
                status_code = 500
            else:
                answer = {"info" : r}
                status_code= 200
        else:
            print("invalid strip id")
            answer = {"info" : "invalid strip id"}
            status_code = 400
    except:
        answer = {"info" : "error"}
        status_code = 500
    finally:
        return answer, status_code


def get_temp():
    global fakeTemp
    # try:
        # data = {"objective" : "getTemp", "additional_info" : ""}
        # r = requests.get(RASPBERRY_PI_IP_ADDRESS,json=data)
        # answer = r.json()#- answer from server should be: {status_code : 200/400/500, info : {"temp" : 0-100}}
        # print(answer)
        # if r.status_code == 500 or r.status_code == 400: 
    #     #     answer = {"info" : "error", "status_code" : r.status_code}
    #     # else:
    #     #     answer = {"info" : answer, "status_code" : 200}
    # except:
    #     answer = {"info" : "error", "status_code" : 500}
    # finally:
    answer = {"info" : {"info" : fakeTemp}}
    fakeTemp += 1
    return answer


def get_all():
    
    request = {"objective" : "getAll", "additional_info" : ""}
    r = requests.get(RASPBERRY_PI_IP_ADDRESS, json=request)
    status_code = 200
    r = r.json()


    
    print(r)
    return r,status_code