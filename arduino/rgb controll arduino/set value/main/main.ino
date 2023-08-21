const int RED_PIN = 13;
const int GREEN_PIN = 12;
const int BLUE_PIN = 11;


int redVal = 255;
int greenVal = 255;
int blueVal = 255;

void setup()
{
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    
    analogWrite(RED_PIN, redVal);
    analogWrite(GREEN_PIN, greenVal);
    analogWrite(BLUE_PIN, blueVal);

}

void loop(){
    delay(10000);
}
