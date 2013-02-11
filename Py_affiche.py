#!/usr/bin/python
#-*- coding: utf-8 -*-

##########################################################
#
# Le contrôleur du journal lumineux est un aniview2000
# http://www.2008led.com/en/displayproduct.html?proTypeID=156118&proID=2194718
#
##########################################################

import argparse
import serial

parser = argparse.ArgumentParser()
parser.add_argument("texte", help="display the string you use here")
parser.add_argument("-p", "--port", help="selected port - default /dev/ttyUSB0")
parser.add_argument("-id", "--displayID", help=" Display ID - default 1", type=int)
parser.add_argument("-o", "--order", help="Order to executute - default Insert text to display")

parser.add_argument("-fc","--fontcolor",help="color to display 1: red 2: green 3: yellow - default red", type=int) 
parser.add_argument("-s", "--speed",help="display speed, 0 -> 255", type=int) 
parser.add_argument("-m","--mode",help="display mode 01: shift left 02: Instant 03: shift up 05: scroll left", type=int)
parser.add_argument("-f", "--font",help="font to use :0 font8(5*7) 2 font16 3 font24 4 font32",type=int)


args = parser.parse_args()


if args.port:
	print "Port: ", args.port
	DisplayPort = args.port 
else:
	DisplayPort = "/dev/ttyUSB0" # default port

if args.displayID:
	DisplayID = args.displayID
else:
	DisplayID = 1	# default display ID

if args.order:
	DisplayOrder = args.order
else:
	DisplayOrder = 0x05 # default Download to RAM and display

if args.fontcolor:
	DisplayFontColor = args.fontcolor
else:
	DisplayFontColor = 1

if args.speed:
	DisplaySpeed = args.speed
else:
	if args.speed != 0:
		DisplaySpeed = 127
	else:
		DisplaySpeed = 0

if args.mode:
	DisplayMode = args.mode
else:
	DisplayMode = 2 # instant display

if args.font:
	DisplayFont = args.font
else:
	if args.font != 0:
		DisplayFont = 2 # use font16
	else:
		DisplayFont = 0

print"Order:     ",DisplayOrder
print"FontColor: ",DisplayFontColor
print"Speed:     ",DisplaySpeed
print"Mode:      ",DisplayMode
print"font:      ",DisplayFont

print args.texte

Start_code = chr(0xa5) +chr(0xed)
E_C_insert = chr(0x0d)+ chr(0x0a) 	# end code for insert

ser = serial.Serial (DisplayPort, 57600, timeout=0)

cmd_send_display = Start_code + chr(0x10) + chr(DisplayID) + chr(DisplayOrder) + chr(DisplayFontColor) + chr(DisplaySpeed) + chr(DisplayMode) + chr(DisplayFont)
cmd_send_display = cmd_send_display + args.texte
cmd_send_display = cmd_send_display + E_C_insert
verifCode=0
for i in range(1, len (cmd_send_display)):
	verifCode = verifCode + ord(cmd_send_display[i])

verif_high = (verifCode & 0xFF00)/0xFF
# remplace 0xa5 0xae 0xaa
if verif_high == 0xa5:
	verifcode_str = chr(0xaa) + chr (0x5)
elif verif_high == 0xae:
	verifcode_str = chr(0xaa) + chr (0xe)
elif verif_high == 0xaa:
	verifcode_str = chr(0xaa) + chr (0xa)
else:
	verifcode_str = chr(verif_high)
	
verif_low = verifCode & 0xFF
# remplace 0xa5 0xae 0xaa
if verif_low == 0xa5:
	verifcode_str = verifcode_str + chr(0xaa) + chr (0x5)
elif verif_low == 0xae:
	verifcode_str = verifcode_str + chr(0xaa) + chr (0xe)
elif verif_low == 0xaa:
	verifcode_str = verifcode_str + chr(0xaa) + chr (0xa)
else:
	verifcode_str = verifcode_str + chr(verif_low)



cmd_send_display = cmd_send_display + verifcode_str + chr (0xae)

print "----------------"

## print cmd_send_display
for i in range(0,len(cmd_send_display)):
	print hex(ord(cmd_send_display[i]))
	i = i +1

ser.open()
if ser.isOpen:
	print"send command"
	ser.write(cmd_send_display)
	ser.close
