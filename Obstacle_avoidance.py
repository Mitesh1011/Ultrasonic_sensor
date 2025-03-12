import RPi.GPIO as GPIO
import time

# Set GPIO modecle(DutyCycle)
    pwmMotorB_Backward.ChangeDutyCycle(Stop)

def turn_right():
    pwmMotorA_Forward.ChangeDutyCycle(DutyCycle)
    pwmMotorA_Backward.ChangeDutyCycle(Stop)
    pwmMotorB_Forward.ChangeDutyCycle(Stop)
    pwmMotorB_Backward.ChangeDutyCycle(DutyCycle)

# Obstacle avoidance logic
def avoid_obstacle():
    center_distance = measure_distance(Trig_Center, Echo_Center)
    left_distance = measure_distance(Trig_Left, Echo_Left)
    right_distance = measure_distance(Trig_Right, Echo_Right)

    print(f"Center: {center_distance} cm, Left: {left_distance} cm, Right: {right_distance} cm")

    if center_distance < safe_distance:
        stop_motors()
        time.sleep(0.1)
       
        if left_distance > right_distance and left_distance > safe_distance:
            print("Turning left")
            turn_left()
            time.sleep(turn_time)
        elif right_distance > left_distance and right_distance > safe_distance:
            print("Turning right")
            
        move_forward()

# Main loop
try:
    print("Starting obstacle avoidance...")
    time.sleep(0.5)

    while True:
        avoid_obstacle()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping robot...")
    GPIO.cleanup()
