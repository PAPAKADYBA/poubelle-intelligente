#include <ESP32Servo.h>

// --- Broches ---
const int TRIG_NIVEAU = 5,  ECHO_NIVEAU = 18;
const int TRIG_MAIN   = 19, ECHO_MAIN   = 21;
const int PIN_SERVO   = 13;
const int PIN_LED     = 26;
const int PIN_BUZZER  = 27;

// --- Paramètres ---
const float HAUTEUR_TOTALE = 40.0;   // cm : profondeur de la poubelle vide
const float SEUIL_MAIN     = 20.0;   // cm : détection de la main
const float SEUIL_ALERTE   = 80.0;   // % : alerte de remplissage
const unsigned long DUREE_OUVERTURE = 3000;   // ms
const unsigned long PERIODE_MESURE  = 5000;   // ms (augmente pour la collecte réelle)

Servo servo;
unsigned long derniereMesure = 0;

float mesureDistance(int trig, int echo) {
  digitalWrite(trig, LOW);  delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duree = pulseIn(echo, HIGH, 30000);   // timeout 30 ms
  if (duree == 0) return -1;                 // pas d'écho
  return duree * 0.0343 / 2.0;               // cm
}

float calculNiveau(float distance) {
  float niveau = (HAUTEUR_TOTALE - distance) / HAUTEUR_TOTALE * 100.0;
  return constrain(niveau, 0, 100);
}

void ouvrirCouvercle() {
  servo.write(90);
  delay(DUREE_OUVERTURE);
  servo.write(0);
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_NIVEAU, OUTPUT); pinMode(ECHO_NIVEAU, INPUT);
  pinMode(TRIG_MAIN, OUTPUT);   pinMode(ECHO_MAIN, INPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  servo.attach(PIN_SERVO);
  servo.write(0);                       // couvercle fermé
  Serial.println("temps_ms,distance_cm,niveau_pct");
}

void loop() {
  // 1) Détection de la main -> ouverture
  float dMain = mesureDistance(TRIG_MAIN, ECHO_MAIN);
  if (dMain > 0 && dMain < SEUIL_MAIN) {
    ouvrirCouvercle();
  }

  // 2) Mesure périodique du niveau (couvercle fermé)
  if (millis() - derniereMesure >= PERIODE_MESURE) {
    derniereMesure = millis();
    float d = mesureDistance(TRIG_NIVEAU, ECHO_NIVEAU);
    if (d > 0) {
      float niveau = calculNiveau(d);
      Serial.printf("%lu,%.1f,%.1f\n", millis(), d, niveau);

      bool alerte = niveau >= SEUIL_ALERTE;
      digitalWrite(PIN_LED, alerte);
      if (alerte) tone(PIN_BUZZER, 1000); else noTone(PIN_BUZZER);
    }
  }
  delay(100);
}