#!/usr/bin/python

import os
import sys
import denon

def main():

  denonctl = denon.Denon('/dev/ttyS0',1)
  denonctl.what_si()
  denonctl.power_status()
  if (denonctl.power == u"OFF"):
    denonctl.power_on()
    denonctl.mv(45)
  if (denonctl.si != u"DBS"):
    denonctl.si_dbs()

if __name__ == '__main__':
  main()
