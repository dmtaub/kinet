#!/usr/bin/env python
from kinet import *
from sys import argv, exit
import time

if len(argv) <3:
    print("Usage: ./led.py <red> <green> <blue>\ndefault r/g/b values from 0-255\n")
    exit()

print argv[0]
# Our ethernet attached power supply.
pds = PowerSupply("192.168.1.244")
numLights = 50
fix = [None]*numLights

# Our light fixtures
for i in range(0,numLights):
    fix[i] = FixtureRGB(0+3*i)

# Attach our fixtures to the power supply
for i in range(0,numLights):
    pds.append(fix[i])


r= int(argv[1])
g= int(argv[2])
b= int(argv[3])



def fadeToDest(destination, start=[0,0,0]):
  print "fading to R-%d, G-%d, B-%d"%destination
  start = tuple(start)
  ratio = 0.0 
  steps = 20
  pause = 0.05
  def _scale(orig_new):
   col= (orig_new[0]*(1-ratio)+orig_new[1]*ratio)
   return col
  def scale(orig_col,new_col):
    return map(_scale, zip(orig_col,new_col))

  for step in range(steps):
    ratio = (step+1)/float(steps)
    nextVal = [scale(start,destination)]*numLights
    for idx in range(len(fix)):
      fixture = fix[idx]
      fixture.rgb = nextVal[idx] 
      #print rgb
      #print pds
    pds.go()
    time.sleep(pause)

STARTMSG = "\n RED=on G=off B=off -> 255,0,0 \n"

print STARTMSG
count = 0
rgbStart = None
rgbDest = None
while 1:
  valid=True
  #print "start: ",rgbStart," dest: ",rgbDest
  print "-> ",
  try:
    rgbDest = input()

    if type(rgbDest) is not tuple:
      if type(rgbDest) is int and rgbDest<=255:
        rgbDest = (rgbDest,)*3
      else: 
        raise(Exception("Max RED -> 255,0,0"))
    if len(rgbDest) == 1:
      rgbDest = rgbDest + (0,0)
    elif len(rgbDest) == 2:
      rgbDest += (0,)
  except Exception as e:
    print e.message
    if False:
      pass # eventually set dest/start=default
    else:
      if rgbStart and rgbDest:
        valid = True
      print "Reverse",
  rgbDest = rgbDest or (r,g,b)
  rgbStart = rgbStart or (0,0,0)
  fadeToDest(rgbDest,rgbStart)
  if valid:  #input was valid, save val
    a = rgbStart 
    rgbStart = rgbDest
    rgbDest = a
