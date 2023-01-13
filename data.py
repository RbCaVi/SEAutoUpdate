import json,shutil,os,subprocess,signal

import util
import fix

def getmods():
  mods=[*filter(lambda x:x.is_dir(),os.scandir(os.path.join(util.fdir,'mods')))]
#  mods=[mod.name.rsplit('_',maxsplit=1)[0] for mod in mods]
  nmods=[]
  for mod in mods:
    if mod.name.endswith('.zip'):
      nmods.append(mod.name.rsplit('_',maxsplit=1)[0])
    else:
      with open(os.path.join(mod.path,'info.json')) as f:
        nmods.append(json.load(f)['name'])
  return nmods

try:
  shutil.rmtree(os.path.join(util.fdir,'mods/datalogger'))
except:
  pass

info={
  "name": "datalogger",
  "version": "0.0.1",
  "title": "Log the entire data.raw table",
  "author": "A person named Robert",
  "factorio_version": "1.1",
  "dependencies": getmods()
}
shutil.copytree('datalogger',os.path.join(util.fdir,'mods/datalogger'))
with open(os.path.join(util.fdir,'mods/datalogger/info.json'),'w') as f:
  json.dump(info,f,indent=2)

os.chdir(util.fdir)
#subprocess.run(util.fexe+['--create','saves/protodump.zip'])
#fproc=subprocess.Popen(util.fexe+['--start-server','saves/protodump.zip'],stdout=subprocess.PIPE,text=True)
fproc=subprocess.Popen(['cat','factorio-current.log'],stdout=subprocess.PIPE,text=True)
fout=''
while True:
  out=fproc.stdout.readline()
#  print(out,end='')
  fout=fout+out
  if 'Hosting game at' in fout:
    break

fproc.send_signal(signal.SIGINT)
data=fout.split('__datalogger__/data-final-fixes.lua')[2]
data=data.split(' ',maxsplit=1)[1].rsplit('\n',maxsplit=1)[0]
data=json.loads(data)
data['recipe']={x:fix.fixrecipe(data['recipe'][x]) for x in data['recipe']}
#print(fout)


