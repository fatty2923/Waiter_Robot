from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import ZLAC8015D
import time

db = 25.5 # cm, Khoang cach 2 banh xe
Rw = 6.5 # cm, Ban kinh banh xe
t1 = 0.5 # thoi gian tang toc
t2 = 0.5 # thoi gian giam toc
# alpha = 0.2 # sai so thoi gian giam toc cho stop()
RPM = int(input("Enter RPM for 2 wheels: "))
theta = float(input("Enter turning angle: "))

t3 = (db * theta) / (12 * RPM * Rw) - (t1 +t2) / 2

client = ModbusClient(method='rtu', port="COM10", baudrate=115200, timeout=1)
motors = ZLAC8015D.Controller(client)

motors.disable_motor()

motors.set_accel_time(t1*1000, t1*1000)
motors.set_decel_time(t2*1000, t2*1000)
# Function stop() is affected by deceleration time
# Function disable_motor() is not

motors.set_mode(3)
motors.enable_motor()

# cmds = [140, 170]
# cmds = [100, 50]
# cmds = [150, -100]
# cmds = [-15, -15]
time.sleep(5)
while True:
    try:
        motors.set_rpm(RPM, RPM)
        time.sleep(t1 + t3)
        motors.stop()
        time.sleep(10)
        motors.enable_motor()
    except KeyboardInterrupt:
        motors.disable_motor()
        break
