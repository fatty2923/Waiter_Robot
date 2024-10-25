from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import D_MNSV7_X16
import time

# from LineFollowerRobot import client
client = ModbusClient(method='rtu', port="COM10", baudrate=115200, timeout=1)

sensor = D_MNSV7_X16.Magnetic_Line_Sensor(client)

while True:
    try:
        arr = sensor.get_analog_output()
        print(arr)
        time.sleep(0.5)

    except KeyboardInterrupt:
        break
