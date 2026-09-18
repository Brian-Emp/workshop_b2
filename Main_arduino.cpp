#include <Servo.h>

// ---------- Paramètres à ajuster ----------
const int SERVO_PIN_1 = 9;
const int SERVO_PIN_2 = 10;

const int ANGLE_OUVERT = 10;
const int ANGLE_FERME  = 170;

const int VITESSE = 20;                        // ms entre chaque degré
const unsigned long DUREE_OUVERTURE = 8000;    // ms porte ouverte
// ------------------------------------------

Servo s1;
Servo s2;

int angleActuel = ANGLE_FERME;
bool porteOuverte = false;
unsigned long instantOuverture = 0;

String ligne = "";

// Déplacement progressif, bloquant mais court (~3 s max)
void bouger(int arrivee) {
  int pas = (arrivee > angleActuel) ? 1 : -1;
  while (angleActuel != arrivee) {
    angleActuel += pas;
    s1.write(angleActuel);
    s2.write(180 - angleActuel);
    delay(VITESSE);
  }
}

void ouvrir() {
  bouger(ANGLE_OUVERT);
  porteOuverte = true;
  instantOuverture = millis();
  Serial.println("OK OPEN");
}

void fermer() {
  bouger(ANGLE_FERME);
  porteOuverte = false;
  Serial.println("OK CLOSE");
}

void traiterCommande(const String &cmd) {
  if (cmd == "OPEN") {
    if (porteOuverte) {
      instantOuverture = millis();   // badge repassé : on prolonge
      Serial.println("OK OPEN");
    } else {
      ouvrir();
    }
  }
  else if (cmd == "CLOSE") fermer();
  else if (cmd == "PING")  Serial.println("PONG");
  else                     Serial.println("ERR");
}

void setup() {
  Serial.begin(115200);

  s1.attach(SERVO_PIN_1);
  s2.attach(SERVO_PIN_2);

  // état connu au démarrage, sans animation
  angleActuel = ANGLE_FERME;
  s1.write(ANGLE_FERME);
  s2.write(180 - ANGLE_FERME);
  porteOuverte = false;

  Serial.println("READY");
}

void loop() {
  // 1) Lecture non bloquante du port série
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      ligne.trim();
      if (ligne.length() > 0) {
        traiterCommande(ligne);
        ligne = "";
      }
    } else if (ligne.length() < 32) {
      ligne += c;
    }
  }

  // 2) Refermeture automatique
  if (porteOuverte && millis() - instantOuverture >= DUREE_OUVERTURE) {
    fermer();
  }
}