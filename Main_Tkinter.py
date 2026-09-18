import tkinter as tk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import serial
import time

reader = SimpleMFRC522()

# --- Connexion a l'Arduino -------------------------------------------
try:
    arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    time.sleep(2)          # l'Arduino redemarre a l'ouverture du port
    print("Arduino connecte")
except Exception as e:
    arduino = None         # l'interface tourne quand meme, sans les servos
    print(f"Arduino absent : {e}")


def ouvrir():
    if arduino:
        arduino.write(b"OPEN\n")


def fermer():
    if arduino:
        arduino.write(b"CLOSE\n")


fenetre = tk.Tk()
fenetre.title("Portail Rick & Morty")
fenetre.attributes('-fullscreen', True)
fenetre.geometry("800x480")

couleur_fond = "#0f171e"
couleur_portail = "#39ff14"
couleur_rick = "#00bfff"
fenetre.configure(bg=couleur_fond)

label_status = tk.Label(
    fenetre,
    text="Bienvenue !\nPour rechercher une personne,\nveuillez approcher son badge...",
    font=("Helvetica", 28, "bold"), fg=couleur_portail, bg=couleur_fond)
label_status.pack(expand=True)

DOSSIER = "/home/bob/nfc-env/workshop_b2/"

# UID -> (nom affiche, fichier video)
# Mettez les NOMS EXACTS tels qu'ils sont écrits dans votre dossier (attention aux majuscules)
BADGES = {
    1081687635404: ("M. Pickle Rick", "Animation_720p_Pickle_Rick.mov"),
    49538561101: ("M. Larbin",      "Animation_720p_Monsieur_Larbin.mov"), # À vérifier
    51264386313: ("Rick et Morty", "Animation_720p_Rick_Morty.mov"), # Corrigé
    119881430522: ("Robot beurre", "Animation_720p_Robot_Beurre.mov"),
    323427398836: ("Jerry", "Animation_720p_Jerry.mov")
}

def jouer_sequence(nom, video):
    ouvrir() 
    
    # On met à jour l'interface immédiatement
    label_status.config(text=f"Badge détecté : {nom}\nOuverture en cours...", fg=couleur_rick)
    
    # Fonction locale qui sera déclenchée après l'attente
    def lancer_vlc():
        try:
            subprocess.run(["cvlc", "--fullscreen", "--play-and-exit",
                            "--no-video-title-show", DOSSIER + video])
        finally:
            fermer()           
        reset_interface()


    # Tkinter attend 2000 millisecondes (2 secondes) sans figer, puis lance VLC
    fenetre.after(2000, lancer_vlc)


def verifier_nfc():
    id, text = reader.read_no_block()

    if id in BADGES:
        nom, video = BADGES[id]
        jouer_sequence(nom, video)

    elif id:
        label_status.config(
            text="Badge inconnu,\nréessaye avec un autre badge\nou configure-en un nouveau !",
            fg="red")
        fenetre.update()
        fenetre.after(2000, reset_interface)

    else:
        fenetre.after(200, verifier_nfc)


def reset_interface():
    label_status.config(text="Présente un autre badge", fg=couleur_portail)
    fenetre.after(200, verifier_nfc)


btn_quit = tk.Button(fenetre, text="Fermer la dimension", command=fenetre.destroy,
                     bg="#8b0000", fg="white", font=("Helvetica", 14))
btn_quit.pack(pady=20)

try:
    fenetre.after(500, verifier_nfc)
    fenetre.mainloop()
finally:
    if arduino:
        arduino.close()
    GPIO.cleanup()