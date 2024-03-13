#include <Servo.h>

// Define the servo objects

// Define the pins for the servos
int in1 = 5;
int in2 = 4;
int in3 = 6;
int in4 = 7;

String data = "";

void setup() {
  Serial.begin(115200);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}

void loop() {

  if (Serial.available() > 0)
  {
    data = Serial.readString();
    if(data=="G") //change the string alphabets according to the pyhton code done in the raspberry pi
    {
      forward();

    }

      else if(data=="K")
    {
      backward();

    }
      else  if(data=="S")
    {
      left();

    }
      else  if(data=="F")
    {
      right();

    }
      else  if(data=="B")
    {
      stopMotors();

    }
  }
}

void forward() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void backward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void stopMotors() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}