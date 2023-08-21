#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};
byte rowPins[ROWS] = {23, 25, 27, 29}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {31, 33, 35, 37}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

const int RED_PIN = 6;
const int GREEN_PIN = 5;
const int BLUE_PIN = 4;


void setup(){
    Serial.begin(9600);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
}

char selectedColor;
String colorVal;

void loop(){
    char customKey = customKeypad.getKey();
    if (customKey){
        Serial.println(customKey);
        if (customKey == 'A'){
            selectedColor = 'R';
        }
        else if (customKey == 'B'){
            selectedColor = 'G';
        }
        else if (customKey == 'C'){
            selectedColor = 'B';
        }
        else if (customKey == '*'){
            send(selectedColor,colorVal);
        }
        else if (customKey == '#'){
            int lastIndex = colorVal.length() - 1;
            colorVal.remove(lastIndex);
            Serial.println(colorVal);
        }
        else if (customKey == 'D'){}
        else {
            colorVal += customKey;
            Serial.println(colorVal);
        }
    }
}

void send(char selectedColor, String val){
    Serial.println(selectedColor);
    Serial.println(val);
    int val2 = val.toInt();
    if (selectedColor == 'R'){
        analogWrite(RED_PIN, val2);
    }
    else if (selectedColor == 'G'){
        analogWrite(GREEN_PIN, val2);
    }
    else if (selectedColor == 'B'){
        analogWrite(BLUE_PIN, val2);
    }
    colorVal = "";
}
