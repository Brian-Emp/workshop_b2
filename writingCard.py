import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Place your card to read/write data...")
    
    
    uid = reader.read_id()
    print(f"Badge détecté, ID : {uid}")
    

    if uid == 49538561101:
        data_to_write = "M. Larbin"
    elif uid == 51264386313: 
        data_to_write = "Rick et Morty"
    elif uid == 1081687635404: 
            data_to_write = "M. Pickle Rick"
    elif uid == 119881430522: 
            data_to_write = "Robot beurre"
    elif uid == 323427398836: 
            data_to_write = "Jerry"
    else:
        data_to_write = input("Entrez le nom du propriétaire pour le badge : ")
        
    print("Laissez le badge sur le lecteur pour l'écriture...")
    reader.write(data_to_write)
    print(f"Succès ! '{data_to_write}' a été écrit sur la carte.")

finally:
    GPIO.cleanup()
