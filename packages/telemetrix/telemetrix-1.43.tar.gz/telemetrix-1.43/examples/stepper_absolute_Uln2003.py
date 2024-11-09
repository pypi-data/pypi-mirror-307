"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""

import sys
import time

from telemetrix import telemetrix

"""
Run a motor to an absolute position. Server will send a callback notification 
when motion is complete.
"""

# Create a Telemetrix instance.
board = telemetrix.Telemetrix()


def the_callback(data):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    print(f'Motor {data[1]} absolute motion completed at: {date}.')


def running_callback(data):
    if data[1]:
        print('The motor is running.')
    else:
        print('The motor IS NOT running.')


# create an accelstepper instance for a TB6600 motor driver
motor = board.set_pin_mode_stepper(interface=8, pin1=8, pin2=9, pin3=10, pin4=11)
board.stepper_is_running(motor, callback=running_callback)
time.sleep(.2)
# set the max speed and acceleration
board.stepper_set_max_speed(motor, 1000)
board.stepper_set_acceleration(motor, 800)

# set the absolute position in steps
board.stepper_move_to(motor, 2000)

# run the motor
print('Starting motor...')
board.stepper_run(motor, completion_callback=the_callback)
time.sleep(.2)
board.stepper_is_running(motor, callback=running_callback)
time.sleep(.2)

# keep application running
while True:
    try:
        time.sleep(.2)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)
