#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

import lifetest_FX811E_BCM as lt

print(lt.get_cycles())
lt.set_cycles(76)
print(lt.get_cycles())
lt.set_cycles(42)
print(lt.get_cycles())
