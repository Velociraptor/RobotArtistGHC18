#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h> 

// Create the motor shield object and motor objects
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *leftMotor  = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);
Servo markerMotor;

void setup() {
  // Set up motors to run when instructed
  AFMS.begin();
  markerMotor.attach(10);
  markerMotor.write(90);
  leftMotor->setSpeed(10);
  rightMotor->setSpeed(10);
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
}

// Actuate the servo to touch the pen to the paper
void penDown()
{
  markerMotor.write(0);
}

// Actuate the servo to tilt the pen up off the paper
void penUp()
{
  markerMotor.write(90);
}

// Drive forward at specified speed (0-100%) for specified time (in milliseconds)
void driveForward(int speed_pct, int time_ms)
{
  int speed_val = speed_pct * (255.0 / 100.0);
  leftMotor->setSpeed(speed_val);
  rightMotor->setSpeed(speed_val);
  leftMotor->run(FORWARD);
  rightMotor->run(FORWARD);
  delay(time_ms);
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
}

/* Run only the right drive motor to turn left
  Hint: this is only one way to turn left -- experiment with different 
  motor speed settings or try running the left motor backwards at the
  same time to change the turning behavior to suit your needs. */
void turnLeft(int time_ms)
{
  rightMotor->setSpeed(100);
  rightMotor->run(FORWARD);
  delay(time_ms);
  rightMotor->run(RELEASE);
}

// Run only the left motor to turn right
void turnRight(int time_ms)
{
  leftMotor->setSpeed(100);
  leftMotor->run(FORWARD);
  delay(time_ms);
  leftMotor->run(RELEASE);
}

// Testing... TODO: REMOVE THESE FUNCTIONS AFTER TESTING
void drawSquare(int sideLength)
{
  int scaleFactor = 50;
  penDown();
  for (int i=0; i<4; i++)
  {
    driveForward(sideLength * scaleFactor);
    turnRight();
  }
}

void drawArc(int radius, int angle)
{
  
}

void drawGHC()
{
  
}

void starter()
{
  penDown();
  driveForward(20, 1000);
  penUp();
  turnRight();
  delay(1000);
  turnLeft();
}

void loop() {
  //starter();
  penDown();
  delay(1000);
  penUp();
  delay(1000);
}
