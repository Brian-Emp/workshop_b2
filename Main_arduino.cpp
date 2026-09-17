#include <Servo.h>
Servo s1;
Servo s2;

const int servo_pin = 9;
const int servo_pin2 = 10;
int angle_ouvert = 180;
int angle_ferme = 0;

void ouvrir() {
  s1.write(angle_ouvert);
  s2.write(180 - angle_ouvert);
}

void fermer() {
  s1.write(angle_ferme);
  s2.write(180 - angle_ferme);
}

void setup() {
  s1.attach(servo_pin);
  s2.attach(servo_pin2);

  fermer(); 
}

void ouverture_controler(int depart, int arrive, int vitesse) {
  int pas = arrive > depart ? 1 : -1;
  for (int a = depart; a != arrive; a += pas) {
    s1.write(a);
    s2.write(180 - a);
    delay(vitesse);
  }
  s1.write(arrive);
  s2.write(180 - arrive);
}

//exemple test
void loop() {
  ouverture_controler(0, 120, 20);
  delay(5000);
  ouverture_controler(120, 0, 20);
}

void traiterCommande(const String &cmd) {
  if (cmd == "OPEN")            ouvrir();
  else if (cmd == "CLOSE")      fermer();
  else if (cmd == "PING")       Serial.println("PONG");
  else                          Serial.println("ERR");
}