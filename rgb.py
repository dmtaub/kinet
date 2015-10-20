#!/usr/bin/env python
from kinet import *
from sys import argv, exit
import time

if len(argv) <3:
    print("Uwage: ./rgb.py <red> <green> <blue>\n")
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

def scale(a,b):
  return(a*b/steps)

for step in range(steps):
  ratio += 1
  for fixture in fix:
    #ratio += (step) % steps / float(steps)
    #fixture.hsv = (ratio, 1.0, 1.0)
    #print ratio, r,g,b
    #import pdb; pdb.set_trace()
    #print ratio, r,g,b, rgb
    fixture.rgb = (scale(r,ratio),scale(g,ratio),scale(b,ratio))
    #print rgb
    #print pds
  pds.go()
  time.sleep(pause)
