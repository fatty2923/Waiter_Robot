import D_MNSV7_X16
from LineFollowerRobot import client

sensor = D_MNSV7_X16.Magnetic_Line_Sensor(client)

sensor.set_ID(2)