from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import ZLAC8015D
import time

client = ModbusClient(method='rtu', port="COM10", baudrate=115200, timeout=1)
motors = ZLAC8015D.Controller(client)

motors.disable_motor()

motors.set_accel_time(6000,6000)
motors.set_decel_time(1000,1000)
motors.set_maxRPM_pos(40, 40)

motors.set_mode(1)
motors.set_position_async_control()
motors.enable_motor()
motors.set_relative_angle(361,361)
motors.move_left_wheel()
motors.move_right_wheel()

while True:
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        motors.disable_motor()
        break
