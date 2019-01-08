#!/usr/bin/python

import denon

def main():

  denonctl = denon.Denon('/dev/ttyUSB_cableRS232',1)
  denonctl.what_si()
  denonctl.power_status()
  if (denonctl.power == u"STANDBY"):
    denonctl.power_on()
    denonctl.mv(45)
  if (denonctl.si != u"DBS"):
    denonctl.si_dbs()

if __name__ == '__main__':
  main()
