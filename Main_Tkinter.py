import tkinter as tk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess


reader = SimpleMFRC522()

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

def verifier_nfc():
    id, text = reader.read_no_block()
    
    if id == 481729585450:
        print ("Badge détecté : M. Larbin")

        chemin_video = "/home/bob/nfc-env/Animation_720p_Pickle_Rick.mov"
        subprocess.run(["cvlc", "--fullscreen", "--play-and-exit", "--no-video-title-show", chemin_video])
        fenetre.after(1000, verifier_nfc)
        
    elif id == 145033995888:
        print ("Badge détecté : M. Pickle Rick")

        chemin_video = "/home/bob/nfc-env/M.Larbin_720p_animation.mov"
        subprocess.run(["cvlc", "--fullscreen", "--play-and-exit", "--no-video-title-show", chemin_video])
        fenetre.after(1000, verifier_nfc)

    elif id:
        print(f"Badge inconnu détecté : {id}")
        fenetre.after(2000, verifier_nfc)
        
    else:
        fenetre.after(200, verifier_nfc)

def reset_interface():
    label_status.config(text="Présente un autre pass", fg=couleur_portail)
    fenetre.after(200, verifier_nfc)


btn_quit = tk.Button(fenetre, text="Fermer la dimension", command=fenetre.destroy, 
                     bg="#8b0000", fg="white", font=("Helvetica", 14))
btn_quit.pack(pady=20)


try:
    fenetre.after(500, verifier_nfc)
    fenetre.mainloop()
finally:
    GPIO.cleanup()
