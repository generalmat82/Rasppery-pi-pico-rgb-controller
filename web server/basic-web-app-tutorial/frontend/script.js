var xhr = null;

const BACKEND_ADDRESS = "http://192.168.0.8:6969"


/**
 * Creates a new XMLHttpRequest object.
 * @return {XMLHttpRequest}
 */
getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        getDate();
        // Set current data text
    }
}

//Updates the time displayed
function getDate() {
    date = new Date().toString();
    document.getElementById('time-container').innerHTML = date;
}
getDate();

function update_info(){
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = update_info_callback;
    xhr.open("GET", `${BACKEND_ADDRESS}/getInfo`, true);
    xhr.send();
}

function get_temp(){
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = get_temp_callback;
    xhr.open("GET", `${BACKEND_ADDRESS}/getTemp`, true);
    xhr.send();
}

function get_temp_callback(){
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        info = JSON.parse(xhr.responseText);
        console.log(info);
    }
}

function update_info_callback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        getDate();
        info = JSON.parse(xhr.responseText);

        console.log(info);
        console.log(typeof(info))


        // Set current data text
        document.getElementById('temp-container').innerHTML = info['temp']+"°C";


        document.getElementById("connect-led-state").innerHTML = info['connectLed'];

        document.getElementById("pwr-led-state").innerHTML = info['pwrLed'];


        //-------------------------------------------------------------------------------------------------------------------------------
        //* seetting the values of the rgb strips


        document.getElementById("grid-rangeR1").value = info["rgbVal"]["strip1"]["valR"];
        document.getElementById("grid-range-valueR1").innerHTML = info["rgbVal"]["strip1"]["valR"];

        document.getElementById("grid-rangeG1").value = info["rgbVal"]["strip1"]["valG"];
        document.getElementById("grid-range-valueG1").innerHTML = info["rgbVal"]["strip1"]["valG"];

        document.getElementById("grid-rangeB1").value = info["rgbVal"]["strip1"]["valB"];
        document.getElementById("grid-range-valueB1").innerHTML = info["rgbVal"]["strip1"]["valB"];

        document.getElementById("grid-rangeR2").value = info["rgbVal"]["strip2"]["valR"];
        document.getElementById("grid-range-valueR2").innerHTML = info["rgbVal"]["strip2"]["valR"];

        document.getElementById("grid-rangeG2").value = info["rgbVal"]["strip2"]["valG"];
        document.getElementById("grid-range-valueG2").innerHTML = info["rgbVal"]["strip2"]["valG"];

        document.getElementById("grid-rangeB2").value = info["rgbVal"]["strip2"]["valB"];
        document.getElementById("grid-range-valueB2").innerHTML = info["rgbVal"]["strip2"]["valB"];

    }
}

update_info();



function toggle_pwr(){
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = toggle_pwr_callback;
    xhr.open("POST", BACKEND_ADDRESS, true);
    xhr.setRequestHeader("Content-type", "application/json");
    data = {objective: "togglePwrLed", "additional_info" : ""};
    xhr.send(JSON.stringify(data));
}

function toggle_pwr_callback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        info = JSON.parse(xhr.responseText);
        // Set current data text
        getDate();
        get_temp();
    }
}



function toggle_connect(){
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = toggle_connect_callback;
    xhr.open("POST", BACKEND_ADDRESS, true);
    xhr.setRequestHeader("Content-type", "application/json");
    data = {objective: "toggleConnectLed", "additional_info" : ""};
    xhr.send(JSON.stringify(data));
}

function toggle_connect_callback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        info = JSON.parse(xhr.responseText);
        // Set current data text
        getDate();
        get_temp();
    }
}


function submit_strip(stripNum){
    valR = document.getElementById(`grid-rangeR${stripNum}`).value;
    valG = document.getElementById(`grid-rangeG${stripNum}`).value;
    valB = document.getElementById(`grid-rangeB${stripNum}`).value;

    data = {objective: "rgbStripChange","additional_info" : {
        "strip_id" : stripNum,
        "R" : parseInt(valR),
        "G" : parseInt(valG),
        "B" : parseInt(valB)
    }}
    var xhr = getXmlHttpRequestObject();
    if (stripNum == 1) {
        xhr.onreadystatechange = submit_strip1_callback;
    }
    else if (stripNum == 2) {
        xhr.onreadystatechange = submit_strip2_callback;
    }
    xhr.open("POST", BACKEND_ADDRESS, true);
    xhr.setRequestHeader("Content-type", "application/json");
    data = JSON.stringify(data);
    console.log(data);
    xhr.send(data);
}


function submit_strip1_callback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        // Set current data text
        getDate();
        get_temp();
    }
}

function submit_strip2_callback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        // Set current data text
        getDate();
        get_temp();
    }
}


document.getElementById("strip1-form").addEventListener("submit", function(e){
    e.preventDefault();
    submit_strip(1);
})

document.getElementById("strip2-form").addEventListener("submit", function(e) {
    e.preventDefault();
    submit_strip(2);
})

function rangeSlide(val,color){
    if (color == "r1") {document.getElementById("grid-range-valueR1").innerHTML = val;}
    else if (color == "g1") {document.getElementById("grid-range-valueG1").innerHTML = val;}
    else if (color == "b1") {document.getElementById("grid-range-valueB1").innerHTML = val;}
    
    else if (color == "r2") {document.getElementById("grid-range-valueR2").innerHTML = val;}
    else if (color == "g2") {document.getElementById("grid-range-valueG2").innerHTML = val;}
    else if (color == "b2") {document.getElementById("grid-range-valueB2").innerHTML = val;}
}

// setInterval(update_info, 10000)


document.getElementById("my-own-language").addEventListener("submit", function(e) {
    e.preventDefault();
    code=document.getElementById("textarea-code").value;
    console.log(code);
    console.log(typeof(code));
    code = code.split("\n");
    request = {objective: "codeInput", "additional_info" : code}
    var xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = submit_code_callback;
    xhr.open("POST", `${BACKEND_ADDRESS}/code`, true);
    xhr.setRequestHeader("Content-type", "application/json");
    data = JSON.stringify(request);
    console.log(data);
    xhr.send(data);
})

function submit_code_callback(){
    console.log("warioj")
}


const handleOnMouseMove = e => {
    const {currentTarget: target} = e;

    const rect = target.getBoundingClientRect(),
        x = e.clientX - rect.left,
        y = e.clientY - rect.top;
    target.style.setProperty("--mouse-x", `${x}px`);
    target.style.setProperty("--mouse-y", `${y}px`);
}

// document.body.onmousemove = e => handleOnMouseMove(e);

for(const card of document.querySelectorAll("button")){
    card.onmousemove = e => handleOnMouseMove(e);
}