import time
import RPi.GPIO as GPIO
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# --- Servo Setup ---
SERVO_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)

# --- OLED Setup with PIL ---
WIDTH = 128
HEIGHT = 64
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.show()

# PIL image buffer setup
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# --- Valve Control ---
def set_valve(open_valve):
    if open_valve:
        print("Opening valve...")
        servo.ChangeDutyCycle(7)  # Adjust for "open" position
    else:
        print("Closing valve...")
        servo.ChangeDutyCycle(2)  # Adjust for "closed" position
    time.sleep(1)
    servo.ChangeDutyCycle(0)

# --- Manual Temp & Humidity Input ---
def get_manual_input():
    try:
        temp = float(input("Enter temperature (°C): "))
        hum = float(input("Enter humidity (%): "))
        return temp, hum
    except ValueError:
        print("Invalid input. Using fallback values.")
        return 32.0, 70.0

# --- OLED Display ---
def display_oled(temp, hum, valve_open):
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw.text((0, 0), f"Temp: {temp:.1f} C", font=font, fill=255)
    draw.text((0, 15), f"Humidity: {hum:.1f} %", font=font, fill=255)
    draw.text((0, 30), f"Valve: {'OPEN' if valve_open else 'CLOSED'}", font=font, fill=255)
    oled.image(image)
    oled.show()

# --- Main Loop ---
try:
    valve_open = False

    while True:
        temp, hum = get_manual_input()
        print(f"Temp: {temp}C, Humidity: {hum}%")

        if temp >= 35 and hum >= 90:
            if not valve_open:
                set_valve(True)
                valve_open = True
        elif temp <= 32 and hum <= 70:
            if valve_open:
                set_valve(False)
                valve_open = False
        else:
            print("No change in valve state.")

        display_oled(temp, hum, valve_open)
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    servo.stop()
    GPIO.cleanup()
    oled.fill(0)
    oled.show()
