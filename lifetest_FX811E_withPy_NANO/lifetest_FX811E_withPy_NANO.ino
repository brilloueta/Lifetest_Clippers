#include "Arduino.h"
#include "Wire.h"
#include "core.h"
#include "linker_oled.h"

int relais1 = 2;                        // Relais 1 sur pin 2 - Tondeuse 1
int relais2 = 3;                        // Relais 2 sur pin 3 - Tondeuse 2
int relais3 = 4;                        // Relais 3 sur pin 4 - Tondeuse 3
int relais4 = 5;                        // Relais 4 sur pin 5 - Tondeuse 4
int relais5 = 6;                        // Relais 5 sur pin 6 - Tondeuse 5
int relais6 = 7;                        // Relais 6 sur pin 7 - Tondeuse 6
int relais7 = 8;                        // Relais 7 sur pin 8
int relais8 = 9;                        // Relais 8 sur pin 9 - Charge tondeuses
int bouton = 10;                        // Bouton sur pin 10
int fin_prog = 11;                      // signal fin de prog sur pin 11
int led_temoin = 12;
unsigned int y=30867;                   // y=nombre de cycles à l'origine

void setup() 
{
  pinMode(relais1, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais1, HIGH);           // Déclaration des états des relais
  pinMode(relais2, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais2, HIGH);           // Déclaration des états des relais
  pinMode(relais3, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais3, HIGH);           // Déclaration des états des relais
  pinMode(relais4, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais4, HIGH);           // Déclaration des états des relais
  pinMode(relais5, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais5, HIGH);           // Déclaration des états des relais
  pinMode(relais6, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais6, HIGH);           // Déclaration des états des relais
  pinMode(relais7, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais7, HIGH);           // Déclaration des états des relais
  pinMode(relais8, OUTPUT);              // Déclaration des états des relais
  digitalWrite(relais8, HIGH);           // Déclaration des états des relais
  pinMode(bouton, INPUT);                // Déclaration bouton en entrée
  pinMode(fin_prog, OUTPUT);              // 
  digitalWrite(fin_prog, LOW);           // 
  pinMode(led_temoin, OUTPUT);              // 
  digitalWrite(led_temoin, LOW);           // 

  Wire.begin();
  Serial.begin(9600);

  linkeroled.init();
  linkeroled.setNormalDisplay();         // Set display to normal mode (i.e non-inverse mode)
  //linkeroled.setInverseDisplay();      // Set display to inverse mode 
  linkeroled.setHorizontalMode();        // Set addressing mode to Page Mode
  linkeroled.clearDisplay();             // Efface l'écran
  linkeroled.setTextXY(4,1);             // Set the cursor to Xth Page, Yth Column
  linkeroled.putString ("Cycle");        // Affiche "Cycle" 
}

void loop ()
{
  int valeur = digitalRead(10);           // Lit l'état de la broche 10 et met le résultat dans la variable "valeur"
  Serial.println(valeur, DEC);            // Affiche la variable "valeur" dans le Terminal Serie
  if (valeur!=0)                        // Si bouton appuyé
  {
    activation();                         // Lancement "activation"
  }
  else
  {
    Serial.println("attente top depart");
    delay(5000); 
  }


}

void activation ()                      // Sous programme "activation"  
{  
  Serial.println(y);

  for (int j=0; j < 3; j=j+1){        // j=nombre de séries (cycles 5 min ON - 4min30sec charge - 30sec OFF)
    Serial.println("nombre de serie= ");
    Serial.println(j, DEC);            // 
    for (int i=0; i < 5; i=i+1){     // i=nombre de cycles 5 min ON - 4min30sec charge - 30sec OFF valeur initiale = 12 cycle
      Serial.println("nombre de cycle= ");
      Serial.println(i, DEC);            // 
      linkeroled.setTextXY(4,9);        // Set the cursor to Xth Page, Yth Column
      linkeroled.putNumber(y);          // Affiche le n° de cycle 

      Serial.println("relais ON 1.5 sec");         
      digitalWrite(led_temoin, HIGH);       // 
      digitalWrite(relais1, LOW);       // Fermeture relais 1 --> ON tondeuse 1
      digitalWrite(relais2, LOW);       // Fermeture relais 2 --> ON tondeuse 2
      digitalWrite(relais3, LOW);       // Fermeture relais 3 --> ON tondeuse 3 
      digitalWrite(relais4, LOW);       // Fermeture relais 4 --> ON tondeuse 4
      digitalWrite(relais5, LOW);       // Fermeture relais 5 --> ON tondeuse 5
      digitalWrite(relais6, LOW);       // Fermeture relais 6 --> ON tondeuse 6
      delay(1500);                    // 5 min ON (300000)

      Serial.println("relais OFF 0.1 sec");         
      digitalWrite(led_temoin, LOW);       // 
      digitalWrite(relais1, HIGH);       // Ouverture relais 1 --> OFF tondeuse 1
      digitalWrite(relais2, HIGH);       // Ouverture relais 2 --> OFF tondeuse 2
      digitalWrite(relais3, HIGH);       // Ouverture relais 3 --> OFF tondeuse 3
      digitalWrite(relais4, HIGH);       // Ouverture relais 4 --> OFF tondeuse 4
      digitalWrite(relais5, HIGH);       // Ouverture relais 5 --> OFF tondeuse 5
      digitalWrite(relais6, HIGH);       // Ouverture relais 6 --> OFF tondeuse 6
      delay(100);                      // 10 sec OFF (10000)

      Serial.println("charge 1 sec + 0.2 sec");       
      digitalWrite(relais8, LOW);       // Fermeture relais 8 --> Charge des tondeuses
      delay(1000);                    // 4 min 30sec de charge (270000)
      digitalWrite(relais8, HIGH);      // Ouverture relais 8 --> Arrêt charge des tondeuses
      delay(200);                     // Pause 20 sec (20000) pour 5 min OFF (4min30sec de charge + 30sec OFF)

      y++;                              // Incrementation y=nombre de cycles

    }
    Serial.println("charge 2 sec"); 
    digitalWrite(relais8, LOW);         // Fermeture relais 8 --> Charge des tondeuses
    delay(2000);                      // 15 minutes de charge (900000)
    digitalWrite(relais8, HIGH);        // Ouverture relais 8 --> Arrêt charge des tondeuses

  }

  Serial.println("pause 3 sec"); 
  delay(3000);                      // Pause 2h (7 200 000)
  digitalWrite(fin_prog, LOW);       // 

}



