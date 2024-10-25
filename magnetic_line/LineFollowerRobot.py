from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from array import array
# import ZLAC8015D
import D_MNSV7_X16
import time

## Values of 16 pins in magnetic line sensor
pin_values = array('B', [0] * 16)    # Analog values (each is 1 byte)
channels_value = 0xffff                       # Digital value (16 bit - 16 channels: 0-off, 1-on)

# We will be using 2 port: 1 for driver control only, 1 for sensors (rs485-multidrop)
# # client1 for ZLAC8015D control port
# client1 = ModbusClient(method='rtu', port="COM10", baudrate=115200, timeout=1)
# client2 for D_MNSV7_X16 control port
client2 = ModbusClient(method='rtu', port="COM9", baudrate=115200, timeout=1)

# # Initialize dual servo motor driver
# motors = ZLAC8015D.Controller(client1)
# Initialize magnetic line sensor
sensor = D_MNSV7_X16.Magnetic_Line_Sensor(client2)

# ## Initialize RPM control mode (3) for driver
# motors.disable_motor()
# motors.set_accel_time(500, 500)
# motors.set_decel_time(500, 500)
# motors.set_mode(3)
# motors.enable_motor()
# # cmds for speed each wheel: same sign is forward/backward motion, for now...
# cmds = [20, -20]

def get_position_value():
    global pin_values
    pin_values = sensor.get_analog_output()

    # Calculate the weighted sum and total sum of sensor values
    weighted_sum = sum(i * value for i, value in enumerate(pin_values))
    total_sum = sum(pin_values)

    # Avoid division by zero if no sensor is activated
    if total_sum == 0:
        return None  # No line detected

    # Calculate the position as a weighted average
    position = weighted_sum / total_sum
    return position

max_pos = 0
min_pos = 9999
last_time = time.time()
while time:
    position = get_position_value()
    if max_pos < position: max_pos = position
    if min_pos > position: min_pos = position
    print(position)
    time.sleep(0.05)

    if time.time() - last_time > 300:
        break

print("Max position: {:.f}".format(max_pos))
print("Min position: {:.f}".format(min_pos))




