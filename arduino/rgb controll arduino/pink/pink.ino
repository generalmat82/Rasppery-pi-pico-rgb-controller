const int RED_PIN = 6;
const int GREEN_PIN = 5;
const int BLUE_PIN = 3;


int redVal = 0;
int greenVal = 0;
int blueVal = 0;

void setup()
{
    Serial.begin(9600);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    
    Serial.println("red val:");
    while (Serial.available()==0){}
    redVal = Serial.parseInt();
    Serial.println("got: ");
    Serial.println(redVal);
    analogWrite(RED_PIN, redVal);

    Serial.println("green val:");
    while (Serial.available()==0){}
    greenVal = Serial.parseInt();
    Serial.println("got: ");
    Serial.println(greenVal);
    analogWrite(GREEN_PIN, greenVal);

    Serial.println("blue val:");
    while (Serial.available()==0){}
    blueVal = Serial.parseInt();
    Serial.println("got: ");
    Serial.println(blueVal);
    analogWrite(BLUE_PIN, blueVal);

}

void loop(){
    delay(1000);
}