import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Place your card to read/write data...")
    
    
    uid = reader.read_id()
    print(f"Badge détecté, ID : {uid}")
    

    if uid == 481729585450:
        data_to_write = "M. Larbin"
    elif uid == 145033995888: 
        data_to_write = "M. Pickle Rick"
    else:
        data_to_write = input("Entrez le nom du propriétaire pour le badge : ")
        
    print("Laissez le badge sur le lecteur pour l'écriture...")
    reader.write(data_to_write)
    print(f"Succès ! '{data_to_write}' a été écrit sur la carte.")

finally:
    GPIO.cleanup()
