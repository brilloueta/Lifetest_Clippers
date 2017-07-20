#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bibliothèques
try:
    import RPi.GPIO as GPIO
except ImportError:
    print('LOADING MOCK GPIO')
    import mock_gpio as GPIO

import time
import sys

LOG_FILE_TXT = "Log_FX811E_Lifetest.txt"
LOG_FILE_CSV = "Log_FX811E_Lifetest.csv"

def date_str():
    return time.strftime('%d/%m/%y %H:%M:%S', time.localtime())

def pause_board(msg):
    log_time = date_str()
    print(msg, log_time)
    GPIO.output(25,GPIO.LOW)        # information vers arduino de ne rien faire
    time.sleep(pause_delay_sec)     # on ne change rien pendant X minutes, initialement 15 minutes

def log_counter(cycles):
    fichier = open(LOG_FILE_TXT, "w")
    fichier.write(str(cycles))
    fichier.close()

    # ajoute la valeur dans le fichier log CSV
    #fichier = open(LOG_FILE_CSV,"a") # "a" pour ajouter
    #fichier.write(compteur_string)
    #fichier.write(", ")
    #fichier.write(log_time)
    #fichier.write("\n")
    #fichier.close()


def main():
    # configurations
    GPIO.setmode(GPIO.BCM)                      # mode de numérotation des pins
    GPIO.setwarnings(False)                     # supprime les messages d'erreurs

    # declaration des I/O
    GPIO.setup(25,GPIO.OUT, initial=GPIO.LOW)           # la pin 25 réglee en sortie, valeur basse par défaut => départ cycle ARDUINO
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # la pin 4 réglée en entrée => bouton bascule programme actif sur raspberry
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # la pin 19 réglée en entrée => signal haut envoyé par arduino en fin de programme arduino

    # variables perso

    pas_incr = 96                                       # chaque fin de boucle ajoute 96 cycles de 5min ONcycle_arduino()

    pause_delay_sec = 15



    # recuperer la valeur du compteur
    fichier = open(LOG_FILE_TXT,"r")
    compteur_string = fichier.read()
    compteur = int(compteur_string)
    print ("La derniere valeur enregistree du compteur est ", compteur_string,"\n")

    choix = input("Souhaitez vous modifier la valeur ? Y/N\n")

    if choix.lower() in ["y", "yes"]:
        compteur_string = input("Saisir la nouvelle valeur pour le compteur\n")
        print ("La nouvelle valeur du compteur est ", compteur_string, "\n")
        compteur = int(compteur_string)
        fichier = open(LOG_FILE_TXT,"w") #"w" pour écraser
        fichier.write(compteur_string)
        fichier.close()

    elif choix.lower() in ["n", "no"]:
        compteur_string = str(compteur)
        print ("La valeur enregistree du compteur est ", compteur_string, "\n")
        compteur = int(compteur_string)

    else:
        print ("Le choix n'est pas repertorie, le prog s'arrete ici !")
        sys.exit(0)





    # Verifie les conditions pour lancer le prog arduino
    while True:

        fin_arduino = GPIO.input(19)
        bouton_bascule = GPIO.input(4)

        current_day = time.strftime('%A',time.localtime())
        current_hour = time.strftime('%H',time.localtime())
        current_hour_int = int(current_hour)

        # tant que l'arduino n'a pas termine son programme continue ce qui suit
        if fin_arduino == 0:
            log_time = date_str()
            print ("programme ARDUINO terminé", log_time)
            
            # verifie que le bouton bascule raspberry est active
            if bouton_bascule == 0:
                log_time = date_str()
                print ("selecteur en position ON", log_time)
            
                # condition if, si jour = jour de semaine samedi ou dimanche alors demarrer, sinon attendre 15 minutes
                if current_day.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
                    log_time = date_str()
                    print ("programme dans les jours fixes", log_time)
                
                    # condition if, si heure >8H et <17H alors demarrer, sinon attendre 15 minutes
                    if current_hour_int >= 8 and  current_hour_int <= 17:
                        log_time = date_str()
                        print ("programme dans les heures fixes", log_time)

                        #depart cycle
                        GPIO.output(25,GPIO.HIGH)       # depart cycle pour l'arduino

                        #affichage dans le shell
                        log_time = date_str()
                        print ("depart programme le ", log_time, "\n")

                        old_compteur = compteur
                        compteur += pas_incr
                        print('Le compteur passe de {} à {}'.format(old_compteur, compteur))

                        log_counter(compteur)

                        time.sleep(50)              # on ne change rien pendant X minutes, initalement 1 minute (tps supérieur au déroulement du prog arduino)

                    else:
                        pause_board("programme en dehors des heures fixes")

                else:
                    pause_board("programme en dehors des jours fixes")

            else:
                pause_board("selecteur en position OFF")

        else:
            pause_board("programme ARDUINO déja en cours")


if __name__ == '__main__':
    main()
