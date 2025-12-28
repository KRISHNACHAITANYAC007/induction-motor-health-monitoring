import time
import math
import serial
import spidev
import board
import adafruit_dht
import smbus
import requests
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

TS_API_KEY = "G4YUK8LGZVNJE0LC"
TS_URL = "https://api.thingspeak.com/update"

ser = serial.Serial("/dev/serial0", 9600, timeout=1)
time.sleep(2)

dht = adafruit_dht.DHT11(board.D4)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((r[1] & 3) << 8) + r[2]

def adc_to_current(adc):
    voltage = adc * (3.3 / 1023.0)
    offset = 2.5
    sensitivity = 0.185  # ACS712 5A
    return round((voltage - offset)/sensitivity, 2)

bus = smbus.SMBus(1)
ADXL_ADDR = 0x53
try:
    bus.write_byte_data(ADXL_ADDR, 0x2D, 0x08)  
except Exception as e:
    print("ADXL345 init error:", e)

def read_accel():
    try:
        data = bus.read_i2c_block_data(ADXL_ADDR, 0x32, 6)
        x = int.from_bytes(data[0:2], byteorder='little', signed=True) * 0.004
        y = int.from_bytes(data[2:4], byteorder='little', signed=True) * 0.004
        z = int.from_bytes(data[4:6], byteorder='little', signed=True) * 0.004
        acc = math.sqrt(x*x + y*y + z*z)
        return round(acc, 2)
    except:
        return 0.0

factory = PiGPIOFactory()
servo = AngularServo(18, min_angle=-90, max_angle=90, pin_factory=factory)

motor_status = 1
last_ts = 0

try:
    while True:
        try:
            temp = dht.temperature
        except:
            temp = 0
        adc_val = read_adc(0)
        current = adc_to_current(adc_val)
        acc = read_accel()
        lcd_line = f"T{temp}C{current}A{acc}M{motor_status}\n"
        ser.write(lcd_line.encode())
        now = time.time()
        if now - last_ts >= 15:
            payload = {
                "api_key": TS_API_KEY,
                "field1": temp,
                "field2": current,
                "field3": acc,
                "field4": motor_status
            }
            try:
                r = requests.post(TS_URL, data=payload, timeout=10)
                print("ThingSpeak Response:", r.text)
            except Exception as e:
                print("ThingSpeak Error:", e)
            last_ts = now
        print(f"T={temp}C, Curr={current}A, Acc={acc}, Motor={motor_status}")
        servo.angle = 0
        sleep(1)
        servo.angle = -90
        sleep(1)
        servo.angle = 90
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    print("Cleaning up...")
    spi.close()
    ser.close()
    servo.close()
