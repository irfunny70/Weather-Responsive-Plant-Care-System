import time
import board
import busio
import RPi.GPIO as GPIO
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# --- GPIO Pins ---
TRIG = 23
ECHO = 24
BUZZER_PIN = 22
WATER_LEVEL_THRESHOLD = 10  # cm

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# --- OLED Setup ---
WIDTH = 128
HEIGHT = 64
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Clear OLED display
oled.fill(0)
oled.show()

# Create a blank image for drawing
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# --- Function to get distance from ultrasonic sensor ---
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        if time.time() > timeout:
            return -1  # Timeout

    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if time.time() > timeout:
            return -1  # Timeout

    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2  # cm
    return distance

# --- Main Loop ---
try:
    while True:
        dist = get_distance()

        if dist == -1:
            display_text = "Sensor error"
            print("Ultrasonic sensor timeout")
            GPIO.output(BUZZER_PIN, False)  # Turn off buzzer if error
        else:
            display_text = f"Water Level:\n{dist:.1f} cm"
            print(display_text)

            # Buzzer alert if water level is too low
            if dist > WATER_LEVEL_THRESHOLD:
                GPIO.output(BUZZER_PIN, True)
            else:
                GPIO.output(BUZZER_PIN, False)

        # Clear and draw new display content
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        draw.text((0, 0), display_text, font=font, fill=255)
        oled.image(image)
        oled.show()

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    GPIO.cleanup()
    oled.fill(0)
    oled.show()
