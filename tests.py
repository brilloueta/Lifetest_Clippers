#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

import lifetest_FX811E_BCM as lt
import time

#lt.log_counter(30)
#lt.load_app_state()
#lt.set_cycles(8)
#lt.set_pas_incr(16)

def date_str():
    return time.time()

print('seconds since epoch : ', date_str())
print('date since epoch : ', time.strftime('%d/%m/%y %H:%M:%S', time.localtime(date_str())))

print ('current_day = ', time.strftime('%A',time.localtime(date_str())))
print ('current_hour = ', int(time.strftime('%H',time.localtime(date_str()))))
