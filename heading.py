import smbus
import os
import time
import math


def get_magnetometer():
    # activate Magnetometer (address, ctrl_reg, value)
    bus.write_byte_data(0x1e, 0x20, 0x10) 
    bus.write_byte_data(0x1e, 0x21, 0x00)
    bus.write_byte_data(0x1e, 0x22, 0x00) 
    time.sleep(0.01)
    readings_m = dict()
    # Read back the Magnetometer values (addr, data_reg)
    readings_m["x0"] = bus.read_byte_data(0x1e, 0x28)
    readings_m["x1"] = bus.read_byte_data(0x1e, 0x29)
    readings_m["y0"] = bus.read_byte_data(0x1e, 0x2a)
    readings_m["y1"] = bus.read_byte_data(0x1e, 0x2b)
    readings_m["z0"] = bus.read_byte_data(0x1e, 0x2c)
    readings_m["z1"] = bus.read_byte_data(0x1e, 0x2d)

    return(readings_m)


def get_gyro():
    # activate gyro (address, ctrl_reg, value)
    bus.write_byte_data(0x6b, 0x16, 0x38)
    bus.write_byte_data(0x6b, 0x11, 0x40)
    time.sleep(0.01)
    readings_g = dict()
    # Read back the gyro values (addr, data_reg)
    readings_g["x0"] = bus.read_byte_data(0x6b, 0x22)
    readings_g["x1"] = bus.read_byte_data(0x6b, 0x23)

    readings_g["y0"] = bus.read_byte_data(0x6b, 0x24)

    readings_g["y1"] = bus.read_byte_data(0x6b, 0x25)

    readings_g["z0"] = bus.read_byte_data(0x6b, 0x26)
    readings_g["z1"] = bus.read_byte_data(0x6b, 0x27)
    return(readings_g)


def get_accel():
    # activate accel (address, ctrl_reg, value)
    bus.write_byte_data(0x6b, 0x18, 0x38) # set freq /dps
    bus.write_byte_data(0x6b, 0x10, 0x40) # turn 3d accel on
    time.sleep(0.01)
    readings_a = dict()
    # Read back the gyro values (addr, data_reg)
    readings_a["x0"] = bus.read_byte_data(0x6b, 0x28)
    readings_a["x1"] = bus.read_byte_data(0x6b, 0x29)

    readings_a["y0"] = bus.read_byte_data(0x6b, 0x2A)
    readings_a["y1"] = bus.read_byte_data(0x6b, 0x2B)

    readings_a["z0"] = bus.read_byte_data(0x6b, 0x2C)
    readings_a["z1"] = bus.read_byte_data(0x6b, 0x2D)
    return(readings_a)



   
## Maintry: os.chdir("/usbdrv/data/sensor_data")
#except: os.mkdir("/usbdrv/data/sensor_data")
# confirm which when running i2c-detect second parameterbus = smbus.SMBus(1)

# wait for the pin to go high


bus = smbus.SMBus(1)

while True:


    reading = get_magnetometer()

    x = reading['x1']
    y = reading['y1']
    z = reading['z1']  

    heading = math.atan2(y, x) 
        
    #Due to declination check for >360 degree
    if(heading > 2*math.pi):
            heading = heading - 2*math.pi

    #check for sign
    if(heading < 0):
            heading = heading + 2*math.pi

    #convert into angle
    heading_angle = int(heading * 180/math.pi)

    print ("Heading Angle =" +str(heading_angle))
    time.sleep(1)


