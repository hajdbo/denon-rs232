#!/usr/bin/python

import os
import time
import sys
import denon
import cgi
import re

def main():

  denonctl = denon.Denon('/dev/ttyS0',1)
  denonctl.what_si()
  denonctl.power_status()
  if (denonctl.power == "OFF"):
    denonctl.power_on()
    denonctl.mv(45)
  if (denonctl.si != "DBS"):
    denonctl.si_dbs()

if __name__ == '__main__':
  main()
