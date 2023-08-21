const int RED_PIN = 6;
const int GREEN_PIN = 5;
const int BLUE_PIN = 3;

void setup()
{
    Serial.begin(9600);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
}

// void loop()
// {
//     digitalWrite(RED_PIN, HIGH);
//     digitalWrite(GREEN_PIN, HIGH);
//     digitalWrite(BLUE_PIN, HIGH);
//     analogWrite(RED_PIN, 85);
//     delay(500);
//     analogWrite(GREEN_PIN, 85);
//     delay(500);
//     analogWrite(BLUE_PIN, 85);
// }

int valRed = 0;
int valGreen = 0;
int valBlue = 0;

void loop(){
    valRed = valRed + 5;
    analogWrite(RED_PIN, valRed);
    Serial.println(valRed);
    delay(500);
    valGreen = valGreen + 5;
    analogWrite(GREEN_PIN, valGreen);
    Serial.println(valGreen);
    delay(500);
    valBlue = valBlue + 5;
    analogWrite(BLUE_PIN, valBlue);
    Serial.println(valBlue);
    delay(500);
}