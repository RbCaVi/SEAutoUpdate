import sys,os
import json

itemtypes=[
  'item',
  'ammo',
  'capsule',
  'gun',
  'item-with-entity-data',
  'item-with-label',
  'item-with-inventory',
  'blueprint-book',
  'item-with-tags',
  'selection-tool',
  'blueprint',
  'copy-paste-tool',
  'deconstruction-item',
  'upgrade-item',
  'module',
  'rail-planner',
  'spidertron-remote',
  'tool',
  'armor',
  'repair-tool'
]

devel=True
qpy=False

if qpy:
  fdir='/storage/emulated/0/qpython/projects3/SEAutoUpdate-main/SEAutoUpdate-main/'
else:
  if len(sys.argv)>1:
    fdir=sys.argv[1]
  else:
    fdir=os.getcwd()

fexe=['wine',os.path.join(fdir,'bin/x64/factorio.exe')]

difficulty=['normal','expensive']

def pj(x):
  print(json.dumps(x,indent=2))

def trace(f):
    def g(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            print(args,kwargs)
            raise e
    return g
