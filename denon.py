#!/usr/bin/python
# librarie de pilotage de l'ampli
import os
import serial
import time
import sys
import re
import json
import io

#### tout ce qui est json devrait etre deporte dans le cgi

#### volume: 00= -80db (inaudible)
#### volume: 80=   0db (hyper fort)

class Denon:
  "objet pour Denon"
  #def __init__(self):
  def __init__(self, serialport='/dev/ttyUSB_cableRS232', dontprint=0):
    self.vol = 0
    self.power = ""
    self.si = ""
    self.muted = ""
    self.delayed = 0
    self.response = ""
    self.dontprint = dontprint
    #self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  #/dev/ttyS0 n'est pas accessible depuis apache on dirait...
    #self.ser = serial.Serial('ttyS0', 9600, timeout=1)  #/dev/ttyS0 n'est pas accessible depuis apache on dirait...
    self.ser = serial.Serial(serialport, 9600, timeout=0.2)  #/dev/ttyS0 n'est pas accessible depuis apache on dirait...
    #self.ser = serial.Serial('ttyUSB1', 9600, timeout=1) #2
    #puisque le readline ne permet plus de specifier une fin de ligne = \r
    self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

  
  def print_data(self, data):
    if self.dontprint == 0:
      print(data)

  def read_response_simple(self):
    #data = self.ser.readline(None,'\r').strip()
    data = self.sio.readline().strip()
    while (data):
      self.print_data(data)
      #data = self.ser.readline(None,'\r').strip()
      data = self.sio.readline().strip()

  def read_response(self):
    response = ""
    #data = self.ser.readline(None,'\r').strip()
    data = self.sio.readline().strip()
    while (data):
      response = response + "\n" + data
      self.print_data(data)
      #data = self.ser.readline(None,'\r').strip()
      data = self.sio.readline().strip()
    self.response = response
    self.analyse_response()

  def analyse_response(self, response=None):
    if (response is None):
      response=self.response
    # volume MV
    p = re.compile('MV(\\d\\d)\\d?', re.MULTILINE) # qqfois il y a trois chiffres, le dernier represente un demi dB (qui ne nous interesse pas)
    m = p.search(response)
    if (m != None):
      self.vol = int(m.group(1))
    # source SI
    p = re.compile('SI([A-Z0-9-]+)', re.M) # SICD SIDVD SIVCR-1 SITUN
    m = p.search(response)
    if (m != None):
      self.si = m.group(1)
    # power PW
    p = re.compile('PW([A-Z]+)', re.M) # PWON ou PWSTANDBY
    m = p.search(response)
    if (m != None):
      self.power = m.group(1)
    # MUTE
    p = re.compile('MU([A-Z]+)', re.M) # MUON ou MUOFF
    m = p.search(response)
    if (m != None):
      self.muted = m.group(1)
    # DELAY
    p = re.compile('DELAY(\\d+)', re.M) # DELAY 0 a 150ms
    m = p.search(response)
    if (m != None):
      self.delayed = int(m.group(1))
    # AJOUTER INPUT


  def send_command(self, command):
    # print_data ("*%s*" % (command,))
    self.ser.write(command + '\r')
    #self.sio.write(command + '\r')
    #self.sio.flush()
    self.read_response()

  def full_status(self):
    a = self.dontprint
    self.dontprint=1
    self.power_status()
    if (self.power == "ON"):
      self.what_si()
      self.mv_status()
      self.mute_status()
      print(json.dumps( dict(power=self.power, vol=self.vol, si=self.si, mute=self.muted) ))
    self.dontprint = a

  def power_on(self):
    self.ser.write("PWON\r")
    #self.sio.write("PWON\r")
    #self.sio.flush()
    time.sleep(2)
    self.read_response()

  def power_off(self):
    command = "PWSTANDBY"
    self.send_command(command)

  def power_status(self):
    command = "PW?"
    self.send_command(command)  # retour attendu: PWON ou PWSTANDBY  (entre autres)

  def what_si(self):
    command = "SI?"
    self.send_command(command)

  def si_vdp(self):
    command = "SIVDP"
    self.send_command(command)

  def si_vaux(self):
    command = "SIV.AUX"
    self.send_command(command)

  def si_tv(self):
    command = "SITV"
    self.send_command(command)

  def si_tun(self):
    command = "SITUN"
    self.send_command(command)

  def si_cd(self):
    command = "SICD"
    self.send_command(command)

  def si_dvd(self):
    command = "SIDVD"
    self.send_command(command)

  def si_dbs(self):
    command = "SIDBS"
    self.send_command(command)

  def si_vcr1(self):
    command = "SIVCR-1"
    self.send_command(command)

  def si_vcr2(self):
    command = "SIVCR-2"
    self.send_command(command)

  def delay_up(self):
    command = "DELAY UP"
    self.send_command(command)

  def delay_down(self):
    command = "DELAY DOWN"
    self.send_command(command)

  def delay(self, delay):
    command = "DELAY %d" % (delay,)
    self.send_command(command)

  def mv_up(self):
    command = "MVUP"
    self.send_command(command)

  def mv_down(self):
    command = "MVDOWN"
    self.send_command(command)

  def mv(self, vol):
    command = "MV%d" % (vol,)
    self.send_command(command)

  #def mv_status(self):
    #command = "MV?"
    ## equivalent de send_command
    ## print_data( "*%s*" % (command,))
    #self.ser.write(command + '\r')
    ## equivalent de read_response
    #data_string = ""
    #data = self.ser.readline(None,'\r').strip()
    #p = re.compile('MV(\\d\\d)\\d?') # qqfois il y a trois chiffres, le dernier represente un demi dB (qui ne nous interesse pas)
    #while (data):
      #data_string = data_string + "\n" + data
      #m = p.match(data)
      #if (m != None):
        #self.vol = int(m.group(1))
        #data = self.ser.readline(None,'\r').strip()
    #self.print_data(data_string)
    #return vol

  def mv_status(self):
    command = "MV?"
    self.send_command(command)
    return self.vol
  
  def delay_status(self):
    command = "DELAY?"
    self.send_command(command)
    return self.delayed
  
  def mute_status(self):
    command = "MU?"
    self.send_command(command)
    return self.muted
  
  def mute(self):
    command = "MUON"
    self.send_command(command)

  def unmute(self):
    command = "MUOFF"
    self.send_command(command)

