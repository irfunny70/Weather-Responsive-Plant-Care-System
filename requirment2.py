import time
import RPi.GPIO as GPIO
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# --- Pin Setup ---
SERVO_PIN = 17
BUTTON_PIN = 27
LDR_PIN = 13  # Digital LDR input (0 = light, 1 = dark)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LDR_PIN, GPIO.IN)

# --- Servo Setup ---
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
servo.start(0)

def set_valve(open_valve):
    if open_valve:
        print("Opening valve...")
        servo.ChangeDutyCycle(7)  # Open
    else:
        print("Closing valve...")
        servo.ChangeDutyCycle(2)  # Close
    time.sleep(1)
    servo.ChangeDutyCycle(0)

# --- OLED Setup ---
WIDTH = 128
HEIGHT = 64
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.show()
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def display_oled(temp, hum, valve_open, mode):
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw.text((0, 0), f"Mode: {mode}", font=font, fill=255)
    draw.text((0, 15), f"Temp: {temp:.1f} C", font=font, fill=255)
    draw.text((0, 30), f"Humidity: {hum:.1f} %", font=font, fill=255)
    draw.text((0, 45), f"Valve: {'OPEN' if valve_open else 'CLOSED'}", font=font, fill=255)
    oled.image(image)
    oled.show()

def get_manual_input():
    try:
        temp = float(input("Enter temperature (°C): "))
        hum = float(input("Enter humidity (%): "))
        return temp, hum
    except ValueError:
        print("Invalid input. Using fallback values.")
        return 32.0, 70.0

# --- Main Loop ---
try:
    valve_open = False

    while True:
        is_day = GPIO.input(LDR_PIN) == 0  # 0 = light, 1 = dark

        if is_day:
            print("Daytime: Auto watering mode")
            mode = "AUTO"
            temp, hum = get_manual_input()

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

            display_oled(temp, hum, valve_open, mode)

        else:
            print("Nighttime: Manual watering mode")
            mode = "MANUAL"
            button_pressed = GPIO.input(BUTTON_PIN) == GPIO.HIGH
            display_oled(0, 0, valve_open, mode)

            if button_pressed:
                print("Button pressed: watering")
                set_valve(True)
                time.sleep(2)
                set_valve(False)

        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    servo.stop()
    GPIO.cleanup()
    oled.fill(0)
    oled.show()
