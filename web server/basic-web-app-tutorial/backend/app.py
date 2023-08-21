import os, flask, json, requests, re
import time
from flask_cors import CORS
import communication_with_raspberrypi as raspCom
from communication_with_raspberrypi import get_all
from threading import Thread
"""
Way to run the have requests from frontend:

{
    "objective" : objective of the request (can only be:{
        actions(post requests) {
            "stop",
            "togglePwrLed",
            "toggleConnectLed",
            "rgbStripChange"
        },
        getting Info(get requests) {
            "getRgbValue",
            "getPwrLedState",
            "getConnectLedState",
            "getTemperature",
            "requestList"
        }
    }),
    "additional_info" : additional information (if none just put ""),
}

How to send data to raspberry for aquirement of temp:
    typical get request used before
how to send data to raspberry for actions:
    {
        "objective" : any action,
        "additional_info" : "" if there is additional info see something
    }

"""



app = flask.Flask(__name__)
CORS(app)






valStrip1R = 0
valStrip1G = 0
valStrip1B = 0

valStrip2R = 0
valStrip2G = 0
valStrip2B = 0

valTemp = 0

pwrLedState = False
connectLedState = False
"""
template of request from frontend and to raspberry:
    {
        "objective" : objective of the request
        "additional_info" : additional information (if none just put "")
    }
"""


possibleRequest = {
    "GET/getting info": {
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
        "stoadditional_infop" : {
            "description": "stops the machine",
            "requestCommand": "/stop/"
        },
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
            "answepaddingr": "new state of the power led"
        },
        "toggleConnectLed": {
            "description": "toggles the connection led",
            "requestCommand": "/toggleConnectLed/",
            "answer": "new state of the connection led"
        }
    }
}




@app.route("/", methods=["GET", "POST"])
def main_endpoint():
    print("main endpoint reached...")

    params = flask.request.json

    answer, status_code = process_request(params)
    return flask.jsonify(answer), status_code

def process_request(request:dict):
    if flask.request.method == "GET":
        answer, status_code =get_request_handler(request)
    elif flask.request.method == "POST":
        answer, status_code = post_request_handler(request)
    return answer, status_code


POSSIBLE_GET_REQUESTS = ["getRgbValue", "getPwrLedState", "getConnectLedState", "getTemperature"]
def get_request_handler(request:dict):
    if request["objective"] in POSSIBLE_GET_REQUESTS:
        if request["objective"] == "getRgbValue":
            return get_rgb_value()
        elif request["objective"] == "getPwrLedState":
            return {"PwrLedState": pwrLedState}
        elif request["objective"] == "getConnectLedState":
            return {"ConnectLedState": connectLedState}
        elif request["objective"] == "getTemperature":
            return raspCom.get_temp()
    else:
        return {"error": "unknown objective"}




def get_rgb_value():
    vals= {
        "strip1": {
            "valR": valStrip1R,
            "valG": valStrip1G,
            "valB": valStrip1B
        },
        "strip2": {
            "valR": valStrip2R,
            "valG": valStrip2G,
            "valB": valStrip2B
        }
    }
    return vals

POSSIBLE_POST_REQUESTS = ["stop","togglePwrLed","toggleConnectLed","rgbStripChange"]
def post_request_handler(request:dict):
    if request["objective"] in POSSIBLE_POST_REQUESTS:
        if request["objective"] == "stop":
            answer = raspCom.stop()
        elif request["objective"] == "togglePwrLed":
            answer = raspCom.toggle_pwr_led()
        elif request["objective"] == "toggleConnectLed":
            answer = raspCom.toggle_connect_led()
        elif request["objective"] == "rgbStripChange":
            answer = raspCom.send_change_rgb_value(request["additional_info"])
        else:
            answer ={"error": "unknown objective"}
    else:
        answer = {"error": "unknown objective"}
    return answer


@app.route("/getInfo", methods=["GET"])
def send_all_info():
    global pwrLedState, connectLedState, valStrip1R, valStrip1G, valStrip1B, valStrip2R, valStrip2G, valStrip2B
    answer, status_code = get_all()

    pwrLedState = answer["info"]["pwrLed"]
    connectLedState = answer["info"]["connectLed"]
    valStrip1R = answer["info"]["rgbVal"]["strip1"]["valR"]
    valStrip1G = answer["info"]["rgbVal"]["strip1"]["valG"]
    valStrip1B = answer["info"]["rgbVal"]["strip1"]["valB"]

    valStrip2R = answer["info"]["rgbVal"]["strip2"]["valR"]
    valStrip2G = answer["info"]["rgbVal"]["strip2"]["valG"]
    valStrip2B = answer["info"]["rgbVal"]["strip2"]["valB"]

    print(answer)
    answer = json.dumps(answer["info"])
    return flask.Response(response=answer, status=status_code)


@app.route("/getTemp", methods=["GET"])
def get_temp():
    answer = raspCom.get_temp()
    answer = json.dumps(answer)
    return flask.Response(response=answer, status=200)




@app.route("/code", methods=["POST"])
def my_language():
    # print(flask.request.json)
    # code = flask.request.json["additional_info"]
    # while True:
    #     for i in range(len(code)):
    #         if re.search("red1\+\d", code[i]):
    #             number = int(code[i].split("+")[1])
    #     break
    Thread(code_processing(flask.request.json["additional_info"])).start()
    print("returning")
    return flask.jsonify(flask.request.json),200

def code_processing(code):
    for i in range(15):
        print(i)
        time.sleep(1)
