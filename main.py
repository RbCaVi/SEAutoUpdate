import data
import fix
import locales as locale
import util
import wikiapi
import process
import towiki
#import imageio as iio
import skimage.io as sio
import skimage

sio.use_plugin('pil')

def replaceroots(path,roots):
    for root in roots:
        path=path.replace(root,roots[root])
    return path

data.init()
process.init()

import sys
import os

#datacards=[x for x in data.data['recipe'] if 'data' in x]

#util.pj(datacards)

#print(len(datacards))

silos=['rocket-silo','se-space-probe-rocket-silo']

cards=[x for x in data.data['item'] if 'data' in x]
cards.remove('se-junk-data')
util.pj([(card,process.produces['normal'].get((card,'item'))) for card in cards])
spacks=[x for x in data.data['tool'] if 'science' in x]
sims=[x for x in data.data['recipe'] if 'simulation' in x]
formats=[x for x in data.data['recipe'] if 'formatting' in x]
insights=[x for x in data.data['item'] if 'insight' in x]
cats=[x for x in data.data['item'] if 'catalogue' in x]
#sys.exit()
#util.pj(data.data['recipe'][datacards[0]])
#util.pj(data.data['recipe']['se-formatting-1'])
#util.pj(processrecipe(datacards[0]))
#util.pj(list(set([data.data['item-subgroup'][data.data['item'][x].get('subgroup','other')]['group'] for x in data.data['item']])))

graphicsroots={
    '__space-exploration-graphics__':'/storage/emulated/0/Documents/SE/space-exploration-graphics_0.6.13/space-exploration-graphics',
  }#  '__base__':'/storage/emulated/0/Documents/factorio-data-1.1.72/factorio-data-1.1.72/base'}
print(spacks)
#for item in cards+spacks:
    
def putitemonwiki(item,recipenames):
    idata=process.getitem(item)
    
    iconname=idata['icon']
    iconname=replaceroots(iconname,graphicsroots)
    iconsize=idata['icon_size']
    print(iconname)
    if '__' in iconname:
        print('icon not found, skipping '+item)
        return
    icon=sio.imread(iconname,plugin='pil',mode='RGBA',as_gray=False)[:iconsize,:iconsize]
    print(icon.shape)
    sio.imsave('temp.png',icon,'pil')
    
    recipes=[data.pdata['recipe'][r] for r in recipenames]
    
    info=towiki.towikiitem(item)
    info=towiki.towikirecipe(recipenames,info)
    if len(recipes)==0:
        info['producers']=silos
    infobox=towiki.toinfobox(info)
    
    realname=locale.itemlocale(item,data.data)[0]
    
    print(realname)
    
    category='\n<noinclude>[[Category:'+info['category']+']]</noinclude>'
    
    contents=infobox+category
    
    print(contents)
    
    
    wikiapi.upload('temp.png',realname+'.png')
    
    time=wikiapi.gettimestamp()
    
    util.pj(wikiapi.edit(realname,contents,time,createonly=False))

def puttechonwiki(tech):
    tdata=data.data['technology'][tech]
    
    iconname=tdata['icon']
    iconname=replaceroots(iconname,graphicsroots)
    iconsize=tdata['icon_size']
    
    if '__' in iconname:
        print('icon not found, skipping '+tech)
        return
    icon=sio.imread(iconname,plugin='pil',mode='RGBA',as_gray=False)[:iconsize,:iconsize]
    sio.imsave('temp.png',icon,'pil')
    
    info=towiki.towikitech(tech)
    infobox=towiki.toinfobox(info)
    
    realname=locale.techlocale(tech,data.data)[0] or tech
    
    print(realname)
    
    contents=infobox
    
    print(contents)
    
    
    wikiapi.upload('temp.png',realname+'.png')
    
    time=wikiapi.gettimestamp()
    
    util.pj(wikiapi.edit(realname,contents,time,createonly=False))

puttechonwiki('se-space-supercomputer-1')