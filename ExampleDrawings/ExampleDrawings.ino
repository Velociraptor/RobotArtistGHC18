// Scroll down for drawing code examples from presentation slide

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
  markerMotor.write(180);
  leftMotor->setSpeed(10);
  rightMotor->setSpeed(10);
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
}

// Actuate the servo to touch the pen to the paper
void _penDown()
{
  markerMotor.write(105);
}

// Actuate the servo to tilt the pen up off the paper
void _penUp()
{
  markerMotor.write(180);
}

// Smarter "wait" to keep pen in position
static bool _putPenDown = false;
void wait(unsigned long time_ms)
{
  unsigned long wait_until = millis() + time_ms;
  do
  {
    if (_putPenDown)
    {
      _penDown();
    }
    else
    {
      _penUp();
    }
  } while (millis() < wait_until);
}

void penDown() { _putPenDown = true; wait(0); }
void penUp() { _putPenDown = false; wait(0); }

// Drive forward at specified speed (0-100%) for specified time (in milliseconds)
void driveForward(int speed_pct, int time_ms)
{
  int speed_val = speed_pct * (255.0 / 100.0);
  leftMotor->setSpeed(speed_val);
  rightMotor->setSpeed(speed_val);
  leftMotor->run(FORWARD);
  rightMotor->run(FORWARD);
  wait(time_ms);
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
  wait(time_ms);
  rightMotor->run(RELEASE);
}

// Run only the left motor to turn right
void turnRight(int time_ms)
{
  leftMotor->setSpeed(100);
  leftMotor->run(FORWARD);
  wait(time_ms);
  leftMotor->run(RELEASE);
}

void drawPentagon()
{
  penDown();
  wait(500);
  for (int i=0; i<5; i++)
  {
    driveForward(25, 1000);
    penUp();
    wait(500);
    turnRight(450);
    wait(500);
    penDown();
    wait(500);
  }
  penUp();
}

void drawSpiral()
{
   penDown();
   wait(500);
   float theta = 0.0;
   for (int i=0; i<50; i++)
   {
      driveForward(25,18);
      float timeTheta = theta * (1000.0 / 360.0); // approximate conversion of angle to time for turning
      turnRight(timeTheta);
      theta += (1.0 / (0.7 + 0.001 * theta));
   }
   penUp();
    
}

void drawSquiggle()
{
  penDown();
  for (int i = 0; i < 2; i++)
  {
    turnRight(1000);
    driveForward(20, 100);
    turnLeft(1000);
    driveForward(20, 100);
  }
  penUp();
}

void drawPicture()
{
    // drawSpiral();
    // drawSquiggle();
    // drawPentagon();
}

void loop() {
  static bool firstRun = true;
  // Wait a few seconds to make sure the robot is on the table before motors run
  wait(3000);
  if (firstRun)
  {
    firstRun = false;
    drawPicture();
  }
}
