import json
import os
import sys
import re

import util
import fix

# data extracts the data.raw table from factorio or a cached log file

regen=False

def getmods():
  # get the list of mods in factorio
  mods=[
    *filter(lambda x:x.is_dir() or x.name.endswith('.zip'),
      os.scandir(os.path.join(util.fdir,'mods'))
    )
  ]
  nmods=[] # the list of mod names (no extension or version)
  for mod in mods:
    if mod.name.endswith('.zip'):
      nmods.append(mod.name.rsplit('_',maxsplit=1)[0])
    else:
      with open(os.path.join(mod.path,'info.json')) as f:
        nmods.append(json.load(f)['name']) # get the mod's name from its info.json
  return nmods

if regen:
  import shutil
  try:
    # clear any old datalogger mod
    shutil.rmtree(os.path.join(util.fdir,'mods','datalogger'))
  except:
    pass

  info={ # the data in the datalogger mod's info.json
    "name": "datalogger",
    "version": "0.0.1",
    "title": "Log the entire data.raw table",
    "author": "A person named Robert",
    "factorio_version": "1.1",
    "dependencies": getmods()
  }
  # add the mod to factorio
  shutil.copytree('datalogger',os.path.join(util.fdir,'mods/datalogger'))
  with open(os.path.join(util.fdir,'mods/datalogger/info.json'),'w') as f:
    json.dump(info,f,indent=2)

d=os.getcwd() # save the cwd to restore it later
os.chdir(util.fdir)

# outf is the (possibly cached) output from factorio
if util.qpy or not regen:
  outf=open(os.path.join(util.fdir,'factorio-current.log'))
else:
  import subprocess
  subprocess.run(util.fexe+['--create','saves/protodump.zip']) # create a dummy save
  fproc=subprocess.Popen(util.fexe+['--start-server','saves/protodump.zip'],stdout=subprocess.PIPE,text=True)
  outf=fproc.stdout

fout=''
while True:
  out=outf.readline()
  fout=fout+out
  if 'Hosting game at' in fout[-30:]+out:
    del fout
    break

outf.close()

if not util.qpy and regen:
  import signal
  fproc.send_signal(signal.SIGINT)

# get just the data i need
data=fout.split('__datalogger__/data-final-fixes.lua')[2]
data=data.split(' ',maxsplit=1)[1].rsplit('\n',maxsplit=1)[0]

data=json.loads(data)

# fix the recipes and tech
data['recipe']={x:fix.fixrecipe(data['recipe'][x]) for x in data['recipe']}
data['technology']={x:fix.fixtech(data['technology'][x]) for x in data['technology']}

os.chdir(d)

import process

def init():
    # creates pdata
    global pdata
    pdata={}
    pdata['recipe']={x:process.processrecipe(x) for x in data['recipe']}
    pdata['technology']={x:process.processtech(x) for x in data['technology']}
