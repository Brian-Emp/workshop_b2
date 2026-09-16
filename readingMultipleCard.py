import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

reader = SimpleMFRC522()

try:
    while True:
        print("Place your card to read data...")
        id, text = reader.read()
        if id is not None:
            print(f"Card ID: {id}")
            print(f"Data on card: {text}")
            sleep(3)

except KeyboardInterrupt:
    print("Fermeture du programme.")
finally:
    GPIO.cleanup()