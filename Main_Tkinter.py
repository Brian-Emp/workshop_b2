import tkinter as tk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import serial 

reader = SimpleMFRC522()

try:
    # C'est cette ligne qui ouvre physiquement le port USB
    arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except serial.SerialException:
    print("Attention : Arduino non connecté ou port incorrect")
    arduino = None

fenetre = tk.Tk()
fenetre.title("Portail Rick & Morty")
fenetre.attributes('-fullscreen', True) 
fenetre.geometry("800x480") 


couleur_fond = "#0f171e" # Noir
couleur_portail = "#39ff14" # Vert fluo du portail
couleur_rick = "#00bfff" # Bleu cyan
fenetre.configure(bg=couleur_fond)

# 3. Le texte affiché à l'écran
label_status = tk.Label(fenetre, text="Bienvenu !\nPour rechercher une personne, \nveuillez approchez son badge...", 
font=("Helvetica", 28, "bold"), fg=couleur_portail, bg=couleur_fond)
label_status.pack(expand=True)

def lancer_vidéo_Larbin():
    chemin_video = "/home/bob/nfc-env/workshop_b2/Animation_720p_Pickle_Rick.mov"
    subprocess.run(["cvlc", "--fullscreen", "--play-and-exit", "--no-video-title-show", chemin_video])
    reset_interface()

def lancer_vidéo_Pickle_Rick():
    chemin_video = "/home/bob/nfc-env/workshop_b2/M.Larbin_720p_animation.mov"
    subprocess.run(["cvlc", "--fullscreen", "--play-and-exit", "--no-video-title-show", chemin_video])
    reset_interface()

def verifier_nfc():
    id, text = reader.read_no_block()
    
    if id == 481729585450:
        if arduino:
            arduino.write(b"OPEN\n")

        label_status.config(text="Badge détecté : " + text, fg=couleur_rick)
        fenetre.update()  
        lancer_vidéo_Larbin()
       
        arduino.write(b"CLOSE\n")   
        fenetre.after(6000, verifier_nfc)

    elif id == 145033995888:
        if arduino:
            arduino.write(b"OPEN\n")

        label_status.config(text="Badge détecté : " + text, fg=couleur_rick)
        fenetre.update()  
        lancer_vidéo_Pickle_Rick()
        arduino.write(b"CLOSE\n")   
        fenetre.after(6000, verifier_nfc)


    elif id is not None:
        if arduino:
            arduino.write(b"OPEN\n")
        label_status.config(text="Badge inconnu, \nréessaye avec un autre badge \nou configure en un nouveau !", fg="red")
        fenetre.update()
        arduino.write(b"CLOSE\n") 
        fenetre.after(6000, reset_interface)
        
    else:
        fenetre.after(6000, verifier_nfc)

def reset_interface():
    label_status.config(text="Présente un autre badge", fg=couleur_portail)
    fenetre.after(4000, verifier_nfc)


btn_quit = tk.Button(fenetre, text="Fermer la dimension", command=fenetre.destroy, 
                     bg="#8b0000", fg="white", font=("Helvetica", 14))
btn_quit.pack(pady=20)


try:
    fenetre.after(500, verifier_nfc)
    fenetre.mainloop()
finally:
    GPIO.cleanup()
