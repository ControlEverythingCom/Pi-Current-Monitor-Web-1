#!/usr/bin/python

import smbus
import time
import sys

print "Content-Type: text/plain\r\n\r\n"

# Get I2C bus
bus = smbus.SMBus(1)

# PECMAC125A address, 0x2A(42)
# Command for reading device identification data
# 0x6A(106), 0x02(2), 0x00(0),0x00(0), 0x00(0) 0x00(0), 0xFE(254)
# Header byte-2, command-2, byte 3, 4, 5 and 6 are reserved, checksum
command2 = [0x6A, 0x02, 0x00, 0x00, 0x00, 0x00, 0xFE]
bus.write_i2c_block_data(0x2A, 0x92, command2)

time.sleep(0.5)

# PECMAC125A address, 0x2A(42)
# Read data back from 0x55(85), 3 bytes
# Type of Sensor, Maximum Current, No. of Channels
data = bus.read_i2c_block_data(0x2A, 0x55, 3)

# Convert the data
typeOfSensor = data[0]
maxCurrent = data[1]
noOfChannel = data[2]

# Output data to screen
#print "Type of Sensor : %d" %typeOfSensor
#print "Maximum Current : %d A" %maxCurrent
#print "No. of Channels : %d" %noOfChannel

# PECMAC125A address, 0x2A(42)
# Command for reading current
# 0x6A(106), 0x01(1), 0x01(1),0x0C(12), 0x00(0), 0x00(0) 0x0A(10)
# Header byte-2, command-1, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
command1 = [0x6A, 0x01, 0x01, 0x0C, 0x00, 0x00, 0x0A]       #all channels
command2 = [0x6A, 0x01, 0x01, 0x0B, 0x00, 0x00, 0x09]       #channels 1-11
command3 = [0x6A, 0x01, 0x02, 0x0C, 0x00, 0x00, 0x0B]       #channels 2-12
command4 = [0x6A, 0x01, 0x0C, 0x0C, 0x00, 0x00, 0x15]       #channel 12 only

calibrationRead = [0x6A,  0x03,  0x01,  0x0C, 0x00,  0x00, 0x0C]

bus.write_i2c_block_data(0x2A, 0x92, command1)

time.sleep(0.5)

# PECMAC125A address, 0x2A(42)
# Read data back from 0x55(85), No. of Channels * 3 bytes
# current MSB1, current MSB, current LSB
#data1 = bus.read_i2c_block_data(0x2A, 0x55, (noOfChannel*3)+1)
data1 = bus.read_i2c_block_data(0x2A, 0x55, 37)

readings = ""

print data1
sys.exit()

# Convert the data
for i in range(0, noOfChannel) :
    msb1 = data1[i * 3]
    msb = data1[1 + i * 3]
    lsb = data1[2 + i * 3]
    
    # Convert the data to ampere
    current = (msb1 * 65536 + msb * 256 + lsb) / 1000.0
    readings += str("%.3f" %current)
    readings += "|"

readings = readings[:-1]
print readings
    # Output data to screen
    #print "Channel no : %d " %(i + 1)
    #print "Current Value : %.3f A" %current