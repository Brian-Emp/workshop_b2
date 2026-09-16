import tkinter as tk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# 1. Initialisation du lecteur NFC
reader = SimpleMFRC522()

# 2. Création de l'interface
fenetre = tk.Tk()
fenetre.title("Portail Rick & Morty")
# Pour mettre en plein écran (retirez le # au début de la ligne suivante si vous le souhaitez)
# fenetre.attributes('-fullscreen', True) 
fenetre.geometry("800x480") # Taille par défaut

# Couleurs du thème
couleur_fond = "#0f171e" # Noir profond de l'espace
couleur_portail = "#39ff14" # Vert fluo du portail
couleur_rick = "#00bfff" # Bleu cyan
fenetre.configure(bg=couleur_fond)

# 3. Le texte affiché à l'écran
label_status = tk.Label(fenetre, text="Wubba Lubba Dub Dub!\nPrésente ton pass, Morty...", 
                        font=("Helvetica", 28, "bold"), fg=couleur_portail, bg=couleur_fond)
label_status.pack(expand=True)

# 4. La fonction magique (Non-bloquante)
def verifier_nfc():
    # read_no_block lit le lecteur sans figer la fenêtre
    id, text = reader.read_no_block()
    
    if id:
        # Un badge a été détecté ! L'interface réagit !
        print(f"Badge détecté: {id}")
        label_status.config(text=f"Portail ouvert !\nID Détecté : {id}", fg=couleur_rick)
        
        # On remet l'interface à zéro après 3 secondes (3000 ms)
        fenetre.after(3000, reset_interface)
    else:
        # Aucun badge, on revérifie dans 200 millisecondes
        fenetre.after(200, verifier_nfc)

def reset_interface():
    # Remet le texte initial en vert
    label_status.config(text="Wubba Lubba Dub Dub!\nPrésente ton pass, Morty...", fg=couleur_portail)
    # Relance la vérification
    fenetre.after(200, verifier_nfc)

# Bouton pour quitter (utile en plein écran)
btn_quit = tk.Button(fenetre, text="Fermer la dimension", command=fenetre.destroy, 
                     bg="#8b0000", fg="white", font=("Helvetica", 14))
btn_quit.pack(pady=20)

# 5. Lancement
try:
    # On lance la première vérification NFC juste après l'affichage
    fenetre.after(500, verifier_nfc)
    # On lance l'interface graphique
    fenetre.mainloop()
finally:
    # TRÈS IMPORTANT : libère les broches GPIO quand on ferme la fenêtre
    GPIO.cleanup()
