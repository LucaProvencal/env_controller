import time
import BlynkLib
import board
import busio
import adafruit_scd4x
import os
import RPi.GPIO as GPIO

BLYNK_AUTH_TOKEN = os.environ["BLYNK_AUTH_TOKEN"]
BLYNK_INTERVAL = 120 # seconds

# Virtual Blynk pins
V_TEMP = 0
V_RH = 1
V_CO2 = 2

FAN_PIN = 17 # fan relay signal GPIO pin
HUMIDIFIER_PIN = 4  # humidifier relay signal GPIO pin

HUMIDITY_HIGH = 92 # %
HUMIDITY_LOW = 81 # %

FAN_INTERVAL = 60 * 20 # seconds
FAN_RUN_DURATION = 60 * 5 # seconds
CO2_HIGH = 500 # %

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(HUMIDIFIER_PIN, GPIO.OUT)

GPIO.output(FAN_PIN, GPIO.LOW) # set fan off
GPIO.output(HUMIDIFIER_PIN, GPIO.LOW) # set humidifier off

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server="blynk.cloud", port=80)

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize SCD41 sensor
scd41 = adafruit_scd4x.SCD4X(i2c)
scd41.start_periodic_measurement()

print("Waiting for first measurement...")

last_blynk_update = time.time()
last_fan_interval_start_time = 0
fan_off_time = 0

while True:
    blynk.run()
    
    if scd41.data_ready:
        co2 = scd41.CO2 # ppm
        temp_c = scd41.temperature  # °C
        temp_f = (temp_c * 9 / 5) + 32  # Convert to °F
        rh = scd41.relative_humidity # %
        
        if rh is not None:
            if rh > HUMIDITY_HIGH:
                GPIO.output(HUMIDIFIER_PIN, GPIO.LOW)
                print("Relay OFF (Humidity too high)")

            elif rh < HUMIDITY_LOW:
                GPIO.output(HUMIDIFIER_PIN, GPIO.HIGH)
                print("Relay ON (Humidity too low)")
                
        else:
            print("Failed to read humidity sensor!")
            
        if co2 is not None:
            if time.time() - last_fan_interval_start_time >= FAN_INTERVAL:
                last_fan_interval_start_time = time.time()
                fan_off_time = last_fan_interval_start_time + FAN_RUN_DURATION
            
            if fan_off_time < time.time():
                GPIO.output(FAN_PIN, GPIO.LOW)
                print("Fan OFF (run duration reached)")
            else:
                GPIO.output(FAN_PIN, GPIO.HIGH)
                print("Fan ON (run duration not reached)")

            
        else:
            print("Failed to read co2!")

        print(f"CO2: {co2} ppm")
        print(f"Temperature: {temp_f} °C")
        print(f"Humidity: {rh:.2f} %")
        print("----------------------")
        
        if time.time() - last_blynk_update >= BLYNK_INTERVAL:
            blynk.virtual_write(V_TEMP, temp_f)
            blynk.virtual_write(V_RH, rh)
            blynk.virtual_write(V_CO2, co2)
            print("Data sent to Blynk")
            last_blynk_update = time.time()
    else:
        print("Waiting for data...")

    time.sleep(5)
