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

steps = 20
pause = 0.05
ratio = 0 

r= int(argv[1])
g= int(argv[2])
b= int(argv[3])

start = [0,0,0]
destination = [r,g,b]

def _scale(orig_new):
 step = orig_new[2]
 return ((orig_new[1]-orig_new[0])*step/steps)
def scale(orig_col,new_col,step):
  return map(_scale, zip(orig_col,new_col,[step,step,step]))
  #return(col*b/stepsI#)

for step in range(steps):
  ratio += 1
  for fixture in fix:
    fixture.rgb = scale(start,destination,ratio)
    #print rgb
    #print pds
  pds.go()
  time.sleep(pause)
