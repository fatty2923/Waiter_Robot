from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import ZLAC8015D
import time

# from LineFollowerRobot import client
client = ModbusClient(method='rtu', port="COM10", baudrate=115200, timeout=1)
motors = ZLAC8015D.Controller(client)

motors.disable_motor()
motors.set_accel_time(500, 500)
motors.set_decel_time(500, 500)

motors.set_mode(3)
motors.enable_motor()
cmds = [20, -20]

motors.set_rpm(cmds[0], cmds[1])

time.sleep(6)
print("Stop")
motors.stop()
time.sleep(10)
motors.enable_motor()
motors.set_rpm(cmds[0], cmds[1])
time.sleep(6)
print("Stop")
motors.stop()
time.sleep(10)
while True:
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        motors.disable_motor()