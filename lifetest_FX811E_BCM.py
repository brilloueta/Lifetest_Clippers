#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bibliothèques
try:
    import RPi.GPIO as GPIO
except ImportError:
    print('LOADING MOCK GPIO')
    import mock_gpio as GPIO

import argparse
import json
import pathlib
import sys
import time

DEFAULT_APP_STATE = {
    'cycles': 0,
    'date': None,
    'pas_incr': 1
}


def dump_app_state(file_path, **kwargs):
    state = load_app_state(file_path)
    state.update(kwargs)
    state['date'] = date_sec_epoch()

    with open(file_path, 'w') as fd:
        json_str = json.dumps(state)
        fd.write(json_str)


def load_app_state(file_path):
    path = pathlib.Path(file_path)
    if not path.exists():
        return DEFAULT_APP_STATE

    with path.open('r') as fd:
        json_str = fd.read()
        d = json.loads(json_str)
        return d


class App(object):
    def __init__(self, log_file, app_state_file):
        self.log_file = log_file
        self.app_state_file = app_state_file

    def get_cycles(self):
        return load_app_state(self.app_state_file)['cycles']

    def set_cycles(self, cycle):
        dump_app_state(self.app_state_file, cycles=cycle)

    def get_pas_incr(self):
        return load_app_state(self.app_state_file)['pas_incr']

    def set_pas_incr(self, pas_incr):
        dump_app_state(self.app_state_file, pas_incr=pas_incr)

    def log_to_csv(self, cycles):
        log_to_csv(self.log_file, cycles)


def date_sec_epoch():
    #return time.strftime('%d/%m/%y %H:%M:%S', time.localtime())
    return time.time()

def log_time():
    return time.strftime('%d/%m/%y %H:%M:%S', time.localtime(date_sec_epoch()))

def arduino_idle():
    GPIO.output(25,GPIO.LOW)


def pause_board(msg, delay=15):
    print(msg, time.strftime('%d/%m/%y %H:%M:%S', time.localtime(date_sec_epoch())))
    arduino_idle()
    time.sleep(delay)


def log_to_csv(file_path, cycles):
    with open(file_path, "a") as fd:
        fd.write(str(date_sec_epoch()))
        fd.write(", ")
        fd.write(log_time())
        fd.write(", ")
        fd.write(str(cycles))
        fd.write("\n")


def init_cycles(app):
    cycles_string = app.get_cycles()
    print ('La derniere valeur enregistree du compteur est {}'.format(cycles_string))
    choix = input('Souhaitez vous modifier la valeur ? Y/N \n')

    if choix.lower() in ['y', 'yes']:
        cycles_string = input('\nSaisir la nouvelle valeur pour le compteur \n')
        print ('\nLa nouvelle valeur du compteur est {} \n'.format(cycles_string))
        app.set_cycles(int(cycles_string))        # dump de l'etat courant

    elif choix.lower() in ['n', 'no']:
        print ('\nLa valeur enregistree du compteur est {} \n'.format(cycles_string))
        cycle = int(cycles_string)

    else:
        print ("Le choix n'est pas repertorie, le prog s'arrete ici ! \n \n")
        sys.exit(0)


def init_pas_incr(app):
    pas_incr = app.get_pas_incr()
    print ('chaque fin de boucle ajoute {} cycles de 5min ON'.format(pas_incr))
    choix = input('Souhaitez vous modifier la valeur ? Y/N \n')

    if choix.lower() in ['y', 'yes']:
        pas_incr = input('\nSaisir la nouvelle valeur de pas \n')
        print ('\nchaque fin de boucle ajoute {} cycles de 5min ON \n'.format(pas_incr))
        app.set_pas_incr(int(pas_incr))        # dump de l'etat courant

    elif choix.lower() in ['n', 'no']:
        print ('\nchaque fin de boucle ajoute dorénavant {} cycles de 5min ON \n'.format(pas_incr))
        pas_incr = int(pas_incr)

    else:
        print ("Le choix n'est pas repertorie, le prog s'arrete ici ! \n \n")
        sys.exit(0)


def main(args):
    app = App(
        log_file=args.log_file,
        app_state_file=args.app_state_file
    )
    # configurations
    GPIO.setmode(GPIO.BCM)                      # mode de numérotation des pins
    GPIO.setwarnings(False)                     # supprime les messages d'erreurs

    # declaration des I/O
    GPIO.setup(25,GPIO.OUT, initial=GPIO.LOW)           # la pin 25 réglee en sortie, valeur basse par défaut => départ cycle ARDUINO
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # la pin 4 réglée en entrée => bouton bascule programme actif sur raspberry
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # la pin 19 réglée en entrée => signal haut envoyé par arduino en fin de programme arduino

    # variables perso
    init_cycles(app)
    init_pas_incr(app)
    
    # Verifie les conditions pour lancer le prog arduino
    while True:

        fin_arduino = GPIO.input(19)
        bouton_bascule = GPIO.input(4)

        current_day = time.strftime('%A',time.localtime(date_sec_epoch()))
        current_hour = int(time.strftime('%H',time.localtime(date_sec_epoch())))

        # tant que l'arduino n'a pas termine son programme continue ce qui suit
        if fin_arduino == 0:
            print ("cycles ON/OFF terminé", log_time())
            
            # verifie que le bouton bascule raspberry est active
            if bouton_bascule == 0:
                print ("selecteur en position ON", log_time())
            
                # condition if, si jour = jour de semaine samedi ou dimanche alors demarrer, sinon attendre 15 minutes
                if current_day.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
                    print ("programme dans les jours fixes", log_time())
                
                    # condition if, si heure >8H et <17H alors demarrer, sinon attendre 15 minutes
                    if current_hour >= 8 and  current_hour <= 17:
                        print ("programme dans les heures fixes", log_time())

                        #depart cycle
                        GPIO.output(25,GPIO.HIGH)       # depart cycle pour l'arduino

                        #affichage dans le shell
                        print ("depart programme le ", log_time(), "\n")

                        old_cycle = cycle
                        cycle += pas_incr
                        print('Le compteur passe de {} à {}'.format(old_cycle, cycle))

                        app.set_cycles(cycle)        # dump de l'etat courant
                        app.log_to_csv(cycle)

                        time.sleep(50)              # on ne change rien pendant X minutes, initalement 1 minute (tps supérieur au déroulement du prog arduino)

                    else:
                        pause_board("programme en dehors des heures fixes")

                else:
                    pause_board("programme en dehors des jours fixes")

            else:
                pause_board("selecteur en position OFF")

        else:
            pause_board("cycles ON/OFF déja en cours")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--log-file',
                        default='Log_Lifetest.csv',
                        help="Path to the log file (CSV)")
    parser.add_argument('-a', '--app-state-file',
                        default='app_state.json',
                        help="Path to the app state file (JSON)")
    return parser.parse_args()


if __name__ == '__main__':
    main(get_args())
