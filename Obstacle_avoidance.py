import RPi.GPIO as GPIO
import time

# =========================
# GPIO SETUP
# =========================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# =========================
# MOTOR PINS
# =========================
MotorA_Forward = 17
MotorA_Backward = 18
MotorB_Forward = 22
MotorB_Backward = 23

motor_pins = [
    MotorA_Forward,
    MotorA_Backward,
    MotorB_Forward,
    MotorB_Backward
]

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# PWM setup
pwmMotorA_Forward = GPIO.PWM(MotorA_Forward, 100)
pwmMotorA_Backward = GPIO.PWM(MotorA_Backward, 100)
pwmMotorB_Forward = GPIO.PWM(MotorB_Forward, 100)
pwmMotorB_Backward = GPIO.PWM(MotorB_Backward, 100)

pwmMotorA_Forward.start(0)
pwmMotorA_Backward.start(0)
pwmMotorB_Forward.start(0)
pwmMotorB_Backward.start(0)

# =========================
# ULTRASONIC SENSOR PINS
# =========================
Trig_Center = 24
Echo_Center = 25

Trig_Left = 5
Echo_Left = 6

Trig_Right = 13
Echo_Right = 19

sensor_pins = [
    Trig_Center, Echo_Center,
    Trig_Left, Echo_Left,
    Trig_Right, Echo_Right
]

GPIO.setup(Trig_Center, GPIO.OUT)
GPIO.setup(Echo_Center, GPIO.IN)

GPIO.setup(Trig_Left, GPIO.OUT)
GPIO.setup(Echo_Left, GPIO.IN)

GPIO.setup(Trig_Right, GPIO.OUT)
GPIO.setup(Echo_Right, GPIO.IN)

GPIO.output(Trig_Center, False)
GPIO.output(Trig_Left, False)
GPIO.output(Trig_Right, False)

# =========================
# SETTINGS
# =========================
DutyCycle = 55
Stop = 0
safe_distance = 25  # cm
turn_time = 0.45    # seconds

# =========================
# DISTANCE FUNCTION
# =========================
def measure_distance(trig, echo):
    GPIO.output(trig, False)
    time.sleep(0.02)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    timeout = start_time + 0.04

    while GPIO.input(echo) == 0:
        start_time = time.time()
        if start_time > timeout:
            return 999

    stop_time = time.time()
    timeout = stop_time + 0.04

    while GPIO.input(echo) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            return 999

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return round(distance, 2)

# =========================
# MOTOR FUNCTIONS
# =========================
def stop_motors():
    pwmMotorA_Forward.ChangeDutyCycle(Stop)
    pwmMotorA_Backward.ChangeDutyCycle(Stop)
    pwmMotorB_Forward.ChangeDutyCycle(Stop)
    pwmMotorB_Backward.ChangeDutyCycle(Stop)

def move_forward():
    pwmMotorA_Forward.ChangeDutyCycle(DutyCycle)
    pwmMotorA_Backward.ChangeDutyCycle(Stop)
    pwmMotorB_Forward.ChangeDutyCycle(DutyCycle)
    pwmMotorB_Backward.ChangeDutyCycle(Stop)

def move_backward():
    pwmMotorA_Forward.ChangeDutyCycle(Stop)
    pwmMotorA_Backward.ChangeDutyCycle(DutyCycle)
    pwmMotorB_Forward.ChangeDutyCycle(Stop)
    pwmMotorB_Backward.ChangeDutyCycle(DutyCycle)

def turn_left():
    pwmMotorA_Forward.ChangeDutyCycle(Stop)
    pwmMotorA_Backward.ChangeDutyCycle(DutyCycle)
    pwmMotorB_Forward.ChangeDutyCycle(DutyCycle)
    pwmMotorB_Backward.ChangeDutyCycle(Stop)

def turn_right():
    pwmMotorA_Forward.ChangeDutyCycle(DutyCycle)
    pwmMotorA_Backward.ChangeDutyCycle(Stop)
    pwmMotorB_Forward.ChangeDutyCycle(Stop)
    pwmMotorB_Backward.ChangeDutyCycle(DutyCycle)

# =========================
# OBSTACLE AVOIDANCE
# =========================
def avoid_obstacle():
    center_distance = measure_distance(Trig_Center, Echo_Center)
    left_distance = measure_distance(Trig_Left, Echo_Left)
    right_distance = measure_distance(Trig_Right, Echo_Right)

    print(f"Center: {center_distance} cm | Left: {left_distance} cm | Right: {right_distance} cm")

    if center_distance > safe_distance:
        print("Moving forward")
        move_forward()

    else:
        print("Obstacle detected")
        stop_motors()
        time.sleep(0.2)

        if left_distance > right_distance and left_distance > safe_distance:
            print("Turning left")
            turn_left()
            time.sleep(turn_time)

        elif right_distance > left_distance and right_distance > safe_distance:
            print("Turning right")
            turn_right()
            time.sleep(turn_time)

        else:
            print("No clear path, reversing")
            move_backward()
            time.sleep(0.5)

            stop_motors()
            time.sleep(0.2)

            print("Turning around")
            turn_right()
            time.sleep(0.7)

        stop_motors()
        time.sleep(0.1)

# =========================
# MAIN PROGRAM
# =========================
try:
    print("Starting obstacle avoidance robot...")
    time.sleep(1)

    while True:
        avoid_obstacle()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping robot...")
    stop_motors()
    GPIO.cleanup()
