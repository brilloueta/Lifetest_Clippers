#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

import lifetest_FX811E_BCM as lt
import time

app = lt.App('test_log.csv', 'test_app_state.json')

app.log_to_csv(30)
app.set_cycles(8)
app.set_pas_incr(16)

app.log_to_csv(60)
app.set_cycles(16)
app.set_pas_incr(32)

#print('seconds since epoch : ', lt.date_sec_epoch())
#print('date since epoch : ', time.strftime('%d/%m/%y %H:%M:%S', time.localtime(lt.date_sec_epoch())))
#print('\n')

#print ('current_day = ', time.strftime('%A',time.localtime(lt.date_sec_epoch())))
#print ('current_hour = ', int(time.strftime('%H',time.localtime(lt.date_sec_epoch()))))
#print('\n')
