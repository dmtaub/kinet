#!/usr/bin/env python
from kinet import *
from sys import argv, exit
import time

if len(argv) <3:
    print("Usage: ./rgb.py <red> <green> <blue>\nr/g/b values from 0-255\n")
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
  ratio = 0 
  steps = 20
  pause = 0.05
  def _scale(orig_new):
   step = orig_new[2]
   return ((orig_new[1]-orig_new[0])*step/steps)
  def scale(orig_col,new_col,step):
    return map(_scale, zip(orig_col,new_col,[step,step,step]))
    #return(col*b/stepsI#)

  for step in range(steps):
    ratio += 1
    nextVal = [scale(start,destination,ratio)]*numLights
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
while 1:
  print "-> ",
  try:
    rgbDest = input()

    if type(rgbDest) is not tuple:
      if type(rgbDest) is int and rgbDest<=255:
        rgbDest = (rgbDest,)
      else: 
        raise(Exception("Max RED -> 255,0,0"))
    if len(rgbDest) == 1:
      rgbDest = rgbDest + (0,0)
    elif len(rgbDest) == 2:
      rgbDest += (0,)
    rgbStart = rgbDest
  except Exception as e:
    print e.message
    if rgbStart is None:
      rgbStart = (0,0,0)
      rgbDest = (r,g,b)
    else:
      #print "start: ",rgbStart," dest: ",rgbDest
      print "Reverse",
      a = rgbDest
      rgbDest = rgbStart
      rgbStart = a
 
  print "fading to R-%d, G-%d, B-%d"%rgbDest
  fadeToDest(rgbDest,rgbStart or (0,0,0))
