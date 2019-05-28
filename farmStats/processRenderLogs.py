#!/usr/bin/python

from __future__ import print_function

import os,sys
from collections import namedtuple

class RenderJob() : 
  def __init__(self, date,duration,durationString,threads,memory,swap,renderer) :
    self.date=date
    self.duration=duration
    self.durationString=durationString
    self.threads=threads
    self.memory=memory
    self.swap=swap
    self.renderer=renderer
  def __str__(self):
    return '%s\t%d\t%s\t%d\t%d\t%d\t%s' %(self.date,self.duration,self.durationString,self.threads,self.memory,self.swap,self.renderer)

Jobs=[]

def processJob(job,renderer) :
  date=''
  threads=0
  mem=0
  swap=0
  duration=0
  durationString=''
  for j in job :
    if j.startswith('start') :
      start=j.find('[')+1
      end=j.find(']')  
      date=j[start:end].replace(',',' ')
    elif j.startswith('thread:') :
      start=j.find(' ')
      threads=int(j[start:])
    elif j.startswith('mem:') :
      start=j.find(' ')
      mem=int(j[start:])
    elif j.startswith('swap:') :
      start=j.find(' ')
      swap=int(j[start:])
    elif j.startswith('time:') :
      start=j.find('[')+1
      end=j.find(']')
      durationString=j[start:end]
      duration=int(j[end+1:])

      
  Jobs.append(RenderJob(date,duration,durationString,threads,mem,swap,renderer))

dirs=os.listdir('.')
cwd=os.getcwd()
for d in dirs :
  try :
    os.chdir(d)
    print('changing to directory {0}'.format(d))
    files=os.listdir('.')
    for file in files :
      if file.endswith('.sts') :
        print('processing {0}'.format(file))
        with open(file, 'r') as f:
          job=f.readlines()
          job=job[0].split('\t')
          outFile=file[0:file.find('.')]
          outFile=outFile+'.out'
          try :
            with open(outFile,'r') as outlog :
              log=outlog.read()
              renderer='unknown'
              if 'houdini' in log :
                renderer='houdini'
              elif 'mtoa' in log :
                renderer='maya arnold'
              elif 'vray' in log :
                renderer='maya vray'
              elif 'RenderMan' in log :
                renderer='Renderman'
              else :
                print("Unknown {0}".format(outlog))

              processJob(job,renderer)
          except IOError :
            pass
  except OSError :
    pass
  os.chdir(cwd)

with open('outfile.csv','w') as outfile :
  outfile.write('date,duration,durationString,threads,memory,swap,renderer\n')
  for j in Jobs :
    if( j.date != 'None') :
      outfile.write('%s,%d,%s,%d,%d,%d,%s\n' %(j.date,j.duration,j.durationString,j.threads,j.memory,j.swap,j.renderer))