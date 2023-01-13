import sys,os
import json

if len(sys.argv)>1:
  fdir=sys.argv[1]
else:
  fdir=os.getcwd()

fexe=['wine',os.path.join(fdir,'bin/x64/factorio.exe')]

def pj(x):
  print(json.dumps(x,indent=2))
