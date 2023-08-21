import json, network, socket, machine, sync_time
from time import sleep
from picozero import pico_temp_sensor, pico_led
import secret # .py file with the sensitive credentials (wifiSSID, wifiPassword, ect)
from sync_time import sync_time, strftime
from request_process import request_handler
from controll import toggle_led, update_rgb

#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
#- setup the functions for everything

def connect_wifi():
    ssid = secret.wifiSSID
    password = secret.wifiPassword

    wlan = network.WLAN(network.STA_IF) # type: ignore
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        toggle_led("connect")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

#==============================================================================

def open_port(ip, port):
    address = (ip, port)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

#====================================================================================

def generate_header(status_code):
    """generates the header for the response message

    Args:
        status_code (int): status code

    Returns:
        byte: the header for the response message
    """
    response_version = "HTTP/1.1"
    status_code = "200"
    if status_code == 500: response_phrase = "Internal Server Error"
    elif status_code == 400: response_phrase = "Bad Request"
    elif status_code == 200: response_phrase = "OK"
    else: response_phrase = "N/A"

    server = "raspberry pi/python/1.0"
    date = strftime("%a, %d %b %Y %I:%M:%S %Z", rtc.datetime(), "GMT")
    content_type = "application/json"
    charset = "utf-8"
    content_length = str(len(json.dumps(answer)))
    access_control_allow_origin = "*"
    connection_header = "close"
    header = f"{response_version} {status_code} {response_phrase}\r\nServer: {server}\r\nDate: {date}\r\nContent-Type: {content_type}; charset={charset}\r\nContent-Length: {content_length}\r\nAccess-Control-Allow-Origin: {access_control_allow_origin}\r\nConnection: {connection_header}\r\n\r\n"
    return header.encode('utf-8')

def setup():
    """setsup the picozero for wifi, rtc, and opening port 80
    """
    ip = connect_wifi()
    rtc = machine.RTC()
    sync_time(rtc)
    connection = open_port(ip, 80)
    return ip,rtc,connection

#¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
try:


    ip,rtc,connection = setup()
    pico_led.off()
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    sleep(0.5)
    pico_led.on()
    sleep(0.5)
    pico_led.off()
    temperature = 0
    print("awating requests...")
    # update_rgb({"strip_id" : 1, "value" : {"R": 50, "G": 50, "B": 50}})
    while True:
        client, addr = connection.accept()
        print(f'Connection from {addr} accepted')

        #Thanks to u/justbuchanan for helping figureing out how to catch post requests!
        header = client.recv(1024)
        header = header.decode('utf-8')
        print("Header:")
        print(header)

        params = client.recv(1024)
        params = params.decode('utf-8')
        
        print("params:")

        params = json.loads(params)
        print(params)

        #verification of if the request is valid or not
        #to do the verification we verify that there is both the objective and additional_info in the request
        #we then verify that those are the only keys being transmitted in the request
        if params.get("objective") != None and params.get("additional_info")!= None and len(list(params.keys())) == 2:
            print("valid")
            requestHandler = request_handler(header,params)
            status_code = requestHandler.status_code
            answer = requestHandler.answer
        else:
            print("invalid")
            answer = {"error" : "invalid request"}
            status_code = 400


        client.send(generate_header(status_code))
        client.send(json.dumps(answer).encode('utf-8'))
        client.close()
except KeyboardInterrupt:
    machine.reset()