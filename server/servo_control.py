import RPi.GPIO as GPIO
from time import sleep

step = 1.2

def initialize_servo():
    default_position = 6
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)
    servo.ChangeDutyCycle(default_position)
    sleep(0.05)

    return default_position

def move_servo(position, direction):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(11, GPIO.OUT)
    servo = GPIO.PWM(11, 50)
    servo.start(0)

    if direction == "right":
        new_position = position-step
        if(new_position <= 0):
            new_position = 0.1
        servo.ChangeDutyCycle(new_position)
        sleep(0.05)

    elif direction == "left":
        new_position = position+step
        if(new_position > 12):
            new_position = 12
        servo.ChangeDutyCycle(new_position)
        sleep(0.05)
    else:
        pass

    servo.stop()
    GPIO.cleanup()

    return new_position

# initialize_servo()
# while True:
#     inp = input("Direction (a/b):")
#     print(position)
#     if inp == "a":
#         move_servo("left")
#     elif inp == "b":
#         move_servo("right")
#     else:
#         pass