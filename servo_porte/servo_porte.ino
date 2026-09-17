#include <Servo.h>
Servo s1;
Servo s2;

const int servo_pin = 9;
const int servo_pin2 = 10;
int angle_ouvert = 10;
int angle_ferme = 170;

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

//exemple de loop
void loop() {
  ouverture_controler(angle_ferme, angle_ouvert, 30);
  delay(3000);
  ouverture_controler(angle_ouvert, angle_ferme, 30);
  delay(3000);
}