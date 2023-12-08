import os
import flask
import json
from flask_cors import CORS
from HTTPResource import get_request
import requests

app = flask.Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if flask.request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username": "user4",
                "pets": ["hamster"]
            })

            return flask.jsonify(data)
    if flask.request.method == "POST":
        received_data = flask.request.get_json()
        print(received_data)
        print(f"received data: {received_data}")
        message = received_data['data']
        
        
        message2 = "get_data"

        if message == "get_data":
            r = get_request("192.168.0.246","/getRgbValue")
            r = json.loads(r)
            print(r)
            message2 = r


        
        return_data = {
            "status": "success",
            "message": f"received: {message}",
            "data": message2
        }
        return flask.Response(response=json.dumps(return_data), status=201)





@app.route('/colors', methods=["GET","POST"])
def colors():
    print("colors endpoint reached...")
    received_data = flask.request.get_json()
    print(received_data)
    print(f"received data: {received_data}")
    command = f'curl -d "/strip/{received_data["strip"]}/valR/{received_data["r"]}/valG/{received_data["g"]}/valB/{received_data["b"]}" 192.168.0.246:80'
    print(command)
    os.system(command)
    

    return flask.Response(response="recived", status=201);


@app.route('/dataTrans',methods=["GET","POST"])
def dataTrans():
    print("dataTrans endpoint reached...")
    received_data = flask.request.get_json();
    print(received_data)
    if received_data["methode"] == "POST":
        r = requests.post('http://192.168.0.246:80', data=received_data)
    elif received_data["methode"] == "GET":
        r = requests.get(f'http://192.168.0.246:80{received_data["request"]}')
        # r = get_request("192.168.0.246",received_data,port=80)
    print(r)
    flask.request

    r.json()
    return flask.Response(response=r, status=201,headers={"Access-Control-Allow-Origin": "*"});
    






if __name__ == "__main__":
    app.run("localhost", 6969)