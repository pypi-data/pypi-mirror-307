# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:14:06 2024

@author: user01
"""

# -*- coding: utf-8 -*-
'''file hello_world.py
 # @brief display "hello,world!"
 # @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 # @licence     The MIT License (MIT)
 # @maintainer [yangfeng](feng.yang@dfrobot.com)
 # @version  V1.0
 # @date  2021-09-26
 # @url https://github.com/DFRobot/DFRobot_RGBLCD1602
'''
import sys
sys.path.append('../')
from DFRobot_RGBLCD1602_telemetrix import *
import time
from telemetrix import telemetrix

colorR = 255
colorG = 0
colorB = 0
# Change the rgb_addr value based on the hardware version
# -----------------------------------------
#        Moudule        | Version|rgb_addr|
# -----------------------------------------
#   LCD1602 Module      |  V1.0  | 0x60   |
# -----------------------------------------
#   LCD1602 Module      |  V1.1  | 0x6B   |
# -----------------------------------------
#   LCD1602 RGB Module  |  V1.0  | 0x60   |
# -----------------------------------------
#   LCD1602 RGB Module  |  V2.0  | 0x2D   |
# -----------------------------------------

board = board = telemetrix.Telemetrix(com_port="COM4")
board.set_pin_mode_i2c()
lcd=DFRobot_RGBLCD1602(board)                               #create LCD object,specify col and row

'''
  @brief set RGB
  @param r  red   range(0-255)
  @param g  green range(0-255)
  @param b  blue  range(0-255)
'''
lcd.set_RGB(colorR, colorG, colorB)
time.sleep(1)
lcd.clear()    
lcd.set_RGB(0, 0, 0)
# Print a message to the LCD.
'''
  @brief output data to LCD to display
  @param arg output data
'''
lcd.print_out("hello, world!")
lcd.scroll_display_left()
time.sleep(1)
lcd.scroll_display_left()

time.sleep(1)
lcd.no_display()

time.sleep(1)
lcd.display()

i = 0

while True:
  i = i+1
  # set the cursor to column 0, line 1
  # (note: line 1 is the second row, since counting begins with 0):
  '''
    @brief set cursor position
    @param col columns optional range 0-15
    @param row rows optional range 0-1，0 is the first row, 1 is the second row
  '''
  lcd.set_cursor(0, 1)
  # print the number of seconds since reset:
  lcd.print_out(i)
  time.sleep(1)
