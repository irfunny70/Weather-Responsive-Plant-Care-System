import time
import RPi.GPIO as GPIO

# --- Pin Definitions ---
LDR_PIN = 13
BUTTON_PIN = 27
SERVO_PIN = 17

# --- GPIO Setup ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# --- Servo Setup ---
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)

# --- Helper Function to Set Servo Angle ---
def set_angle(angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

# --- Watering Function ---
def water_plant():
    print("Watering...")
    set_angle(90)  # Open valve
    time.sleep(2)
    set_angle(0)   # Close valve
    print("Watering complete.")

# --- Main Loop ---
try:
    while True:
        is_day = GPIO.input(LDR_PIN) == 0  # 0 = light, 1 = dark
        button_pressed = GPIO.input(BUTTON_PIN) == GPIO.HIGH

        if is_day:
            print("Daytime: auto watering")
            water_plant()
        elif not is_day and button_pressed:
            print("Night: manual watering")
            water_plant()
        else:
            print("Night: button not pressed")

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    servo.stop()
    GPIO.cleanup()
