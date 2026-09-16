import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try: 
    data_to_write = "A changer lors de la prod"
    print("Place your card to write data...")
    reader.write(data_to_write)
    print("Data written to card successfully!")
finally:
    GPIO.cleanup()
