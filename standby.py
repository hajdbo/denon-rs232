#!/usr/bin/python
# power off de l'ampli

import os
import time
import sys
import denon
import cgi
import re

def main():

  denonctl = denon.Denon('/dev/ttyUSB_cableRS232',1)
  denonctl.power_off()


if __name__ == '__main__':
  main()
