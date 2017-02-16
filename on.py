#!/usr/bin/python
# reveil matin : power on + input = zubunew (dbs) + volume

import os
import time
import sys
import denon
import cgi
import re

def main():

  denonctl = denon.Denon('/dev/ttyS0',1)
  denonctl.power_on()
  time.sleep(2)
  #denonctl.mv(40)
  denonctl.mv(45)
  denonctl.si_dbs()
  time.sleep(2)
  #denonctl.full_status()


if __name__ == '__main__':
  main()
