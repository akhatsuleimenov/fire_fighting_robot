#!/usr/bin/env python3
 
# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *
 
# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
 
spkr = Sound()
radio = Radio()
 
color_sensor_in1 = ColorSensor(INPUT_1)
ultrasonic_sensor_in2 = UltrasonicSensor(INPUT_2)
gyro_sensor_in3 = GyroSensor(INPUT_3)
gps_sensor_in4 = GPSSensor(INPUT_4)
motorC = LargeMotor(OUTPUT_C) # Arm
 
# Firefighter robot
BASE_SPEED = 10 # global base speed
 
def follow_line():
    multiplier = 1.5 * (color_sensor_in1.reflected_light_intensity - 50)
    tank_drive.on(BASE_SPEED - multiplier, BASE_SPEED + multiplier)
 
def pour_water(to_rescue):
    tank_drive.off(brake = True)
    motorC.on_to_position(5, 0) # pour water over person
    time.sleep(2)
    motorC.on_to_position(5, 90) # raise back the arm
    to_rescue -= 1 # 1 person rescued
    tank_drive.on_for_rotations(BASE_SPEED, (-BASE_SPEED), 2) # turn back to follow the right path of the line
    tank_drive.on_for_rotations(BASE_SPEED, BASE_SPEED, 0.3) # drive towards it
    return to_rescue
 
def avoid_obstacle():
    for sign, dist in ((1, 1), (-1, 2), (-1, 1)): # go around the obstacle
        tank_drive.on_for_rotations(BASE_SPEED * sign, (-BASE_SPEED) * sign, 0.695)
        tank_drive.on_for_rotations(BASE_SPEED, BASE_SPEED, 1 * dist)
        tank_drive.off(brake=True)
 
def firefighter_robot(to_rescue):
    while True:
        if to_rescue == 0:
            break
        if color_sensor_in1.color_name == 'White': # location of person found
            to_rescue = pour_water(to_rescue)
            print(to_rescue)
        else:
            avoid_obstacle() if ultrasonic_sensor_in2.distance_centimeters <= 8 else follow_line()
    
if __name__ == '__main__':
    motorC.on_to_position(5, 90) # put the arm up
    to_rescue = 3 # people to rescue
    firefighter_robot(to_rescue)
    print("All people have been rescued! Good job!")
